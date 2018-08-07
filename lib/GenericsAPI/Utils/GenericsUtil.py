import time
import json
import os
import re
import pandas as pd
import uuid
import errno
import traceback
import xlsxwriter
from dotmap import DotMap
from xlrd.biffh import XLRDError
from openpyxl import load_workbook
import collections
import shutil

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as workspaceService
from ConditionUtils.ConditionUtilsClient import ConditionUtils
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    print(('\n' if prefix_newline else '') + str(time.time()) + ': ' + message)

GENERICS_TYPE = ['FloatMatrix2D']  # add case in _convert_data for each additional type
MATRIX_TYPE = ['ExpressionMatrix', 'FitnessMatrix', 'DifferentialExpressionMatrix']


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

    def _validate_import_matrix_from_excel_params(self, params):
        """
        _validate_import_matrix_from_excel_params:
            validates params passed to import_matrix_from_excel method
        """
        log('start validating import_matrix_from_excel params')

        # check for required parameters
        for p in ['obj_type', 'matrix_name', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        obj_type = params.get('obj_type')
        if obj_type not in MATRIX_TYPE:
            raise ValueError('Unknown matrix object type: {}'.format(obj_type))

        if params.get('input_file_path'):
            file_path = params.get('input_file_path')
        elif params.get('input_shock_id'):
            file_path = self.dfu.shock_to_file(
                {'shock_id': params['input_shock_id'],
                 'file_path': self.scratch}).get('file_path')
        elif params.get('input_staging_file_path'):
            file_path = self.dfu.download_staging_file(
                        {'staging_file_subdir_path': params.get('input_staging_file_path')}
                        ).get('copy_file_path')
        else:
            error_msg = "Must supply either a input_shock_id or input_file_path "
            error_msg += "or input_staging_file_path"
            raise ValueError(error_msg)

        refs_key = ['col_conditionset_ref', 'row_conditionset_ref', 'genome_ref',
                    'diff_expr_matrix_ref']
        refs = {k: v for k, v in params.items() if k in refs_key}

        return (obj_type, file_path, params.get('workspace_name'),
                params.get('matrix_name'), refs)

    def _upload_to_shock(self, file_path):
        """
        _upload_to_shock: upload target file to shock using DataFileUtil
        """
        log('Start uploading file to shock: {}'.format(file_path))

        file_to_shock_params = {
            'file_path': file_path,
            'pack': 'zip'
        }
        shock_id = self.dfu.file_to_shock(file_to_shock_params).get('shock_id')

        return shock_id

    def _upload_dir_to_shock(self, directory):
        """
        _upload_dir_to_shock: upload target dir to shock using DataFileUtil
        """
        log('Start uploading directory to shock: {}'.format(directory))

        file_to_shock_params = {
            'file_path': directory,
            'pack': 'zip'
        }
        shock_file = self.dfu.file_to_shock(file_to_shock_params)

        shock_id = shock_file.get('shock_id')

        return shock_id

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

    def _find_type_spec(self, obj_type):
        """
        _find_type_spec: find body spec of type
        """
        obj_type_name = self._find_between(obj_type, '\.', '\-')

        type_info = self.wsClient.get_type_info(obj_type)
        type_spec = type_info.get('spec_def')

        type_spec_list = type_spec.split(obj_type_name + ';')
        obj_type_spec = type_spec_list[0].split('structure')[-1]
        log('Found spec for {}\n{}\n'.format(obj_type, obj_type_spec))

        return obj_type_spec

    def _find_constraints(self, obj_type):
        """
        _find_constraints: retrieve constraints (@contains, rowsum, unique)
        """

        type_info = self.wsClient.get_type_info(obj_type)
        type_desc = type_info.get('description')

        constraints = {'contains': [], 'rowsum': [], 'unique': []}

        unique = [item.split('\n')[0].strip() for item in type_desc.split('@unique')[1:]]
        constraints['unique'] = unique

        contains = [item.split('\n')[0].strip() for item in type_desc.split('@contains')[1:]]
        constraints['contains'] = contains

        return constraints

    def _find_generics_type(self, obj_type):
        """
        _find_generics_type: try to find generics type in an object
        """

        log('Start finding generics type and name')

        obj_type_spec = self._find_type_spec(obj_type)

        if not obj_type_spec:
            raise ValueError('Cannot retrieve spec for: {}'.format(obj_type))

        generics_types = [generics_type for generics_type in GENERICS_TYPE
                          if generics_type in obj_type_spec]

        if not generics_types:
            error_msg = 'Cannot find generics type in spec:\n{}\n'.format(obj_type_spec)
            raise ValueError(error_msg)

        generics_module = dict()
        for generics_type in generics_types:
            for item in obj_type_spec.split(generics_type)[1:]:
                generics_type_name = item.split(';')[0].strip()
                generics_module.update({generics_type_name: generics_type})

        log('Found generics type:\n{}\n'.format(generics_module))

        return generics_module

    def _convert_data(self, data, generics_module):
        """
        _convert_data: convert data to df based on data_type
        """

        data_types = generics_module.values()

        if not set(GENERICS_TYPE) >= set(data_types):
            raise ValueError('Found unknown generics data type in:\n{}\n'.format(data_types))

        if data_types == ['FloatMatrix2D']:
            key = generics_module.keys()[generics_module.values().index('FloatMatrix2D')]
            values = data[key]['values']
            index = data[key]['row_ids']
            columns = data[key]['col_ids']
            df = pd.DataFrame(values, index=index, columns=columns)
        # elif 'FloatMatrix2D' in data_types:  # default case
        #     key = generics_module.keys()[generics_module.values().index('FloatMatrix2D')]
        #     values = data[key]['values']
        #     index = data[key]['row_ids']
        #     columns = data[key]['col_ids']
        #     df = pd.DataFrame(values, index=index, columns=columns)
        else:
            raise ValueError('Unexpected Error')

        return df.to_json()

    def _retrieve_data(self, obj_ref, generics_module=None):
        """
        _retrieve_data: retrieve object data and return a dataframe in json format
        """
        log('Start retrieving data')
        obj_source = self.dfu.get_objects(
            {"object_refs": [obj_ref]})['data'][0]

        obj_info = obj_source.get('info')
        obj_data = obj_source.get('data')

        if not generics_module:
            generics_module = self._find_generics_type(obj_info[2])

        try:
            data = {k: v for k, v in obj_data.items() if k in generics_module.keys()}
        except KeyError:
            raise ValueError('Retrieved wrong generics type name')

        data_matrix = self._convert_data(data, generics_module)

        return data_matrix

    def _get_col_cond_list(self, col_mapping, col_conditionset_ref, cols):
        """
        _get_col_cond_list: generate col condition list for excel
        """
        col_cond_list = []

        conditionset_data = self.dfu.get_objects(
                        {"object_refs": [col_conditionset_ref]})['data'][0]['data']
        col_condition_names = [factor.get('factor') for factor in conditionset_data.get('factors')]
        for col in cols:
            condition_id = col_mapping.get(col)
            if condition_id:
                col_cond_list.append(conditionset_data.get('conditions').get(condition_id))
            else:
                col_cond_list.append(['']*len(col_condition_names))

        col_cond_list = map(list, zip(*col_cond_list))
        for idx, col_array in enumerate(col_cond_list):
            col_array.insert(0, col_condition_names[idx])

        return col_cond_list

    def _get_row_cond_list(self, row_mapping, row_conditionset_ref, rows):
        """
        _get_row_cond_list: generate row condition list for excel
        """
        row_cond_list = []

        conditionset_data = self.dfu.get_objects(
                        {"object_refs": [row_conditionset_ref]})['data'][0]['data']
        row_condition_names = [factor.get('factor') for factor in conditionset_data.get('factors')]

        row_cond_list.append(row_condition_names)

        for row in rows:
            condition_id = row_mapping.get(row)
            if condition_id:
                row_cond_list.append(conditionset_data.get('conditions').get(condition_id))
            else:
                row_cond_list.append(['']*len(row_condition_names))

        return row_cond_list

    def _get_data_list(self, cols, rows, values):
        """
        _get_data_list: generate data value list for excel
        """
        data_arrays = []
        cols.insert(0, '')
        data_arrays.append(cols)
        for idx, row in enumerate(rows):
            values[idx].insert(0, row)
        data_arrays += values

        return data_arrays

    def _merge_cond_list(self, excel_list, col_cond_list, row_cond_list):
        """
        _merge_cond_list: merge lists for excel
        """
        col_cond_len = len(col_cond_list)
        for item in excel_list[:col_cond_len]:
            row_len = len(row_cond_list[0]) if row_cond_list else 0
            item[0:0] = [''] * row_len

        if row_cond_list:
            for idx, item in enumerate(excel_list[col_cond_len:]):
                item[0:0] = row_cond_list[idx]

    def _is_number(s):
        """
        _is_number: string is a numeric
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        return False

    def _gen_excel(self, excel_list, obj_name):
        """
        _gen_excel: create excel
        """

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        file_path = os.path.join(result_directory, '{}.xlsx'.format(obj_name))

        log('Start writing to file: {}'.format(file_path))

        workbook = xlsxwriter.Workbook(file_path, {'nan_inf_to_errors': True})
        worksheet = workbook.add_worksheet()

        row = 1
        for data_entry in excel_list:
            for idx, cell_data in enumerate(data_entry):
                worksheet.write(row, idx, cell_data)

            row += 1

        workbook.close()

        return file_path

    def _write_mapping_sheet(self, file_path, sheet_name, mapping, index):
        """
        _write_mapping_sheet: write mapping to sheet
        """
        df_dict = collections.OrderedDict()

        df_dict[index[0]] = []
        df_dict[index[1]] = []

        for key, value in mapping.items():
            df_dict.get(index[0]).append(key)
            df_dict.get(index[1]).append(value)

        df = pd.DataFrame.from_dict(df_dict)

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            writer.book = load_workbook(file_path)
            df.to_excel(writer, sheet_name=sheet_name)

    def _retrieve_value(self, data, value):
        log('Getting value for {}'.format(value))
        retrieve_data = []
        m_data = DotMap(data)
        if value.startswith('values'):  # TODO: nested values e.g. values(values(ids))
            search_value = re.search('{}(.*){}'.format('\(', '\)'), value).group(1)
            unique_list = search_value.split('.')
            m_data_cp = m_data.copy()
            for attr in unique_list:
                m_data_cp = getattr(m_data_cp, attr)
            retrieve_data = m_data_cp.values()
        elif ':' in value:
            obj_ref = getattr(m_data, value.split(':')[0])
            if obj_ref:
                included = value.split(':')[1]
                included = '/' + included.replace('.', '/')
                ref_data = self.wsClient.get_objects2({'objects': [{'ref': obj_ref,
                                                       'included': [included]}]})['data'][0]['data']
                m_ref_data = DotMap(ref_data)
                if ref_data:
                    if '*' not in included:
                        for key in included.split('/')[1:]:
                            m_ref_data = getattr(m_ref_data, key)
                    else:
                        keys = included.split('/')[1:]
                        m_ref_data = [x.get(keys[2]) for x in ref_data.get(keys[0])]  # TODO: only works for 2 level nested data like '/features/[*]/id'

                retrieve_data = list(m_ref_data)
        else:
            unique_list = value.split('.')
            m_data_cp = m_data.copy()
            for attr in unique_list:
                m_data_cp = getattr(m_data_cp, attr)
            retrieve_data = list(m_data_cp)

        log('Retrieved value (first 20):\n{}\n'.format(retrieve_data[:20]))

        return retrieve_data

    def _generate_report(self, matrix_obj_ref, workspace_name):
        """
        _generate_report: generate summary report
        """

        report_params = {'message': '',
                         'objects_created': [{'ref': matrix_obj_ref,
                                              'description': 'Imported Matrix'}],
                         'workspace_name': workspace_name,
                         'report_object_name': 'import_matrix_from_excel_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _validate(self, constraints, data):
        """
        _validate: validate data
        """

        validated = True
        failed_constraints = {'contains': [], 'rowsum': [], 'unique': []}

        unique_constraints = constraints.get('unique')
        for unique_constraint in unique_constraints:
            retrieved_value = self._retrieve_value(data, unique_constraint)
            if len(set(retrieved_value)) != len(retrieved_value):
                validated = False
                failed_constraints['unique'].append(unique_constraint)

        contains_constraints = constraints.get('contains')
        for contains_constraint in contains_constraints:
            value = contains_constraint.split(' ')[0]
            in_values = contains_constraint.split(' ')[1:]
            retrieved_in_values = []
            for in_value in in_values:
                retrieved_in_values += self._retrieve_value(data, in_value)
            if not (set(self._retrieve_value(data, value)) <= set(retrieved_in_values)):
                validated = False
                failed_constraints['contains'].append(contains_constraint)

        return validated, failed_constraints

    def _process_mapping_sheet(self, file_path, sheet_name):
        """
        _process_mapping: process mapping sheet
        """

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        except XLRDError:
            return dict()
        else:
            mapping = {value[0]: value[1] for value in df.values.tolist()}

        return mapping

    def _process_conditionset_sheet(self, file_path, sheet_name, matrix_name, workspace_id):
        """
        _process_conditionset_sheet: process condition set sheet
        """

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        except XLRDError:
            return ''
        else:
            obj_name = '{}_{}'.format(sheet_name, matrix_name)
            result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
            self._mkdir_p(result_directory)
            file_path = os.path.join(result_directory, '{}.xlsx'.format(obj_name))
            df.to_excel(file_path)
            import_condition_set_params = {
                'output_obj_name': obj_name,
                'output_ws_id': workspace_id,
                'input_file_path': file_path
            }

            ref = self.cu.file_to_condition_set(import_condition_set_params)

            return ref.get('condition_set_ref')

    def _file_to_data(self, file_path, refs, matrix_name, workspace_id):
        log('Start reading and converting excel file data')
        data = refs

        try:
            pd.read_excel(file_path)
        except XLRDError:
            # TODO: convert csv file to excel
            log('Found csv file')
            raise ValueError('Please provide .xlsx file only')

        # processing data sheet
        try:
            df = pd.read_excel(file_path, sheet_name='data')
        except XLRDError:
            raise ValueError('Cannot find <data> sheetss')
        else:
            matrix_data = {'row_ids': df.index.tolist(),
                           'col_ids': df.columns.tolist(),
                           'values': df.values.tolist()}
            data.update({'data': matrix_data})

        # processing col/row_mapping
        col_mapping = self._process_mapping_sheet(file_path, 'col_mapping')
        data.update({'col_mapping': col_mapping})

        row_mapping = self._process_mapping_sheet(file_path, 'row_mapping')
        data.update({'row_mapping': row_mapping})

        # processing col/row_conditionset
        col_conditionset_ref = self._process_conditionset_sheet(file_path,
                                                                'col_conditionset',
                                                                matrix_name,
                                                                workspace_id)
        data.update({'col_conditionset_ref': col_conditionset_ref})

        row_conditionset_ref = self._process_conditionset_sheet(file_path,
                                                                'row_conditionset',
                                                                matrix_name,
                                                                workspace_id)
        data.update({'row_conditionset_ref': row_conditionset_ref})

        # processing metadata
        metadata = self._process_mapping_sheet(file_path, 'metadata')
        data.update(metadata)

        return data

    def _build_header_str(self, factor_names):

        header_str = ''

        header_str += '<tr class="header">'
        header_str += '<th style="width:40%;">Feature ID</th>'

        for factor_name in factor_names:
            header_str += '<th style="width:40%;">{}</th>'.format(factor_name)
        header_str += '</tr>'

        return header_str

    def _build_html_str(self, row_mapping, conditions):

        log('Start building html replacement')

        factor_names = [x.get('factor') for x in conditions[conditions.keys()[0]].values()[0]]

        factor_names += [x[0].get('factor') for x in conditions[conditions.keys()[0]].values()]

        factor_names = list(set(factor_names))

        header_str = self._build_header_str(factor_names)

        table_str = ''

        for feature_id, factor_id in row_mapping.items():
            condition = conditions.get(factor_id)
            condition_values = [None] * len(factor_names)

            for condition_info in condition.values():
                factor_name = condition_info[0].get('factor')
                idx = factor_names.index(factor_name)
                condition_values[idx] = condition_info[0].get('value')

            table_str += '<tr>'
            table_str += '<td>{}</td>'.format(feature_id)

            for condition_value in condition_values:
                table_str += '<td>{}</td>'.format(condition_value)
            table_str += '</tr>'

        return header_str, table_str

    def _generate_search_html_report(self, header_str, table_str):

        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'search.html')

        shutil.copy2(os.path.join(os.path.dirname(__file__), 'kbase_icon.png'),
                     output_directory)
        shutil.copy2(os.path.join(os.path.dirname(__file__), 'search_icon.png'),
                     output_directory)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'search_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('//HEADER_STR', header_str)
                report_template = report_template.replace('//TABLE_STR', table_str)
                result_file.write(report_template)

        html_report.append({'path': result_file_path,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for StringTie App'})

        return html_report

    def _generate_search_report(self, header_str, table_str, workspace_name):
        log('Start creating report')

        output_html_files = self._generate_search_html_report(header_str, table_str)

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 366,
                         'report_object_name': 'kb_matrix_filter_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)
        self.wsClient = workspaceService(self.ws_url, token=self.token)
        self.cu = ConditionUtils(self.callback_url, service_ver="dev")

    def matrix_filter(self, params):
        """
        matrix_filter: generate a HTML report that allows users to fitler feature ids

        arguments:
        matrix_obj_ref: object reference of a matrix
        workspace_name: workspace name
        """

        matrix_obj_ref = params.get('matrix_obj_ref')
        workspace_name = params.get('workspace_name')

        matrix_source = self.dfu.get_objects(
            {"object_refs": [matrix_obj_ref]})['data'][0]
        matrix_data = matrix_source.get('data')

        row_mapping = matrix_data.get('row_mapping')
        row_conditionset_ref = matrix_data.get('row_conditionset_ref')

        if not (row_mapping and row_conditionset_ref):
            raise ValueError('Matrix obejct is missing either row_mapping or row_conditionset_ref')

        conditions = self.cu.get_conditions({'condition_set_ref': row_conditionset_ref})

        header_str, table_str = self._build_html_str(row_mapping, conditions.get('conditions'))

        returnVal = self._generate_search_report(header_str, table_str, workspace_name)

        return returnVal

    def import_matrix_from_excel(self, params):
        """
        import_matrix_from_excel: import matrix object from excel

        arguments:
        obj_type: one of ExpressionMatrix, FitnessMatrix, DifferentialExpressionMatrix
        matrix_name: matrix object name
        workspace_name: workspace name matrix object to be saved to
        input_shock_id: file shock id
        or
        input_file_path: absolute file path
        or
        input_staging_file_path: staging area file path

        optional arguments:
        col_conditionset_ref: column ConditionSet reference
        row_conditionset_ref: row ConditionSet reference
        genome_ref: genome reference
        diff_expr_matrix_ref: DifferentialExpressionMatrix reference
        """

        (obj_type, file_path, workspace_name,
         matrix_name, refs) = self._validate_import_matrix_from_excel_params(params)

        if not isinstance(workspace_name, int):
            workspace_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            workspace_id = workspace_name

        data = self._file_to_data(file_path, refs, matrix_name, workspace_id)

        matrix_obj_ref = self.save_object({'obj_type': 'KBaseMatrices.{}'.format(obj_type),
                                           'obj_name': matrix_name,
                                           'data': data,
                                           'workspace_name': workspace_id})['obj_ref']

        returnVal = {'matrix_obj_ref': matrix_obj_ref}

        report_output = self._generate_report(matrix_obj_ref, workspace_name)

        returnVal.update(report_output)

        return returnVal

    def save_object(self, params):
        """
        save_object: validate data constraints and save matrix object

        arguments:
        obj_type: saving object data type
        obj_name: saving object name
        data: data to be saved
        workspace_name: workspace name matrix object to be saved to

        return:
        obj_ref: object reference
        """
        log('Starting saving object')

        obj_type = params.get('obj_type')

        module_name = obj_type.split('.')[0]
        type_name = obj_type.split('.')[1]

        types = self.wsClient.get_module_info({'mod': module_name}).get('types')

        for module_type in types:
            if self._find_between(module_type, '\.', '\-') == type_name:
                obj_type = module_type
                break

        data = dict((k, v) for k, v in params.get('data').iteritems() if v)
        validate = self.validate_data({'obj_type': obj_type,
                                       'data': data})

        if not validate.get('validated'):
            log('Data failed type checking')
            failed_constraints = validate.get('failed_constraints')
            error_msg = 'Object {} failed type checking:\n'.format(params.get('obj_name'))
            if failed_constraints.get('unique'):
                unique_values = failed_constraints.get('unique')
                error_msg += 'Object should have unique field: {}\n'.format(unique_values)
            if failed_constraints.get('contains'):
                contained_values = failed_constraints.get('contains')
                for contained_value in contained_values:
                    subset_value = contained_value.split(' ')[0]
                    super_value = ' '.join(contained_value.split(' ')[1:])
                    error_msg += 'Object field [{}] should contain field [{}]\n'.format(
                                                                                    super_value,
                                                                                    subset_value)
            raise ValueError(error_msg)

        workspace_name = params.get('workspace_name')
        if not isinstance(workspace_name, int):
            ws_name_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            ws_name_id = workspace_name

        info = self.dfu.save_objects({
            "id": ws_name_id,
            "objects": [{
                "type": obj_type,
                "data": data,
                "name": params.get('obj_name')
            }]
        })[0]

        return {"obj_ref": "%s/%s/%s" % (info[6], info[0], info[4])}

    def validate_data(self, params):
        """
        validate_data: validate data

        arguments:
        obj_type: obj type e.g.: 'KBaseMatrices.ExpressionMatrix-1.1'
        data: obj data to be validated

        return:
        validated: True or False
        """

        constraints = self._find_constraints(params.get('obj_type'))
        data = params.get('data')

        validated, failed_constraints = self._validate(constraints, data)

        returnVal = {'validated': validated,
                     'failed_constraints': failed_constraints}

        return returnVal

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
        generics_module: the generics data module to be retrieved from
                        e.g. for an given data type like below:
                        typedef structure {
                          FloatMatrix2D data;
                          condition_set_ref condition_set_ref;
                        } SomeGenericsMatrix;
                        generics_module should be
                        {'data': 'FloatMatrix2D',
                         'condition_set_ref': 'condition_set_ref'}

        return:
        data_matrix: a pandas dataframe in json format
        """

        log('--->\nrunning GenericsUtil.fetch_data\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_fetch_data_params(params)

        try:
            data_matrix = self._retrieve_data(params.get('obj_ref'),
                                              params.get('generics_module'))
        except Exception:
            error_msg = 'Running fetch_data returned an error:\n{}\n'.format(
                                                                traceback.format_exc())
            error_msg += 'Please try to specify generics type and name as generics_module\n'
            raise ValueError(error_msg)

        returnVal = {'data_matrix': data_matrix}

        return returnVal

    def export_matrix(self, params):
        """
        export_matrix: univeral downloader for matrix data object

        arguments:
        obj_ref: generics object reference

        optional arguments:
        generics_module: select the generics data to be retrieved from
                        e.g. for an given data type like below:
                        typedef structure {
                          FloatMatrix2D data;
                          condition_set_ref condition_set_ref;
                        } SomeGenericsMatrix;
                        and only data is needed
                        generics_module should be
                        {'data': 'FloatMatrix2D'}
        """
        log('Start exporting matrix')

        if 'input_ref' in params:
            params['obj_ref'] = params.pop('input_ref')

        obj_source = self.dfu.get_objects(
            {"object_refs": [params.get('obj_ref')]})['data'][0]
        obj_data = obj_source.get('data')

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        file_path = os.path.join(result_directory, '{}.xlsx'.format(obj_source.get('info')[1]))

        data_matrix = self.fetch_data(params).get('data_matrix')
        df = pd.read_json(data_matrix)

        df.to_excel(file_path, sheet_name='data')

        if obj_data.get('col_mapping'):
            self._write_mapping_sheet(file_path, 'col_mapping',
                                      obj_data.get('col_mapping'), ['col_name', 'condition_name'])
            obj_data.pop('col_mapping')

        if obj_data.get('row_mapping'):
            self._write_mapping_sheet(file_path, 'row_mapping',
                                      obj_data.get('row_mapping'), ['row_name', 'condition_name'])
            obj_data.pop('row_mapping')

        try:
            obj_data.pop('data')
        except KeyError:
            log('Missing key [data]')

        self._write_mapping_sheet(file_path, 'metadata', obj_data, ['name', 'value'])

        shock_id = self._upload_to_shock(file_path)

        return {'shock_id': shock_id}
