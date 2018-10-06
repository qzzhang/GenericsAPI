import uuid

import biom

from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenericsAPI.Utils.AttributeUtils import AttributesUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.MatrixUtil import MatrixUtil
from KBaseReport.KBaseReportClient import KBaseReport


class BiomUtil:

    def _file_to_data(self, file_path, refs, matrix_name, workspace_id):
        data = refs
        table = biom.load_table(file_path)

        matrix_data = {'row_ids': table._observation_ids.tolist(),
                       'col_ids': table._sample_ids.tolist(),
                       'values': table.matrix_data.toarray().tolist()}

        data.update({'data': matrix_data})
        data['attributes'] = {}
        for k in ('create_date', 'generated_by'):
            val = getattr(table, k)
            if not val:
                continue
            if isinstance(val, bytes):
                data['attributes'][k] = val.decode('utf-8')
            else:
                data['attributes'][k] = str(val)
        data['search_attributes'] = [f'{k}|{v}' for k, v in data['attributes'].items()]

        if table._observation_metadata:
            name = matrix_name + "_row_attributes"
            data['row_attributemapping_ref'] = self._metadata_to_attribute_mapping(
                table._observation_ids, table._observation_metadata, name, workspace_id)
        if table._sample_metadata:
            name = matrix_name + "_col_attributes"
            data['col_attributemapping_ref'] = self._metadata_to_attribute_mapping(
                table._sample_ids, table._sample_metadata, name, workspace_id)

        return data

    def _metadata_to_attribute_mapping(self, instances, metadata, obj_name, ws_id):
        data = {'ontology_mapping_method': "BIOM file", 'instances': {}}
        sample_set = metadata[0:min(len(metadata), 25)]
        metadata_keys = sorted(set((k for m_dict in sample_set for k in m_dict)))
        data['attributes'] = [{'attribute': key,
                               'attribute_ont_id': self.attr_util.DEFAULT_ONTOLOGY_ID,
                               'attribute_ont_ref': self.attr_util.DEFAULT_ONTOLOGY_REF,
                               } for key in metadata_keys]
        for inst, meta in zip(instances, metadata):
            data['instances'][inst] = [str(meta[attr]) for attr in metadata_keys]
        info = self.dfu.save_objects({
            "id": ws_id,
            "objects": [{
                "type": "KBaseExperiments.AttributeMapping",
                "data": data,
                "name": obj_name
            }]
        })[0]
        return f'{info[6]}/{info[0]}/{info[4]}'

    def _generate_report(self, matrix_obj_ref, workspace_name):
        """
        _generate_report: generate summary report
        """

        report_params = {'message': '',
                         'objects_created': [{'ref': matrix_obj_ref,
                                              'description': 'Imported Matrix'}],
                         'workspace_name': workspace_name,
                         'report_object_name': 'import_matrix_from_biom_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.data_util = DataUtil(config)
        self.attr_util = AttributesUtil(config)
        self.matrix_util = MatrixUtil(config)
        self.matrix_types = [x.split(".")[1].split('-')[0]
                             for x in self.data_util.list_generic_types()]

    def import_matrix_from_biom(self, params):
        """

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

        (obj_type, file_path, workspace_name, matrix_name, refs, scale
         ) = self.matrix_util._validate_import_matrix_from_excel_params(params)

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
