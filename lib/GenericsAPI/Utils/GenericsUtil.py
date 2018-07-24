import time
import json
import os

from DataFileUtil.DataFileUtilClient import DataFileUtil
from biokbase.workspace.client import Workspace as workspaceService


def log(message, prefix_newline=False):
    print(('\n' if prefix_newline else '') + str(time.time()) + ': ' + message)


class GenericsUtil:

    def _validate_fetch_data_params(self, params):
        """
        _validate_fetch_data_params:
            validates params passed to fetch_data method
        """

        log('start validating fetch_data params')

        # check for required parameters
        for p in ['obj_ref', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _generate_html_string(self, df):
        """
        _generate_html_string: generating a html string from df
        template used: https://developers.google.com/chart/interactive/docs/gallery/table
                       https://developers.google.com/chart/interactive/docs/reference#formatters
        """
        dtypes = df.dtypes
        columns = df.columns

        column_str = ''
        number_columns = []
        for idx, column in enumerate(columns):
            dtype = dtypes[idx].name
            if 'int' in dtype or 'float' in dtype:
                column_str += "data.addColumn('number', '{}')\n".format(column)
                number_columns.append(column)
            else:
                column_str += "data.addColumn('string', '{}')\n".format(column)

        data_str = "data.addRows({})".format(df.values.tolist())

        formatter_str = ''
        for number_column in number_columns:
            mean = round(df[number_column].mean(), 2)
            column_n = columns.tolist().index(number_column)
            formatter_str += "var formatter_{} = ".format(column_n)
            formatter_str += "new google.visualization.BarFormat({base: "
            formatter_str += str(mean)
            formatter_str += ", width: 120});\n"
            formatter_str += "formatter_{}.format(data, {});\n".format(column_n, column_n)

        return column_str, data_str, formatter_str

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)
        self.wsClient = workspaceService(self.ws_url)

    def generate_matrix_html(self, params):
        """
        generate_matrix_html: generate a html page for given data

        arguments:
        df: a pandas dataframe

        return:
        html_string: html as a string format
        """

        column_str, data_str, formatter_str = self._generate_html_string(params.get('df'))

        with open(os.path.join(os.path.dirname(__file__), 'matrix_page_template.html'),
                  'r') as matrix_page_template_file:
                html_string = matrix_page_template_file.read()
                html_string = html_string.replace('// ADD_COL', column_str)
                html_string = html_string.replace('// ADD_DATA', data_str)
                html_string = html_string.replace('// ADD_FORMATTER', formatter_str)

        returnVal = {'html_string': html_string}

        return returnVal

    def fetch_data(self, params):
        """
        fetch_data: fetch generics data as pandas dataframe for a generics data object

        arguments:
        obj_ref: generics object reference
        workspace_name: the name of the workspace

        optional arguments:
        target_data_field: the data field to be retrieved from.
                           fetch_data will try to auto find this field.
                            e.g. for an given data type like below:
                            typedef structure {
                              FloatMatrix2D data;
                            } SomeGenericsMatrix;
                            data should be the target data field.

        return:
        data_matrix: a pandas dataframe
        """

        log('--->\nrunning GenericsUtil.fetch_data\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_fetch_data_params(params)

        obj_ref = params.get('obj_ref')
        workspace_name = params.get('workspace_name')

        returnVal = dict()

        return returnVal
