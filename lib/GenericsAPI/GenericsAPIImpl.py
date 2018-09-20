# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import logging

from GenericsAPI.Utils.MatrixUtil import MatrixUtil
from GenericsAPI.Utils.AttributeUtils import AttributesUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.CorrelationUtil import CorrelationUtil
#END_HEADER


class GenericsAPI:
    '''
    Module Name:
    GenericsAPI

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Tianhao-Gu/GenericsAPI.git"
    GIT_COMMIT_HASH = "a8edaaf0752f0ac31b33a7951ad8a62fdca06ade"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.attr_util = AttributesUtil(self.config)
        self.matrix_util = MatrixUtil(self.config)
        self.corr_util = CorrelationUtil(self.config)
        self.data_util = DataUtil(self.config)
        logging.basicConfig(level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def fetch_data(self, ctx, params):
        """
        fetch_data: fetch generics data as pandas dataframe for a generics data object
        :param params: instance of type "FetchDataParams" (Input of the
           fetch_data function obj_ref: generics object reference Optional
           arguments: generics_module: the generics data module to be
           retrieved from e.g. for an given data type like below: typedef
           structure { FloatMatrix2D data; condition_set_ref
           condition_set_ref; } SomeGenericsMatrix; generics_module should be
           {'data': 'FloatMatrix2D', 'condition_set_ref':
           'condition_set_ref'}) -> structure: parameter "obj_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter "generics_module"
           of mapping from String to String
        :returns: instance of type "FetchDataReturn" (Ouput of the fetch_data
           function data_matrix: a pandas dataframe in json format) ->
           structure: parameter "data_matrix" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fetch_data
        returnVal = self.data_util.fetch_data(params)
        #END fetch_data

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_data return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def export_matrix(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (Input of the
           export_matrix function obj_ref: generics object reference Optional
           arguments: generics_module: select the generics data to be
           retrieved from e.g. for an given data type like below: typedef
           structure { FloatMatrix2D data; condition_set_ref
           condition_set_ref; } SomeGenericsMatrix; and only 'FloatMatrix2D'
           is needed generics_module should be {'data': FloatMatrix2D'}) ->
           structure: parameter "obj_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "generics_module" of mapping from String to
           String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN export_matrix
        returnVal = self.matrix_util.export_matrix(params)
        #END export_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method export_matrix return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def validate_data(self, ctx, params):
        """
        validate_data: validate data
        :param params: instance of type "ValidateParams" (Input of the
           validate_data function obj_type: obj type e.g.:
           'KBaseMatrices.ExpressionMatrix-1.1' data: data to be validated)
           -> structure: parameter "obj_type" of String, parameter "data" of
           mapping from String to String
        :returns: instance of type "ValidateOutput" -> structure: parameter
           "validated" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "failed_constraint" of mapping
           from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN validate_data
        returnVal = self.data_util.validate_data(params)
        #END validate_data

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method validate_data return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_matrix_from_excel(self, ctx, params):
        """
        import_matrix_from_excel: import matrix object from excel
        :param params: instance of type "ImportMatrixParams" (Input of the
           import_matrix_from_excel function obj_type: one of
           ExpressionMatrix, FitnessMatrix, DifferentialExpressionMatrix
           input_shock_id: file shock id input_file_path: absolute file path
           input_staging_file_path: staging area file path matrix_name:
           matrix object name workspace_name: workspace name matrix object to
           be saved to optional: col_attributemapping_ref: column
           AttributeMapping reference row_attributemapping_ref: row
           AttributeMapping reference genome_ref: genome reference
           diff_expr_matrix_ref: DifferentialExpressionMatrix reference) ->
           structure: parameter "obj_type" of String, parameter
           "input_shock_id" of String, parameter "input_file_path" of String,
           parameter "input_staging_file_path" of String, parameter
           "matrix_name" of String, parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "genome_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "col_attributemapping_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "row_attributemapping_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "diff_expr_matrix_ref" of type "obj_ref" (An X/Y/Z style reference)
        :returns: instance of type "ImportMatrixOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_matrix_from_excel
        returnVal = self.matrix_util.import_matrix_from_excel(params)
        #END import_matrix_from_excel

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_matrix_from_excel return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def save_object(self, ctx, params):
        """
        save_object: validate data constraints and save matrix object
        :param params: instance of type "SaveObjectParams" (Input of the
           import_matrix_from_excel function obj_type: saving object data
           type obj_name: saving object name data: data to be saved
           workspace_name: workspace name matrix object to be saved to) ->
           structure: parameter "obj_type" of String, parameter "obj_name" of
           String, parameter "data" of mapping from String to String,
           parameter "workspace_name" of type "workspace_name" (workspace
           name of the object)
        :returns: instance of type "SaveObjectOutput" -> structure: parameter
           "obj_ref" of type "obj_ref" (An X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN save_object
        returnVal = self.data_util.save_object(params)
        #END save_object

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method save_object return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def search_matrix(self, ctx, params):
        """
        search_matrix: generate a HTML report that allows users to select feature ids
        :param params: instance of type "MatrixSelectorParams" (Input of the
           search_matrix function matrix_obj_ref: object reference of a
           matrix workspace_name: workspace name objects to be saved to) ->
           structure: parameter "matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "workspace_name" of type
           "workspace_name" (workspace name of the object)
        :returns: instance of type "MatrixSelectorOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN search_matrix
        returnVal = self.matrix_util.search_matrix(params)
        #END search_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method search_matrix return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def filter_matrix(self, ctx, params):
        """
        filter_matrix: create sub-matrix based on input filter_ids
        :param params: instance of type "MatrixFilterParams" (Input of the
           filter_matrix function matrix_obj_ref: object reference of a
           matrix workspace_name: workspace name objects to be saved to
           filter_ids: string of column or row ids that result matrix
           contains filtered_matrix_name: name of newly created filtered
           matrix object) -> structure: parameter "matrix_obj_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter "workspace_name"
           of type "workspace_name" (workspace name of the object), parameter
           "filter_ids" of String, parameter "filtered_matrix_name" of String
        :returns: instance of type "MatrixFilterOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "matrix_obj_refs" of list of type "obj_ref" (An
           X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN filter_matrix
        returnVal = self.matrix_util.filter_matrix(params)
        #END filter_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method filter_matrix return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def file_to_attribute_mapping(self, ctx, params):
        """
        :param params: instance of type "FileToAttributeMappingParams"
           (input_shock_id and input_file_path - alternative input params,)
           -> structure: parameter "input_shock_id" of String, parameter
           "input_file_path" of String, parameter "output_ws_id" of String,
           parameter "output_obj_name" of String
        :returns: instance of type "FileToAttributeMappingOutput" ->
           structure: parameter "attribute_mapping_ref" of type "obj_ref" (An
           X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN file_to_attribute_mapping
        logging.info("Starting 'file_to_attribute_mapping' with params:{}".format(params))
        self.attr_util.validate_params(params, ("output_ws_id", "output_obj_name"),
                                       ('input_shock_id', 'input_file_path'))
        result = self.attr_util.file_to_attribute_mapping(params)
        #END file_to_attribute_mapping

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method file_to_attribute_mapping return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def attribute_mapping_to_tsv_file(self, ctx, params):
        """
        :param params: instance of type "AttributeMappingToTsvFileParams" ->
           structure: parameter "input_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "destination_dir" of String
        :returns: instance of type "AttributeMappingToTsvFileOutput" ->
           structure: parameter "file_path" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN attribute_mapping_to_tsv_file
        logging.info("Starting 'attribute_mapping_to_tsv_file' with params:{}".format(params))
        self.attr_util.validate_params(params, ("destination_dir", "input_ref"))
        am_id, result = self.attr_util.to_tsv(params)
        #END attribute_mapping_to_tsv_file

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method attribute_mapping_to_tsv_file return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_attribute_mapping_tsv(self, ctx, params):
        """
        :param params: instance of type "ExportAttributeMappingParams" ->
           structure: parameter "input_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_attribute_mapping_tsv
        logging.info("Starting 'export_attribute_mapping_tsv' with params:{}".format(params))
        self.attr_util.validate_params(params, ("input_ref",))
        params['destination_dir'] = self.scratch
        am_id, files = self.attr_util.to_tsv(params)
        result = self.attr_util.export(files['file_path'], am_id, params['input_ref'])
        #END export_attribute_mapping_tsv

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_attribute_mapping_tsv return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_attribute_mapping_excel(self, ctx, params):
        """
        :param params: instance of type "ExportAttributeMappingParams" ->
           structure: parameter "input_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_attribute_mapping_excel
        logging.info("Starting 'export_attribute_mapping_excel' with params:{}".format(params))
        self.attr_util.validate_params(params, ("input_ref",))
        params['destination_dir'] = self.scratch
        am_id, files = self.attr_util.to_excel(params)
        result = self.attr_util.export(files['file_path'], am_id, params['input_ref'])
        #END export_attribute_mapping_excel

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_attribute_mapping_excel return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_cluster_set_excel(self, ctx, params):
        """
        :param params: instance of type "ExportClusterSetParams" ->
           structure: parameter "input_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_cluster_set_excel
        logging.info("Starting 'export_cluster_set_excel' with params:{}".format(params))
        self.attr_util.validate_params(params, ("input_ref",))
        params['destination_dir'] = self.scratch
        cs_id, files = self.attr_util.to_excel(params)
        result = self.attr_util.export(files['file_path'], cs_id, params['input_ref'])
        #END export_cluster_set_excel

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_cluster_set_excel return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
