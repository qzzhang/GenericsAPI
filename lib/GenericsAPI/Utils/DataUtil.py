
import time
import json
import traceback
import re
import pandas as pd
from dotmap import DotMap

from Workspace.WorkspaceClient import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil


def log(message, prefix_newline=False):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    print(('\n' if prefix_newline else '') + time_str + ': ' + message)


GENERICS_TYPE = ['FloatMatrix2D']  # add case in _convert_data for each additional type
GENERICS_MODULES = ['KBaseMatrices']


class DataUtil:

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

    def _find_between(self, s, start, end):
        """
        _find_between: find string in between start and end
        """

        return re.search('{}(.*){}'.format(start, end), s).group(1)

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

    def _filter_constraints(self, constraints, data):

        contains_constraints = constraints.get('contains')

        filtered_constraints = []
        for contains_constraint in contains_constraints:
            in_values = contains_constraint.split(' ')[1:]
            missing_key = True
            for in_value in in_values:
                if in_value.startswith('values'):
                    search_value = re.search('{}(.*){}'.format('\(', '\)'), in_value).group(1)
                    unique_list = search_value.split('.')
                    key = unique_list[0]
                elif ':' in in_value:
                    key = in_value.split(':')[0]
                else:
                    unique_list = in_value.split('.')
                    key = unique_list[0]

                if key in data:
                    missing_key = False
                    break

            if missing_key:
                filtered_constraints.append(contains_constraint)

        for x in filtered_constraints:
            contains_constraints.remove(x)

        return constraints

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
                generics_type_name = item.split(';')[0].strip().split(' ')[-1].strip()
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
        else:
            raise ValueError('Unexpected Data Type: {}'.format(data_types))

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

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.wsClient = workspaceService(self.ws_url, token=self.token)
        self.dfu = DataFileUtil(self.callback_url)

    def list_generic_types(self, params=None):
        """
        *Not yet exposed in spec*
        list_generic_types: lists the current valid generics types

        arguments:
            none

        return:
            A list of generic types in the current environment
        """
        returnVal = [x['type_def'] for module in GENERICS_MODULES
                     for x in self.wsClient.get_all_type_info(module)]
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

        log('--->\nrunning DataUtil.fetch_data\n' +
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

        constraints = self._filter_constraints(constraints, data)

        validated, failed_constraints = self._validate(constraints, data)

        returnVal = {'validated': validated,
                     'failed_constraints': failed_constraints}

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
