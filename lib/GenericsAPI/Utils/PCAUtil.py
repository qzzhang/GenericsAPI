import time
import pandas as pd
import os
import uuid
import errno
from matplotlib import pyplot as plt
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objs as go
from plotly.offline import plot

from GenericsAPI.Utils.DataUtil import DataUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(('\n' if prefix_newline else '') + time_str + ': ' + message)


class PCAUtil:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _validate_run_pca_params(self, params):
        """
        _validate_run_pca_params:
            validates params passed to run_pca method
        """

        log('start validating run_pca params')

        # check for required parameters
        for p in ['input_obj_ref', 'workspace_name', 'pca_matrix_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _df_to_list(self, df):
        """
        _df_to_list: convert Dataframe to FloatMatrix2D matrix data
        """

        df.fillna(0, inplace=True)
        matrix_data = {'row_ids': df.index.tolist(),
                       'col_ids': df.columns.tolist(),
                       'values': df.values.tolist()}

        return matrix_data

    def _pca_df_to_excel(self, pca_df, result_dir, pca_matrix_ref):
        """
        write PCA matrix df into excel
        """
        log('writting pca data frame to excel file')
        pca_matrix_obj = self.dfu.get_objects({'object_refs': [pca_matrix_ref]})['data'][0]
        pca_matrix_info = pca_matrix_obj['info']
        pca_matrix_name = pca_matrix_info[1]

        file_path = os.path.join(result_dir, pca_matrix_name + ".xlsx")

        writer = pd.ExcelWriter(file_path)

        pca_df.to_excel(writer, "pca_matrix", index=True)

        writer.close()

    def _Matrix2D_to_df(self, Matrix2D):
        """
        _Matrix2D_to_df: transform a FloatMatrix2D to data frame
        """

        index = Matrix2D.get('row_ids')
        columns = Matrix2D.get('col_ids')
        values = Matrix2D.get('values')

        df = pd.DataFrame(values, index=index, columns=columns)

        return df

    def _pca_to_df(self, pca_matrix_ref):
        """
        retrieve pca matrix ws object to pca_df
        """
        log('converting pca matrix to data frame')
        pca_data = self.dfu.get_objects({'object_refs': [pca_matrix_ref]})['data'][0]['data']

        rotation_matrix_data = pca_data.get('rotation_matrix')
        explained_variance_ratio = pca_data.get('explained_variance_ratio')
        dimension = pca_data.get('pca_parameters').get('dimension')
        original_data_ref = pca_data.get('original_data')

        pca_df = self._Matrix2D_to_df(rotation_matrix_data)
        pca_df.loc['explained_variance_ratio'] = explained_variance_ratio

        if original_data_ref:
            log('appending instance group information to pca data frame')
            obj_data = self.dfu.get_objects({'object_refs': [original_data_ref]})['data'][0]['data']

            if dimension == 'row':
                attribute_mapping = obj_data.get('row_mapping')
            elif dimension == 'col':
                attribute_mapping = obj_data.get('col_mapping')
            else:
                attribute_mapping = None

            if attribute_mapping:
                # append instance col mapping from row/col_mapping
                pca_df['instance_group'] = pca_df.index.map(attribute_mapping)

        return pca_df

    def _save_pca_matrix(self, workspace_name, input_obj_ref, pca_matrix_name, rotation_matrix_df,
                         explained_variance_ratio, n_components, dimension):

        log('saving PCAMatrix')

        if not isinstance(workspace_name, int):
            ws_name_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            ws_name_id = workspace_name

        pca_data = {}

        pca_data.update({'rotation_matrix': self._df_to_list(rotation_matrix_df)})
        pca_data.update({'explained_variance_ratio': explained_variance_ratio})
        pca_data.update({'pca_parameters': {'n_components': str(n_components),
                                            'dimension': str(dimension)}})
        pca_data.update({'original_data': input_obj_ref})

        obj_type = 'KBaseExperiments.PCAMatrix'
        info = self.dfu.save_objects({
            "id": ws_name_id,
            "objects": [{
                "type": obj_type,
                "data": pca_data,
                "name": pca_matrix_name
            }]
        })[0]

        return "%s/%s/%s" % (info[6], info[0], info[4])

    def _pca_for_matrix(self, input_obj_ref, n_components, dimension):
        """
        _pca_for_matrix: perform PCA analysis for matrix object
        """

        data_matrix = self.data_util.fetch_data({'obj_ref': input_obj_ref}).get('data_matrix')

        data_df = pd.read_json(data_matrix)

        if dimension == 'col':
            data_df = data_df.T
        elif dimension != 'row':
            err_msg = 'Input dimension [{}] is not available.\n'.format(dimension)
            err_msg += 'Please choose either "col" or "row"'
            raise ValueError(err_msg)

        if n_components > min(data_df.index.size, data_df.columns.size):
            raise ValueError('Number of components should be less than min(n_samples, n_features)')

        # normalize sample
        log("Standardizing the matrix")
        s_values = StandardScaler().fit_transform(data_df.values)

        # Projection to ND
        pca = PCA(n_components=n_components, whiten=True)
        principalComponents = pca.fit_transform(s_values)
        explained_variance_ratio = list(pca.explained_variance_ratio_)

        col = list()
        for i in range(n_components):
            col.append('principal_component_{}'.format(i+1))

        rotation_matrix_df = pd.DataFrame(data=principalComponents,
                                          columns=col,
                                          index=data_df.index)

        return rotation_matrix_df, explained_variance_ratio

    def _generate_pca_report(self, pca_ref, pca_plot, workspace_name):
        log('creating report')

        html_report = list()
        report_shock_id = self.dfu.file_to_shock({'file_path': os.path.dirname(pca_plot),
                                                  'pack': 'zip'})['shock_id']
        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(pca_plot),
                            'label': os.path.basename(pca_plot),
                            'description': 'HTML summary report for PCA analysis app'
                            })

        objects_created = list()
        objects_created.append({'ref': pca_ref,
                                'description': 'PCA Matrix'})

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'objects_created': objects_created,
                         'html_links': html_report,
                         'direct_html_link_index': 0,
                         'html_window_height': 666,
                         'report_object_name': 'kb_pca_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _append_instance_group(self, plot_pca_matrix, obj_data, dimension):
        plot_pca_matrix = plot_pca_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            log('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_pca_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_pca_matrix['instance'] = plot_pca_matrix.index.map(attribute_mapping)

        return plot_pca_matrix

    def _build_size_pca_matrix(self, plot_pca_matrix, obj_data, dimension, attribute_name):
        """
        _build_size_pca_matrix: append attribute value to rotation_matrix
        """
        log('appending attribute value for sizing to rotation matrix')

        plot_pca_matrix = plot_pca_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
            attribute_mapping_ref = obj_data.get('row_attributemapping_ref')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
            attribute_mapping_ref = obj_data.get('col_attributemapping_ref')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            log('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_pca_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_pca_matrix['instance'] = plot_pca_matrix.index.map(attribute_mapping)

        res = self.dfu.get_objects({'object_refs': [attribute_mapping_ref]})['data'][0]
        attri_data = res['data']
        attri_name = res['info'][1]

        attributes = attri_data.get('attributes')

        attr_pos = None
        for idx, attribute in enumerate(attributes):
            if attribute.get('attribute') == attribute_name:
                attr_pos = idx
                break

        if attr_pos is None:
            raise ValueError('Cannot find attribute [{}] in [{}]'.format(attribute_name,
                                                                         attri_name))

        instances = attri_data.get('instances')

        plot_pca_matrix['attribute_value_size'] = None
        for instance_name, attri_values in instances.items():
            plot_pca_matrix.loc[plot_pca_matrix.instance == instance_name,
                                ['attribute_value_size']] = attri_values[attr_pos]

        return plot_pca_matrix

    def _build_color_pca_matrix(self, plot_pca_matrix, obj_data, dimension, attribute_name):
        """
        _build_color_pca_matrix: append attribute value to rotation_matrix
        """
        log('appending attribute value for grouping color to rotation matrix')

        plot_pca_matrix = plot_pca_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
            attribute_mapping_ref = obj_data.get('row_attributemapping_ref')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
            attribute_mapping_ref = obj_data.get('col_attributemapping_ref')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            log('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_pca_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_pca_matrix['instance'] = plot_pca_matrix.index.map(attribute_mapping)

        res = self.dfu.get_objects({'object_refs': [attribute_mapping_ref]})['data'][0]
        attri_data = res['data']
        attri_name = res['info'][1]

        attributes = attri_data.get('attributes')

        attr_pos = None
        for idx, attribute in enumerate(attributes):
            if attribute.get('attribute') == attribute_name:
                attr_pos = idx
                break

        if attr_pos is None:
            raise ValueError('Cannot find attribute [{}] in [{}]'.format(attribute_name,
                                                                         attri_name))

        instances = attri_data.get('instances')

        plot_pca_matrix['attribute_value_color'] = None
        for instance_name, attri_values in instances.items():
            plot_pca_matrix.loc[plot_pca_matrix.instance == instance_name,
                                ['attribute_value_color']] = attri_values[attr_pos]

        return plot_pca_matrix

    def _plot_pca_matrix(self, plot_pca_matrix):
        traces = []

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'pca_plot.html')

        if 'instance' not in plot_pca_matrix.columns:
            # no associated attribute mapping
            trace = go.Scatter(
                x=list(plot_pca_matrix.principal_component_1),
                y=list(plot_pca_matrix.principal_component_2),
                mode='markers',
                text=list(plot_pca_matrix.index),
                textposition='bottom center',
                marker=go.Marker(size=10, opacity=0.8,
                                 line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5)))
            traces.append(trace)
        else:
            if 'attribute_value_color' in plot_pca_matrix.columns and 'attribute_value_size' in plot_pca_matrix.columns:

                sizeref = 2.*float(max(plot_pca_matrix['attribute_value_size']))/(100**2)

                for name in set(plot_pca_matrix.attribute_value_color):
                    trace = go.Scatter(
                        x=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].principal_component_1),
                        y=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].principal_component_2),
                        mode='markers',
                        name=name,
                        text=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].index),
                        textposition='bottom center',
                        marker=go.Marker(symbol='circle', sizemode='area', sizeref=sizeref,
                                         size=list(map(float, plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].attribute_value_color)),
                                         line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5),
                                         opacity=0.8))
                    traces.append(trace)
            elif 'attribute_value_color' in plot_pca_matrix.columns:
                for name in set(plot_pca_matrix.attribute_value_color):
                    trace = go.Scatter(
                        x=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].principal_component_1),
                        y=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].principal_component_2),
                        mode='markers',
                        name=name,
                        text=list(plot_pca_matrix.loc[plot_pca_matrix['attribute_value_color'].eq(name)].index),
                        textposition='bottom center',
                        marker=go.Marker(size=10, opacity=0.8, line=go.Line(color='rgba(217, 217, 217, 0.14)',
                                                                            width=0.5)))
                    traces.append(trace)
            elif 'attribute_value_size' in plot_pca_matrix.columns:
                sizeref = 2.*float(max(plot_pca_matrix['attribute_value_size']))/(100**2)

                for name in set(plot_pca_matrix.instance):
                    trace = go.Scatter(
                        x=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].principal_component_1),
                        y=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].principal_component_2),
                        mode='markers',
                        name=name,
                        text=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].index),
                        textposition='bottom center',
                        marker=go.Marker(symbol='circle', sizemode='area', sizeref=sizeref,
                                         size=list(map(float, plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].attribute_value_size)),
                                         line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5),
                                         opacity=0.8))
                    traces.append(trace)
            else:
                for name in set(plot_pca_matrix.instance):
                    trace = go.Scatter(
                        x=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].principal_component_1),
                        y=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].principal_component_2),
                        mode='markers',
                        name=name,
                        text=list(plot_pca_matrix.loc[plot_pca_matrix['instance'].eq(name)].index),
                        textposition='bottom center',
                        marker=go.Marker(size=10, opacity=0.8, line=go.Line(color='rgba(217, 217, 217, 0.14)',
                                                                            width=0.5)))
                    traces.append(trace)

        data = go.Data(traces)
        layout = go.Layout(xaxis=go.XAxis(title='PC1', showline=False),
                           yaxis=go.YAxis(title='PC2', showline=False))
        fig = go.Figure(data=data, layout=layout)

        plot(fig, filename=result_file_path)

        return result_file_path

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']

        self.data_util = DataUtil(config)
        self.dfu = DataFileUtil(self.callback_url)

        plt.switch_backend('agg')

    def run_pca(self, params):
        """
        perform PCA analysis on matrix

        input_obj_ref: object reference of a matrix
        workspace_name: the name of the workspace
        pca_matrix_name: name of PCA (KBaseExperiments.PCAMatrix) object

        n_components - number of components (default 2)
        dimension: compute correlation on column or row, one of ['col', 'row']
        """

        log('--->\nrunning NetworkUtil.build_network\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_pca_params(params)

        input_obj_ref = params.get('input_obj_ref')
        workspace_name = params.get('workspace_name')
        pca_matrix_name = params.get('pca_matrix_name')

        n_components = int(params.get('n_components', 2))
        dimension = params.get('dimension', 'row')

        res = self.dfu.get_objects({'object_refs': [input_obj_ref]})['data'][0]
        obj_data = res['data']
        obj_type = res['info'][2]

        if "KBaseMatrices" in obj_type:
            (rotation_matrix_df,
             explained_variance_ratio) = self._pca_for_matrix(input_obj_ref, n_components,
                                                              dimension)
        else:
            err_msg = 'Ooops! [{}] is not supported.\n'.format(obj_type)
            err_msg += 'Please supply KBaseMatrices object'
            raise ValueError("err_msg")

        pca_ref = self._save_pca_matrix(workspace_name, input_obj_ref, pca_matrix_name,
                                        rotation_matrix_df, explained_variance_ratio,
                                        n_components, dimension)

        plot_pca_matrix = self._append_instance_group(rotation_matrix_df.copy(), obj_data,
                                                      dimension)

        if params.get('color_marker_by'):
            plot_pca_matrix = self._build_color_pca_matrix(
                                            plot_pca_matrix, obj_data, dimension,
                                            params.get('color_marker_by').get('attribute_color')[0])

        if params.get('scale_size_by'):
            plot_pca_matrix = self._build_size_pca_matrix(
                                            plot_pca_matrix, obj_data, dimension,
                                            params.get('scale_size_by').get('attribute_size')[0])

        returnVal = {'pca_ref': pca_ref}

        report_output = self._generate_pca_report(pca_ref, self._plot_pca_matrix(plot_pca_matrix),
                                                  workspace_name)

        returnVal.update(report_output)

        return returnVal

    def export_pca_matrix_excel(self, params):
        """
        export PCAMatrix as Excel
        """
        log('start exporting pca matrix')
        pca_matrix_ref = params.get('input_ref')

        pca_df = self._pca_to_df(pca_matrix_ref)

        result_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_dir)

        self._pca_df_to_excel(pca_df, result_dir, pca_matrix_ref)

        package_details = self.dfu.package_for_download({
            'file_path': result_dir,
            'ws_refs': [pca_matrix_ref]
        })

        return {'shock_id': package_details['shock_id']}
