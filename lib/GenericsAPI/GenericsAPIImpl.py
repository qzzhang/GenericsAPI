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
    GIT_COMMIT_HASH = "ff00a997232e190d2095b566a0e8805282c63aca"

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
           fetch_data function obj_ref: generics object reference
           workspace_name: the name of the workspace Optional arguments:
           target_data_field: the data field to be retrieved from. fetch_data
           will try to auto find this field. e.g. for an given data type like
           below: typedef structure { FloatMatrix2D data; }
           SomeGenericsMatrix; data should be the target data field.) ->
           structure: parameter "obj_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "workspace_name" of String, parameter
           "target_data_field" of String
        :returns: instance of type "FetchDataReturn" (Ouput of the fetch_data
           function data_matrix: a pandas dataframe) -> structure: parameter
           "data_matrix" of mapping from String to String
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
           generate_matrix_html function data_matrix: a pandas dataframe e.g.
           {'Department': 'string', 'Revenues':'number'} data: data used to
           generate html report e.g. [['Shoes', 10700], ['Sports', -15400]])
           -> structure: parameter "data_matrix" of mapping from String to
           String
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
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
