import errno
import itertools
import json
import logging
import os
import shutil
import sys
import uuid

import pandas as pd
import numpy as np
import plotly.graph_objs as go
from matplotlib import pyplot as plt
from plotly.offline import plot
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler
from skbio.stats.distance import DistanceMatrix

from installed_clients.DataFileUtilClient import DataFileUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from installed_clients.KBaseReportClient import KBaseReport


class MDSUtil:

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

    def _validate_run_mds_params(self, params):
        """
        _validate_run_mds_params:
            validates params passed to run_mds method
        """

        logging.info('start validating run_mds params')

        # check for required parameters
        for p in ['input_obj_ref', 'workspace_name', 'mds_matrix_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _df_to_list(self, df):
        """
        _df_to_list: convert Dataframe to FloatMatrix2D matrix data
        """

        df.index = df.index.astype('str')
        df.columns = df.columns.astype('str')
        df.fillna(0, inplace=True)
        matrix_data = {'row_ids': df.index.tolist(),
                       'col_ids': df.columns.tolist(),
                       'values': df.values.tolist()}

        return matrix_data

    def _mds_df_to_excel(self, mds_df, bcd_df, result_dir, mds_matrix_ref):
        """
        write MDS matrix df into excel
        """
        logging.info('writting mds data frame to excel file')
        mds_matrix_obj = self.dfu.get_objects({'object_refs': [mds_matrix_ref]})['data'][0]
        mds_matrix_info = mds_matrix_obj['info']
        mds_matrix_name = mds_matrix_info[1]

        file_path = os.path.join(result_dir, mds_matrix_name + ".xlsx")
        writer = pd.ExcelWriter(file_path)

        mds_df.to_excel(writer, "mds_matrix", index=True)
        if bcd_df:
            bcd_df.to_excel(writer, "mds_bcd_matrix", index=True)

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

    def _mds_to_df(self, mds_matrix_ref):
        """
        retrieve MDS matrix ws object to mds_df
        """
        logging.info('converting mds matrix to data frame')
        mds_data = self.dfu.get_objects({'object_refs': [mds_matrix_ref]})['data'][0]['data']

        rotation_matrix_data = mds_data.get('rotation_matrix')
        components_matrix_data = mds_data.get('components_matrix')

        explained_variance = mds_data.get('explained_variance')
        explained_variance_ratio = mds_data.get('explained_variance_ratio')
        singular_values = mds_data.get('singular_values')
        dimension = mds_data.get('mds_parameters').get('dimension')
        original_matrix_ref = mds_data.get('original_matrix_ref')

        mds_df = self._Matrix2D_to_df(rotation_matrix_data)
        components_df = None
        if components_matrix_data:
            components_df = self._Matrix2D_to_df(components_matrix_data)
            components_df.loc['explained_variance'] = explained_variance
            components_df.loc['explained_variance_ratio'] = explained_variance_ratio
            components_df.loc['singular_values'] = singular_values

        if original_matrix_ref:
            logging.info('appending instance group information to mds data frame')
            obj_data = self.dfu.get_objects({'object_refs': [original_matrix_ref]})['data'][0]['data']

            attributemapping_ref = obj_data.get('{}_attributemapping_ref'.format(dimension))

            am_data = self.dfu.get_objects({'object_refs': [attributemapping_ref]})['data'][0]['data']

            attributes = am_data.get('attributes')
            instances = am_data.get('instances')
            am_df = pd.DataFrame(data=list(instances.values()),
                                 columns=list(map(lambda x: x.get('attribute'), attributes)),
                                 index=instances.keys())

            mds_df = mds_df.merge(am_df, left_index=True, right_index=True, how='left',
                                  validate='one_to_one')

        return mds_df, components_df

    def _save_mds_matrix(self, workspace_name, input_obj_ref, mds_matrix_name, rotation_matrix_df,
                         components_df, explained_variance, explained_variance_ratio,
                         singular_values, n_components, dimension):

        logging.info('saving MDSMatrix')

        if not isinstance(workspace_name, int):
            ws_name_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            ws_name_id = workspace_name

        mds_data = {}

        mds_data.update({'rotation_matrix': self._df_to_list(rotation_matrix_df)})
        mds_data.update({'components_matrix': self._df_to_list(components_df)})
        mds_data.update({'explained_variance': explained_variance})
        mds_data.update({'explained_variance_ratio': explained_variance_ratio})
        mds_data.update({'singular_values': singular_values})
        mds_data.update({'mds_parameters': {'n_components': str(n_components),
                                            'dimension': str(dimension)}})
        mds_data.update({'original_matrix_ref': input_obj_ref})

        obj_type = 'KBaseExperiments.MDSMatrix'
        info = self.dfu.save_objects({
            "id": ws_name_id,
            "objects": [{
                "type": obj_type,
                "data": mds_data,
                "name": mds_matrix_name
            }]
        })[0]

        return "%s/%s/%s" % (info[6], info[0], info[4])

    def _bray_curtis_distance(self, df_table, sample1_id, sample2_id):
        """
        _bray_curtis_distance: calculate the bray_curtis_distance between two columns of a table
        :param df_table: a Pandas.DataFrame
        :sample1_id, sample2_id: the sample ids to calculate BC-distance between df_table[sample1_id]
                                 and df_table[sample2_id]
        """
        numerator = 0
        denominator = 0
        sample1_counts = df_table[sample1_id]
        sample2_counts = df_table[sample2_id]
        for sample1_count, sample2_count in zip(sample1_counts, sample2_counts):
            numerator += abs(sample1_count - sample2_count)
            denominator += sample1_count + sample2_count
        return numerator / denominator

    def _df_to_distance_matrix(self, df_table, pairwise_distance_fn):
        """
        _df_to_distances: computes pairwise distances between ALL pairs of samples to
                          get a square distance matrix of order n, where n equals to the number of
                          rows of the input table (i.e., df_table)
        :param df_table: a Pandas.DataFrame (or table)
        :param pairwise_distance_fn: function that calculates pairwise distances between df_table's samples
        """
        sample_ids = df_table.columns
        num_samples = len(sample_ids)
        data = np.zeros((num_samples, num_samples))
        for i, sample1_id in enumerate(sample_ids):
            for j, sample2_id in enumerate(sample_ids[:i]):
                data[i, j] = data[j, i] = pairwise_distance_fn(df_table, sample1_id, sample2_id)
        return DistanceMatrix(data, sample_ids)

    def _mds_project_clusters(self, input_obj_ref, n_components, dimension='row', metrics=False):
        """
        _mds_for_matrix: perform MDS analysis for matrix object
        :param input_obj_ref: KBase object reference to a data matrix
        :param n_components: int, dimentionality of the reduced space
        :param dimension: string, "col" or "row" indicating the data dimension mds is analyze on
        :param metrics: boolean, metrics=False indicating the nonmetric multidimensional scaling
        """
        data_matrix = self.data_util.fetch_data({'obj_ref': input_obj_ref}).get('data_matrix')

        data_df = pd.read_json(data_matrix)
        data_df.fillna(0, inplace=True)

        if dimension == 'col':
            data_df = data_df.T
        elif dimension != 'row':
            err_msg = 'Input dimension [{}] is not available.\n'.format(dimension)
            err_msg += 'Please choose either "col" or "row"'
            raise ValueError(err_msg)

        if n_components > data_df.index.size:
            raise ValueError('Number of components should be less than n_samples')

        # normalize sample
        # logging.info("Standardizing the matrix")
        # s_values = StandardScaler().fit_transform(data_df.values)
        # skip normalizing sample
        s_values = data_df.values

        # calcuate the distance matrix
        distance_mat = self._df_to_distance_matrix(s_values, self._bray_curtis_distance)

        # Projection
        seed = np.random.RandomState(seed=3)
        mds = MDS(n_components=n_components, max_iter=3000, eps=1e-9, random_state=seed,
                  dissimilarity="precomputed", n_jobs=1)
        pos = mds.fit(distance_mat).embedding_
        nmds = MDS(n_components=n_components, metric=False, max_iter=3000, eps=1e-12,
                   dissimilarity="precomputed", random_state=seed, n_jobs=1, n_init=1)
        npos = nmds.fit_transform(distance_mat, init=pos)

        return npos

    def _generate_mds_html_report(self, mds_plots, n_components):

        logging.info('start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'mds_report.html')

        visualization_content = ''

        for mds_plot in mds_plots:
            shutil.copy2(mds_plot,
                         os.path.join(output_directory, os.path.basename(mds_plot)))
            visualization_content += '<iframe height="900px" width="100%" '
            visualization_content += 'src="{}" '.format(os.path.basename(mds_plot))
            visualization_content += 'style="border:none;"></iframe>\n<p></p>\n'

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'templates', 'mds_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Visualization_Content</p>',
                                                          visualization_content)
                report_template = report_template.replace('n_components',
                                                          '{} Components'.format(n_components))
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_directory,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for ExpressionMatrix Cluster App'
                            })
        return html_report

    def _generate_mds_report(self, mds_ref, mds_plots, workspace_name, n_components):
        logging.info('creating report')

        output_html_files = self._generate_mds_html_report(mds_plots, n_components)

        objects_created = list()
        objects_created.append({'ref': mds_ref,
                                'description': 'MDS Matrix'})

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'objects_created': objects_created,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 666,
                         'report_object_name': 'kb_mds_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _append_instance_group(self, plot_mds_matrix, obj_data, dimension):
        plot_mds_matrix = plot_mds_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            logging.warning('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_mds_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_mds_matrix['instance'] = plot_mds_matrix.index.map(attribute_mapping)

        return plot_mds_matrix

    def _build_size_mds_matrix(self, plot_mds_matrix, obj_data, dimension, attribute_name):
        """
        _build_size_mds_matrix: append attribute value to rotation_matrix
        """
        logging.info('appending attribute value for sizing to rotation matrix')

        plot_mds_matrix = plot_mds_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
            attribute_mapping_ref = obj_data.get('row_attributemapping_ref')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
            attribute_mapping_ref = obj_data.get('col_attributemapping_ref')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            logging.warning('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_mds_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_mds_matrix['instance'] = plot_mds_matrix.index.map(attribute_mapping)

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

        plot_mds_matrix['attribute_value_size'] = None
        for instance_name, attri_values in instances.items():
            plot_mds_matrix.loc[plot_mds_matrix.instance == instance_name,
                                ['attribute_value_size']] = attri_values[attr_pos]

        return plot_mds_matrix

    def _build_color_mds_matrix(self, plot_mds_matrix, obj_data, dimension, attribute_name):
        """
        _build_color_mds_matrix: append attribute value to rotation_matrix
        """
        logging.info('appending attribute value for grouping color to rotation matrix')

        plot_mds_matrix = plot_mds_matrix.copy()

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
            attribute_mapping_ref = obj_data.get('row_attributemapping_ref')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
            attribute_mapping_ref = obj_data.get('col_attributemapping_ref')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            logging.warning('Matrix object does not have {}_mapping attribute'.format(dimension))
            # build matrix with unify color and shape
            return plot_mds_matrix
        else:
            # append instance col mapping from row/col_mapping
            plot_mds_matrix['instance'] = plot_mds_matrix.index.map(attribute_mapping)

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

        plot_mds_matrix['attribute_value_color'] = None
        for instance_name, attri_values in instances.items():
            plot_mds_matrix.loc[plot_mds_matrix.instance == instance_name,
                                ['attribute_value_color']] = attri_values[attr_pos]

        return plot_mds_matrix

    def _build_2_comp_trace(self, plot_mds_matrix, components_x, components_y):

        traces = []

        if 'attribute_value_color' in plot_mds_matrix.columns and 'attribute_value_size' in plot_mds_matrix.columns:

            maximum_marker_size = 10
            sizeref = 2.*float(max(plot_mds_matrix['attribute_value_size']))/(maximum_marker_size**2)

            for name in set(plot_mds_matrix.attribute_value_color):
                attribute_value_size = plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)].attribute_value_size
                size_list = list(map(abs, list(map(float, attribute_value_size))))
                for idx, val in enumerate(size_list):
                    if val == 0:
                        size_list[idx] = sys.float_info.min
                trace = go.Scatter(
                    x=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)][components_x]),
                    y=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)][components_y]),
                    mode='markers',
                    name=name,
                    text=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)].index),
                    textposition='bottom center',
                    marker=go.Marker(symbol='circle', sizemode='area', sizeref=sizeref,
                                     size=size_list, sizemin=2,
                                     line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5),
                                     opacity=0.8))
                traces.append(trace)
        elif 'attribute_value_color' in plot_mds_matrix.columns:
            for name in set(plot_mds_matrix.attribute_value_color):
                trace = go.Scatter(
                    x=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)][components_x]),
                    y=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)][components_y]),
                    mode='markers',
                    name=name,
                    text=list(plot_mds_matrix.loc[plot_mds_matrix['attribute_value_color'].eq(name)].index),
                    textposition='bottom center',
                    marker=go.Marker(size=10, opacity=0.8, line=go.Line(color='rgba(217, 217, 217, 0.14)',
                                                                        width=0.5)))
                traces.append(trace)
        elif 'attribute_value_size' in plot_mds_matrix.columns:

            maximum_marker_size = 10
            sizeref = 2.*float(max(plot_mds_matrix['attribute_value_size']))/(maximum_marker_size**2)

            for name in set(plot_mds_matrix.instance):
                attribute_value_size = plot_mds_matrix.loc[plot_mds_matrix['instance'].eq(name)].attribute_value_size
                size_list = list(map(abs, list(map(float, attribute_value_size))))
                for idx, val in enumerate(size_list):
                    if val == 0:
                        size_list[idx] = sys.float_info.min
                trace = go.Scatter(
                    x=list(plot_mds_matrix.loc[plot_mds_matrix['instance'].eq(name)][components_x]),
                    y=list(plot_mds_matrix.loc[plot_mds_matrix['instance'].eq(name)][components_y]),
                    mode='markers',
                    name=name,
                    text=list(plot_mds_matrix.loc[plot_mds_matrix['instance'].eq(name)].index),
                    textposition='bottom center',
                    marker=go.Marker(symbol='circle', sizemode='area', sizeref=sizeref,
                                     size=size_list, sizemin=2,
                                     line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5),
                                     opacity=0.8))
                traces.append(trace)
        else:
            trace = go.Scatter(
                x=list(plot_mds_matrix[components_x]),
                y=list(plot_mds_matrix[components_y]),
                mode='markers',
                text=list(plot_mds_matrix.index),
                textposition='bottom center',
                marker=go.Marker(size=10, opacity=0.8,
                                 line=go.Line(color='rgba(217, 217, 217, 0.14)', width=0.5)))
            traces.append(trace)

        return traces

    def _plot_mds_matrix(self, plot_mds_matrix, n_components):

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_paths = []

        all_pairs = list(itertools.combinations(range(1, n_components+1), 2))

        for pair in all_pairs:
            first_component = pair[0]
            second_component = pair[1]
            result_file_path = os.path.join(output_directory, 'mds_plot_{}_{}.html'.format(
                                                                                first_component,
                                                                                second_component))

            traces = self._build_2_comp_trace(plot_mds_matrix,
                                              'principal_component_{}'.format(first_component),
                                              'principal_component_{}'.format(second_component))

            data = go.Data(traces)
            layout = go.Layout(xaxis=go.XAxis(title='PC{}'.format(first_component), showline=False),
                               yaxis=go.YAxis(title='PC{}'.format(second_component), showline=False))
            fig = go.Figure(data=data, layout=layout)

            plot(fig, filename=result_file_path)

            result_file_paths.append(result_file_path)

        return result_file_paths

    def _validate_mds_matrix(self, obj_data, dimension,
                             color_marker_by, scale_size_by):

        if dimension == 'row':
            attribute_mapping = obj_data.get('row_mapping')
        elif dimension == 'col':
            attribute_mapping = obj_data.get('col_mapping')
        else:
            raise ValueError('Unexpected dimension')

        if not attribute_mapping:
            if (color_marker_by and color_marker_by.get('attribute_color')[0]) or \
               (scale_size_by and scale_size_by.get('attribute_size')[0]):
                raise ValueError('Matrix object is not associated with any {} attribute mapping'.format(dimension))

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']

        self.data_util = DataUtil(config)
        self.dfu = DataFileUtil(self.callback_url)

        plt.switch_backend('agg')

    def run_mds(self, params):
        """
        run_mds: perform MDS analysis on matrix
        :param input_obj_ref: object reference of a matrix
        :param workspace_name: the name of the workspace
        :param mds_matrix_name: name of MDS (KBaseExperiments.MDSMatrix) object
        :param n_components - dimentionality of the reduced space (default 2)
        :param dimension: compute correlation on column or row, one of ['col', 'row']
        """

        logging.info('--->\nrunning NetworkUtil.build_network\n' +
                     'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_mds_params(params)

        input_obj_ref = params.get('input_obj_ref')
        workspace_name = params.get('workspace_name')
        mds_matrix_name = params.get('mds_matrix_name')

        n_components = int(params.get('n_components', 2))
        dimension = params.get('dimension', 'row')

        res = self.dfu.get_objects({'object_refs': [input_obj_ref]})['data'][0]
        obj_data = res['data']
        obj_type = res['info'][2]

        self._validate_mds_matrix(obj_data, dimension,
                                  params.get('color_marker_by'), params.get('scale_size_by'))

        if "KBaseMatrices" in obj_type:

            (rotation_matrix_df, components_df, explained_variance,
             explained_variance_ratio, singular_values) = self._project_clusters(input_obj_ref,
                                                                                 n_components,
                                                                                 dimension)
        else:
            err_msg = 'Ooops! [{}] is not supported.\n'.format(obj_type)
            err_msg += 'Please supply KBaseMatrices object'
            raise ValueError("err_msg")

        mds_ref = self._save_mds_matrix(workspace_name, input_obj_ref, mds_matrix_name,
                                        rotation_matrix_df, components_df, explained_variance,
                                        explained_variance_ratio, singular_values,
                                        n_components, dimension)

        plot_mds_matrix = self._append_instance_group(rotation_matrix_df.copy(), obj_data,
                                                      dimension)

        if params.get('color_marker_by'):
            plot_mds_matrix = self._build_color_mds_matrix(
                                            plot_mds_matrix, obj_data, dimension,
                                            params.get('color_marker_by').get('attribute_color')[0])

        if params.get('scale_size_by'):
            plot_mds_matrix = self._build_size_mds_matrix(
                                            plot_mds_matrix, obj_data, dimension,
                                            params.get('scale_size_by').get('attribute_size')[0])

        returnVal = {'mds_ref': mds_ref}

        report_output = self._generate_mds_report(mds_ref,
                                                  self._plot_mds_matrix(plot_mds_matrix,
                                                                        n_components),
                                                  workspace_name,
                                                  n_components)

        returnVal.update(report_output)

        return returnVal

    def export_mds_matrix_excel(self, params):
        """
        export MDSMatrix as Excel
        """
        logging.info('start exporting mds matrix')
        mds_matrix_ref = params.get('input_ref')

        mds_df, components_df = self._mds_to_df(mds_matrix_ref)

        result_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_dir)

        self._mds_df_to_excel(mds_df, components_df, result_dir, mds_matrix_ref)

        package_details = self.dfu.package_for_download({
            'file_path': result_dir,
            'ws_refs': [mds_matrix_ref]
        })

        return {'shock_id': package_details['shock_id']}
