# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os

from GenericsAPI.Utils.GenericsUtil import GenericsUtil
#END_HEADER


class GenericsAPI:
    '''
    Module Name:
    GenericsAPI

    Module Description:
    A KBase module: GenericsAPI
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Tianhao-Gu/GenericsAPI.git"
    GIT_COMMIT_HASH = "5ffad5b22b9c72822d3e0d8546091be0c723aac3"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
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
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.fetch_data(params)
        #END fetch_data

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fetch_data return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def generate_matrix_html(self, ctx, params):
        """
        generate_matrix_html: generate a html page for given data
        :param params: instance of type "GenMatrixHTMLParams" (Input of the
           generate_matrix_html function df: a pandas dataframe) ->
           structure: parameter "df" of mapping from String to String
        :returns: instance of type "GenMatrixHTMLReturn" (Ouput of the
           generate_matrix_html function html_string: html as a string
           format) -> structure: parameter "html_string" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN generate_matrix_html
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.generate_matrix_html(params)
        #END generate_matrix_html

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method generate_matrix_html return value ' +
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
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.export_matrix(params)
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
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.validate_data(params)
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
           be saved to) -> structure: parameter "obj_type" of String,
           parameter "input_shock_id" of String, parameter "input_file_path"
           of String, parameter "input_staging_file_path" of String,
           parameter "matrix_name" of String, parameter "workspace_name" of
           type "workspace_name" (workspace name of the object)
        :returns: instance of type "ImportMatrixOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_matrix_from_excel
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.import_matrix_from_excel(params)
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
        generics_api = GenericsUtil(self.config)
        returnVal = generics_api.save_object(params)
        #END save_object

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method save_object return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
