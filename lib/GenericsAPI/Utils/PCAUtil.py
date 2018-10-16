import time
import pandas as pd
import os
import uuid
import errno
from matplotlib import pyplot as plt
import json
import shutil
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.plotly as py
import plotly.graph_objs as go

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

    def _save_pca_matrix(self, workspace_name, pca_matrix_name, rotation_matrix_df,
                         explained_variance_ratio, n_components):

        # if not isinstance(workspace_name, int):
        #     ws_name_id = self.dfu.ws_name_to_id(workspace_name)
        # else:
        #     ws_name_id = workspace_name

        # pca_data = {}

        # pca_data.update({'rotation_matrix_data': self._df_to_list(rotation_matrix_df)})
        # pca_data.update({'explained_variance_ratio': explained_variance_ratio})
        # pca_data.update({'pca_parameters': {'n_components': n_components}})

        # obj_type = 'KBaseExperiments.PCAMatrix'
        # info = self.dfu.save_objects({
        #     "id": ws_name_id,
        #     "objects": [{
        #         "type": obj_type,
        #         "data": pca_data,
        #         "name": pca_matrix_name
        #     }]
        # })[0]

        # return "%s/%s/%s" % (info[6], info[0], info[4])
        pca_ref = ''
        return pca_ref

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

    def _build_group_pca_matrix(self, plot_pca_matrix, obj_data, dimension,
                                customize_instance_group):
        """
        _build_group_pca_matrix: select and append group/color/shape col to rotation_matrix
        """
        plot_pca_matrix = plot_pca_matrix.copy

        print('fdsafdsa')
        print(obj_data)

        # if customize_instance_group:

        # else:

        return plot_pca_matrix

    def _plot_pca_matrix(self, rotation_matrix_df):
        pass

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
             explained_variance_ratio) = self._pca_for_matrix(input_obj_ref, n_components, dimension)
        else:
            err_msg = 'Ooops! [{}] is not supported.\n'.format(obj_type)
            err_msg += 'Please supply KBaseMatrices object'
            raise ValueError("err_msg")

        pca_ref = self._save_pca_matrix(workspace_name, pca_matrix_name,
                                        rotation_matrix_df, explained_variance_ratio,
                                        n_components)

        plot_pca_matrix = rotation_matrix_df.copy()
        # if params.get('customize_instance_group'):
        if True:
            plot_pca_matrix = self._build_group_pca_matrix(plot_pca_matrix, obj_data, dimension,
                                                           params.get('customize_instance_group'))

        if params.get('scale_size_by'):
            plot_pca_matrix = self._build_size_pca_matrix(plot_pca_matrix, obj_data, dimension,
                                                          params.get('scale_size_by').get('attribute'))

        # pca_plot = self._plot_pca_matrix(plot_pca_matrix)

        returnVal = {'pca_ref': pca_ref}

        return returnVal
