import time
import os
import re
import pandas as pd
import uuid
import errno
from xlrd.biffh import XLRDError
from openpyxl import load_workbook
import collections
import shutil

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.AttributeUtils import AttributesUtil


def log(message, prefix_newline=False):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(('\n' if prefix_newline else '') + time_str + ': ' + message)


TYPE_ATTRIBUTES = {'description', 'scale', 'row_normalization', 'col_normalization'}
SCALE_TYPES = {'raw', 'ln', 'log2', 'log10'}


class MatrixUtil:

    def _validate_import_matrix_from_excel_params(self, params):
        """
        _validate_import_matrix_from_excel_params:
            validates params passed to import_matrix_from_excel method
        """
        log('start validating import_matrix_from_excel params')

        # check for required parameters
        for p in ['obj_type', 'matrix_name', 'workspace_name', 'scale']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        obj_type = params.get('obj_type')
        if obj_type not in self.matrix_types:
            raise ValueError('Unknown matrix object type: {}'.format(obj_type))

        scale = params.get('scale')
        if scale not in SCALE_TYPES:
            raise ValueError('Unknown scale type: {}'.format(scale))

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

        refs = {k: v for k, v in params.items() if "_ref" in k}

        return (obj_type, file_path, params.get('workspace_name'),
                params.get('matrix_name'), refs, scale)

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

    def _find_between(self, s, start, end):
        """
        _find_between: find string in between start and end
        """

        return re.search('{}(.*){}'.format(start, end), s).group(1)

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

    def _process_attribute_mapping_sheet(self, file_path, sheet_name, matrix_name, workspace_id):
        """
        _process_attribute_mapping_sheet: process attribute_mapping sheet
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
            import_attribute_mapping_params = {
                'output_obj_name': obj_name,
                'output_ws_id': workspace_id,
                'input_file_path': file_path
            }

            ref = self.attr_util.file_to_attribute_mapping(import_attribute_mapping_params)

            return ref.get('attribute_mapping_ref')

    def _file_to_data(self, file_path, refs, matrix_name, workspace_id):
        log('Start reading and converting excel file data')
        data = refs

        try:
            df = pd.read_excel(file_path, sheet_name='data')

        except XLRDError:
            try:
                df = pd.read_excel(file_path)
                print('WARNING: A sheet named "data" was not found in the attached file, '
                      'proceeding with the first sheet as the data sheet.')

            except XLRDError:
                df = pd.read_csv(file_path, index_col=0)

        df.fillna(0, inplace=True)
        matrix_data = {'row_ids': df.index.tolist(),
                       'col_ids': df.columns.tolist(),
                       'values': df.values.tolist()}

        data.update({'data': matrix_data})

        if refs.get('col_attributemapping_ref'):
            res = self.dfu.get_objects({'object_refs': [refs['col_attributemapping_ref']]})['data']
            attri_data = res[0]['data']
            instances = attri_data.get('instances')
            key_values = instances.keys()
            if key_values:
                col_mapping = {key: value for (key, value) in zip(key_values, key_values)}
                data.update({'col_mapping': col_mapping})
        else:
            col_mapping = self._process_mapping_sheet(file_path, 'col_mapping')
            data.update({'col_mapping': col_mapping})
            col_attributemapping_ref = self._process_attribute_mapping_sheet(
                                                                        file_path,
                                                                        'col_attribute_mapping',
                                                                        matrix_name,
                                                                        workspace_id)
            data.update({'col_attributemapping_ref': col_attributemapping_ref})

        if refs.get('row_attributemapping_ref'):
            res = self.dfu.get_objects({'object_refs': [refs['row_attributemapping_ref']]})['data']
            attri_data = res[0]['data']
            instances = attri_data.get('instances')
            key_values = instances.keys()
            if key_values:
                row_mapping = {key: value for (key, value) in zip(key_values, key_values)}
                data.update({'row_mapping': row_mapping})
        else:
            row_mapping = self._process_mapping_sheet(file_path, 'row_mapping')
            row_attributemapping_ref = self._process_attribute_mapping_sheet(
                                                                        file_path,
                                                                        'row_attribute_mapping',
                                                                        matrix_name,
                                                                        workspace_id)
            data.update({'row_mapping': row_mapping})
            data.update({'row_attributemapping_ref': row_attributemapping_ref})

        # processing metadata
        metadata = self._process_mapping_sheet(file_path, 'metadata')
        data['attributes'] = {}
        data['search_attributes'] = []
        for k, v in metadata.items():
            k = k.strip()
            v = v.strip()
            if k in TYPE_ATTRIBUTES:
                data[k] = v
            else:
                data['attributes'][k] = v
                data['search_attributes'].append(" | ".join((k, v)))

        return data

    def _build_header_str(self, attribute_names):

        header_str = ''
        width = 100.0/len(attribute_names)

        header_str += '<tr class="header">'
        header_str += '<th style="width:{0:.2f}%;">Feature ID</th>'.format(width)

        for attribute_name in attribute_names:
            header_str += '<th style="width:{0:.2f}%;"'.format(width)
            header_str += '>{}</th>'.format(attribute_name)
        header_str += '</tr>'

        return header_str

    def _build_html_str(self, row_mapping, attributemapping_data, row_ids):

        log('Start building html replacement')

        attribute_names = [attributes.get('attribute') for attributes in attributemapping_data.get('attributes')]

        header_str = self._build_header_str(attribute_names)

        table_str = ''

        instances = attributemapping_data.get('instances')

        for feature_id, attribute_id in row_mapping.items():
            if feature_id in row_ids:
                feature_instances = instances.get(attribute_id)

                table_str += '<tr>'
                table_str += '<td>{}</td>'.format(feature_id)

                for feature_instance in feature_instances:
                    table_str += '<td>{}</td>'.format(feature_instance)
                table_str += '</tr>'

        return header_str, table_str

    def _generate_search_html_report(self, header_str, table_str):

        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'search.html')

        shutil.copy2(os.path.join(os.path.dirname(__file__), 'templates', 'kbase_icon.png'),
                     output_directory)
        shutil.copy2(os.path.join(os.path.dirname(__file__), 'templates', 'search_icon.png'),
                     output_directory)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'templates', 'search_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('//HEADER_STR', header_str)
                report_template = report_template.replace('//TABLE_STR', table_str)
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_directory,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Search Matrix App'})

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

    @staticmethod
    def _filter_value_data(value_data, filter_ids):
        """Filters a value matrix based on column or row ids"""
        def _norm_id(_id):
            return _id.replace(" ", "_")

        val_df = pd.DataFrame(value_data['values'], index=value_data['row_ids'],
                              columns=value_data['col_ids'], dtype='object')

        if filter_ids[0] in val_df.index:
            filtered_df = val_df.filter(filter_ids, axis=0)

        elif _norm_id(filter_ids[0]) in val_df.index:
            filtered_df = val_df.filter([_norm_id(x) for x in filter_ids], axis=0)

        elif filter_ids[0] in val_df.columns:
            filtered_df = val_df.filter(filter_ids)

        elif _norm_id(filter_ids[0]) in val_df.columns:
            filtered_df = val_df.filter([_norm_id(x) for x in filter_ids])

        else:
            raise ValueError("Unable to match {} to a row or column ID in this matrix"
                             .format(filter_ids[0]))
        filtered_value_data = {
            "values": filtered_df.values.tolist(),
            "col_ids": list(filtered_df.columns),
            "row_ids": list(filtered_df.index),
        }

        return filtered_value_data

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.data_util = DataUtil(config)
        self.attr_util = AttributesUtil(config)
        self.matrix_types = [x.split(".")[1].split('-')[0]
                             for x in self.data_util.list_generic_types()]

    def filter_matrix(self, params):
        """
        filter_matrix: create sub-matrix based on input feature_ids

        arguments:
        matrix_obj_ref: object reference of a matrix
        workspace_name: workspace name
        feature_ids: string of feature ids that result matrix contains
        filtered_matrix_name: name of newly created filtered matrix object
        """

        matrix_obj_ref = params.get('matrix_obj_ref')
        workspace_name = params.get('workspace_name')
        filter_ids = params.get('filter_ids')
        filtered_matrix_name = params.get('filtered_matrix_name')

        matrix_source = self.dfu.get_objects(
            {"object_refs": [matrix_obj_ref]})['data'][0]
        matrix_info = matrix_source.get('info')
        matrix_data = matrix_source.get('data')

        matrix_type = self._find_between(matrix_info[2], '\.', '\-')

        value_data = matrix_data.get('data')
        filter_ids = [x.strip() for x in filter_ids.split(',')]
        filtered_value_data = self._filter_value_data(value_data, filter_ids)

        # if the matrix has changed shape, update the mappings
        if len(filtered_value_data['row_ids']) < len(matrix_data['data']['row_ids']):
            if matrix_data.get('row_mapping'):
                matrix_data['row_mapping'] = {k: matrix_data['row_mapping'][k]
                                              for k in filtered_value_data['row_ids']}
            if matrix_data.get('feature_mapping'):
                matrix_data['feature_mapping'] = {k: matrix_data['feature_mapping'][k]
                                                  for k in filtered_value_data['row_ids']}

        if len(filtered_value_data['col_ids']) < len(matrix_data['data']['col_ids']):
            if matrix_data.get('col_mapping'):
                matrix_data['col_mapping'] = {k: matrix_data['col_mapping'][k]
                                              for k in filtered_value_data['col_ids']}
        matrix_data['data'] = filtered_value_data

        if not isinstance(workspace_name, int):
            workspace_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            workspace_id = workspace_name

        filtered_matrix_obj_ref = self.data_util.save_object({
                                                'obj_type': 'KBaseMatrices.{}'.format(matrix_type),
                                                'obj_name': filtered_matrix_name,
                                                'data': matrix_data,
                                                'workspace_name': workspace_id})['obj_ref']

        returnVal = {'matrix_obj_refs': [filtered_matrix_obj_ref]}

        report_output = self._generate_report(filtered_matrix_obj_ref, workspace_name)

        returnVal.update(report_output)

        return returnVal

    def search_matrix(self, params):
        """
        search_matrix: generate a HTML report that allows users to select feature ids

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
        row_attributemapping_ref = matrix_data.get('row_attributemapping_ref')

        row_ids = matrix_data['data']['row_ids']

        if not (row_mapping and row_attributemapping_ref):
            raise ValueError('Matrix obejct is missing either row_mapping or row_attributemapping_ref')

        attributemapping_data = self.dfu.get_objects(
                                    {"object_refs": [row_attributemapping_ref]})['data'][0]['data']

        header_str, table_str = self._build_html_str(row_mapping, attributemapping_data, row_ids)

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
        col_attributemapping_ref: column AttributeMapping reference
        row_attributemapping_ref: row AttributeMapping reference
        genome_ref: genome reference
        matrix_obj_ref: Matrix reference
        """

        (obj_type, file_path, workspace_name,
         matrix_name, refs, scale) = self._validate_import_matrix_from_excel_params(params)

        if not isinstance(workspace_name, int):
            workspace_id = self.dfu.ws_name_to_id(workspace_name)
        else:
            workspace_id = workspace_name

        data = self._file_to_data(file_path, refs, matrix_name, workspace_id)
        data['scale'] = scale
        if params.get('description'):
            data['description'] = params['description']

        matrix_obj_ref = self.data_util.save_object({
                                                'obj_type': 'KBaseMatrices.{}'.format(obj_type),
                                                'obj_name': matrix_name,
                                                'data': data,
                                                'workspace_name': workspace_id})['obj_ref']

        returnVal = {'matrix_obj_ref': matrix_obj_ref}

        report_output = self._generate_report(matrix_obj_ref, workspace_name)

        returnVal.update(report_output)

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

        data_matrix = self.data_util.fetch_data(params).get('data_matrix')
        df = pd.read_json(data_matrix)

        df.to_excel(file_path, sheet_name='data')

        if obj_data.get('col_mapping'):
            self._write_mapping_sheet(file_path, 'col_mapping',
                                      obj_data.get('col_mapping'), ['col_name', 'instance_name'])
            obj_data.pop('col_mapping')

        if obj_data.get('row_mapping'):
            self._write_mapping_sheet(file_path, 'row_mapping',
                                      obj_data.get('row_mapping'), ['row_name', 'instance_name'])
            obj_data.pop('row_mapping')

        try:
            obj_data.pop('data')
        except KeyError:
            log('Missing key [data]')

        obj_data.update(obj_data.get('attributes', {}))  # flatten for printing
        self._write_mapping_sheet(file_path, 'metadata', obj_data, ['name', 'value'])

        shock_id = self._upload_to_shock(file_path)

        return {'shock_id': shock_id}
