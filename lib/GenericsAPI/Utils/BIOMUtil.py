import uuid

import biom

from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenericsAPI.Utils.AttributeUtils import AttributesUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.MatrixUtil import MatrixUtil
from KBaseReport.KBaseReportClient import KBaseReport


class BiomUtil:

    def _file_to_data(self, file_path, refs, matrix_name, workspace_id, taxonomy_source):
        amplicon_data = refs
        amplicon_set_data = dict()
        table = biom.load_table(file_path)

        observation_ids = table._observation_ids.tolist()
        observation_metadata = table._observation_metadata

        amplicons = dict()
        for index, observation_id in enumerate(observation_ids):
            amplicon = dict()
            taxonomy = dict()
            if observation_metadata:
                taxonomy.update({'lineage': observation_metadata[index].get('taxonomy')})
            else:
                taxonomy.update({'lineage': None})
            # add TaxonomyData to Amplicon
            amplicon.update({'taxonomy_source': taxonomy_source})
            amplicon.update({'taxonomy': taxonomy})
            # add Amplicon
            amplicons.update({observation_id: amplicon})
        amplicon_set_data.update({'amplicons': amplicons})

        if 'reads_set_ref' in refs:
            amplicon_set_data.udpate({'reads_set_ref': refs.get('reads_set_ref')})

        matrix_data = {'row_ids': observation_ids,
                       'col_ids': table._sample_ids.tolist(),
                       'values': table.matrix_data.toarray().tolist()}

        amplicon_data.update({'data': matrix_data})
        amplicon_data.update(self.get_attribute_mapping("row", observation_metadata,
                                                        matrix_data, matrix_name, refs,
                                                        workspace_id))
        amplicon_data.update(self.get_attribute_mapping("col", table._sample_metadata,
                                                        matrix_data, matrix_name, refs,
                                                        workspace_id))

        amplicon_data['attributes'] = {}
        for k in ('create_date', 'generated_by'):
            val = getattr(table, k)
            if not val:
                continue
            if isinstance(val, bytes):
                amplicon_data['attributes'][k] = val.decode('utf-8')
            else:
                amplicon_data['attributes'][k] = str(val)
        amplicon_data['search_attributes'] = [f'{k}|{v}' for k, v in amplicon_data['attributes'].items()]

        return amplicon_data, amplicon_set_data

    def get_attribute_mapping(self, axis, metadata, matrix_data, matrix_name, refs,  workspace_id):
        mapping_data = {}
        axis_ids = matrix_data[f'{axis}_ids']
        if refs.get(f'{axis}_attributemapping_ref'):
            am_data = self.dfu.get_objects(
                {'object_refs': [refs[f'{axis}_attributemapping_ref']]}
            )['data'][0]['data']
            unmatched_ids = set(axis_ids) - set(am_data['instances'].keys())
            if unmatched_ids:
                name = "Column" if axis == 'col' else "Row"
                raise ValueError(f"The following {name} IDs from the uploaded matrix do not match "
                                 f"the supplied {name} attribute mapping: {', '.join(unmatched_ids)}"
                                 f"\nPlease verify the input data or upload an excel file with a"
                                 f"{name} mapping tab.")
            else:
                mapping_data[f'{axis}_mapping'] = {x: x for x in axis_ids}

        elif metadata:
            name = matrix_name + "_row_attributes"
            mapping_data[f'{axis}_attributemapping_ref'] = self._metadata_to_attribute_mapping(
                axis_ids, metadata, name, workspace_id)
            # if coming from biom file, metadata and axis IDs are guaranteed to match
            mapping_data[f'{axis}_mapping'] = {x: x for x in axis_ids}
        return mapping_data

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

        amplicon_data, amplicon_set_data = self._file_to_data(file_path, refs, matrix_name,
                                                              workspace_id,
                                                              params.get('taxonomy_source', 'other'))
        amplicon_data['scale'] = scale
        description = params.get('description')
        if description:
            amplicon_data['description'] = description
            amplicon_set_data['description'] = description

        matrix_obj_ref = self.data_util.save_object({
                                                'obj_type': 'KBaseMatrices.{}'.format(obj_type),
                                                'obj_name': matrix_name,
                                                'data': amplicon_data,
                                                'workspace_name': workspace_id})['obj_ref']

        amplicon_set_data['amplicon_matrix_ref'] = matrix_obj_ref

        returnVal = {'matrix_obj_ref': matrix_obj_ref}

        report_output = self._generate_report(matrix_obj_ref, workspace_name)

        returnVal.update(report_output)

        return returnVal
