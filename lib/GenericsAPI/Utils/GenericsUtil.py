import time
import json
import os
import re
import pandas as pd

from DataFileUtil.DataFileUtilClient import DataFileUtil
from biokbase.workspace.client import Workspace as workspaceService


def log(message, prefix_newline=False):
    print(('\n' if prefix_newline else '') + str(time.time()) + ': ' + message)

GENERICS_TYPE = ['FloatMatrix2D']  # add case in _convert_data for each additional type


class GenericsUtil:

    def _validate_fetch_data_params(self, params):
        """
        _validate_fetch_data_params:
            validates params passed to fetch_data method
        """

        log('start validating fetch_data params')

        # check for required parameters
        for p in ['obj_ref']:
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

    def _find_between(self, s, start, end):
        """
        _find_between: find string in between start and end
        """

        return re.search('{}(.*){}'.format(start, end), s).group(1)

    def _find_generics_type(self, obj_type):
        """
        _find_generics_type: try to find generics type in an object
        """

        log('Start finding generics type and name')

        obj_module = obj_type.split('.')[0]
        obj_type_name = self._find_between(obj_type, '\.', '\-')

        module_info = self.wsClient.get_module_info({'mod': obj_module})
        module_spec = module_info.get('spec')

        module_spec_list = module_spec.split(obj_type_name + ';')
        obj_type_spec = ''
        for module_spec in module_spec_list[:-1]:
            if module_spec.endswith((' ', '}')):
                obj_type_spec = module_spec.split('structure')[-1]
                break

        if not obj_type_spec:
            raise ValueError('Cannot retrieve spec for: {}'.format(obj_type))
        log('Found spec for {}\n{}\n'.format(obj_type, obj_type_spec))

        generics_type = [generics_type for generics_type in GENERICS_TYPE
                         if generics_type in obj_type_spec]

        if not generics_type:
            error_msg = 'Cannot find generics type in spec:\n{}\n'.format(obj_type_spec)
            raise ValueError(error_msg)
        elif len(generics_type) > 1:
            error_msg = 'More than 1 generics type found in spec:\n{}\n'.format(obj_type_spec)
            raise ValueError(error_msg)
        else:
            generics_type = generics_type[0]

        log('Found generics type: {}'.format(generics_type))

        generics_type_name = obj_type_spec.split(generics_type)[1].split(';')[0].strip()
        log('Found generics type name: {}'.format(generics_type_name))

        return generics_type, generics_type_name

    def _convert_data(self, data, data_type):
        """
        _convert_data: convert data to df based on data_type
        """

        if data_type == 'FloatMatrix2D':
            values = data['values']
            index = data['row_ids']
            columns = data['col_ids']
            df = pd.DataFrame(values, index=index, columns=columns)
        else:
            raise ValueError('Unknown generics data type: {}'.format(data_type))

        return df.to_json()

    def _retrieve_data(self, obj_ref, generics_type=None, generics_type_name=None):
        """
        _retrieve_data: retrieve object data and return a dataframe
        """
        log('Start retrieving data')
        obj_source = self.dfu.get_objects(
            {"object_refs": [obj_ref]})['data'][0]

        obj_info = obj_source.get('info')
        obj_data = obj_source.get('data')

        if not (generics_type and generics_type_name):
            generics_type, generics_type_name = self._find_generics_type(obj_info[2])

        try:
            data = obj_data[generics_type_name]
        except KeyError:
            raise ValueError('Retrieved wrong generics type name!')

        data_matrix = self._convert_data(data, generics_type)

        return data_matrix

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

        optional arguments:
        generics_type: the data type to be retrieved from
        generics_type_name: the name of the data type to be retrieved from
                            e.g. for an given data type like below:
                            typedef structure {
                              FloatMatrix2D data;
                            } SomeGenericsMatrix;
                            generics_type should be 'FloatMatrix2D'
                            generics_type_name should be 'data'

        return:
        data_matrix: a pandas dataframe in json format
        """

        log('--->\nrunning GenericsUtil.fetch_data\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_fetch_data_params(params)

        try:
            data_matrix = self._retrieve_data(params.get('obj_ref'),
                                              params.get('generics_type'),
                                              params.get('generics_type_name'))
        except Exception as e:
            error_msg = 'Running fetch_data returned an error:\n{}\n'.format(str(e))
            error_msg += 'Please try to specify generics type and name\n'
            raise ValueError(error_msg)

        returnVal = {'data_matrix': data_matrix}

        return returnVal
