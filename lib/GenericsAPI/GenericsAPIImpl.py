# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from GenericsAPI.Utils.AttributeUtils import AttributesUtil
from GenericsAPI.Utils.BIOMUtil import BiomUtil
from GenericsAPI.Utils.CorrelationUtil import CorrelationUtil
from GenericsAPI.Utils.DataUtil import DataUtil
from GenericsAPI.Utils.MatrixUtil import MatrixUtil
from GenericsAPI.Utils.NetworkUtil import NetworkUtil
from GenericsAPI.Utils.PCAUtil import PCAUtil
from GenericsAPI.Utils.PCAUtil import MDSUtil
from GenericsAPI.Utils.DataTableUtil import DataTableUtil
from installed_clients.GenericsServiceClient import GenericsService
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
    VERSION = "1.0.0"
    GIT_URL = "https://github.com/qzzhang/GenericsAPI.git"
    GIT_COMMIT_HASH = "a8df52053c4670b5bf070bf04eb5a889f15aa1c8"

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
        self.network_util = NetworkUtil(self.config)
        self.biom_util = BiomUtil(self.config)
        self.pca_util = PCAUtil(self.config)
        self.mds_util = MDSUtil(self.config)
        self.data_table_util = DataTableUtil(self.config)

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
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
           true.), parameter "failed_constraint" of mapping from String to
           String
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
           import_matrix_from_excel function obj_type: a type in
           KBaseMatrices input_shock_id: file shock id input_file_path:
           absolute file path input_staging_file_path: staging area file path
           matrix_name: matrix object name description: optional, a
           description of the matrix workspace_name: workspace name matrix
           object to be saved to optional: col_attributemapping_ref: column
           AttributeMapping reference row_attributemapping_ref: row
           AttributeMapping reference genome_ref: genome reference
           diff_expr_matrix_ref: DifferentialExpressionMatrix reference
           biochemistry_ref: (for MetaboliteMatrix) reads_set_ref: (raw data
           for AmpliconMatrix)) -> structure: parameter "obj_type" of String,
           parameter "input_shock_id" of String, parameter "input_file_path"
           of String, parameter "input_staging_file_path" of String,
           parameter "matrix_name" of String, parameter "amplicon_set_name"
           of String, parameter "scale" of String, parameter "description" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "genome_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "col_attributemapping_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "row_attributemapping_ref" of type "obj_ref"
           (An X/Y/Z style reference), parameter "diff_expr_matrix_ref" of
           type "obj_ref" (An X/Y/Z style reference), parameter
           "biochemistry_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "reads_set_ref" of type "obj_ref" (An X/Y/Z style
           reference)
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

    def import_matrix_from_biom(self, ctx, params):
        """
        import_matrix_from_biom: import matrix object from BIOM file format
        :param params: instance of type "ImportMatrixParams" (Input of the
           import_matrix_from_excel function obj_type: a type in
           KBaseMatrices input_shock_id: file shock id input_file_path:
           absolute file path input_staging_file_path: staging area file path
           matrix_name: matrix object name description: optional, a
           description of the matrix workspace_name: workspace name matrix
           object to be saved to optional: col_attributemapping_ref: column
           AttributeMapping reference row_attributemapping_ref: row
           AttributeMapping reference genome_ref: genome reference
           diff_expr_matrix_ref: DifferentialExpressionMatrix reference
           biochemistry_ref: (for MetaboliteMatrix) reads_set_ref: (raw data
           for AmpliconMatrix)) -> structure: parameter "obj_type" of String,
           parameter "input_shock_id" of String, parameter "input_file_path"
           of String, parameter "input_staging_file_path" of String,
           parameter "matrix_name" of String, parameter "amplicon_set_name"
           of String, parameter "scale" of String, parameter "description" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "genome_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter
           "col_attributemapping_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "row_attributemapping_ref" of type "obj_ref"
           (An X/Y/Z style reference), parameter "diff_expr_matrix_ref" of
           type "obj_ref" (An X/Y/Z style reference), parameter
           "biochemistry_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "reads_set_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        :returns: instance of type "ImportMatrixOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_matrix_from_biom
        returnVal = self.biom_util.import_matrix_from_biom(params)
        #END import_matrix_from_biom

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_matrix_from_biom return value ' +
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
           "filtered_matrix_name" of String, parameter "remove_ids" of
           String, parameter "dimension" of String
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

    def standardize_matrix(self, ctx, params):
        """
        standardize_matrix: standardize a matrix
        :param params: instance of type "StandardizeMatrixParams" (Input of
           the standardize_matrix function input_matrix_ref: object reference
           of a matrix workspace_name: workspace name objects to be saved to
           with_mean: center data before scaling with_std: scale data to unit
           variance new_matrix_name: name of newly created matrix object) ->
           structure: parameter "input_matrix_ref" of type "obj_ref" (An
           X/Y/Z style reference), parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "with_mean" of type "boolean" (A boolean - 0 for false, 1 for
           true.), parameter "with_std" of type "boolean" (A boolean - 0 for
           false, 1 for true.), parameter "new_matrix_name" of String
        :returns: instance of type "StandardizeMatrixOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "new_matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN standardize_matrix
        returnVal = self.matrix_util.standardize_matrix(params)
        #END standardize_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method standardize_matrix return value ' +
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

    def update_matrix_attribute_mapping(self, ctx, params):
        """
        :param params: instance of type "UpdateMatrixAMParams" -> structure:
           parameter "staging_file_subdir_path" of String, parameter
           "dimension" of String, parameter "input_matrix_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter "workspace_name"
           of String, parameter "output_am_obj_name" of String, parameter
           "output_matrix_obj_name" of String
        :returns: instance of type "UpdateMatrixAMOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "new_matrix_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference), parameter "new_attribute_mapping_ref" of type
           "obj_ref" (An X/Y/Z style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN update_matrix_attribute_mapping
        logging.info("Starting 'update_matrix_attribute_mapping' with params:{}".format(params))
        self.attr_util.validate_params(params, ("staging_file_subdir_path", "dimension",
                                                "workspace_name", "output_am_obj_name",
                                                "input_matrix_ref",
                                                "output_matrix_obj_name"))
        returnVal = self.attr_util.update_matrix_attribute_mapping(params)
        #END update_matrix_attribute_mapping

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method update_matrix_attribute_mapping return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

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
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
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
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
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
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
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

    def export_corr_matrix_excel(self, ctx, params):
        """
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_corr_matrix_excel
        logging.info("Starting 'export_corr_matrix_excel' with params:{}".format(params))
        result = self.corr_util.export_corr_matrix_excel(params)
        #END export_corr_matrix_excel

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_corr_matrix_excel return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_pca_matrix_excel(self, ctx, params):
        """
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_pca_matrix_excel
        result = self.pca_util.export_pca_matrix_excel(params)
        #END export_pca_matrix_excel

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_pca_matrix_excel return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_amplicon_set_tsv(self, ctx, params):
        """
        :param params: instance of type "ExportObjectParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_amplicon_set_tsv
        result = self.biom_util.export_amplicon_set_tsv(params)
        #END export_amplicon_set_tsv

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_amplicon_set_tsv return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def compute_correlation_matrix(self, ctx, params):
        """
        compute_correlation_matrix: create sub-matrix based on input filter_ids
        :param params: instance of type "CompCorrParams" (Input of the
           compute_correlation_matrix function input_obj_ref: object
           reference of a matrix workspace_name: workspace name objects to be
           saved to corr_matrix_name: correlation matrix object name
           dimension: compute correlation on column or row, one of ['col',
           'row'] method: correlation method, one of ['pearson', 'kendall',
           'spearman'] plot_corr_matrix: plot correlation matrix in report,
           default False plot_scatter_matrix: plot scatter matrix in report,
           default False compute_significance: also compute Significance in
           addition to correlation matrix) -> structure: parameter
           "input_obj_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "workspace_name" of type "workspace_name" (workspace
           name of the object), parameter "corr_matrix_name" of String,
           parameter "dimension" of String, parameter "method" of String,
           parameter "plot_corr_matrix" of type "boolean" (A boolean - 0 for
           false, 1 for true.), parameter "plot_scatter_matrix" of type
           "boolean" (A boolean - 0 for false, 1 for true.), parameter
           "compute_significance" of type "boolean" (A boolean - 0 for false,
           1 for true.)
        :returns: instance of type "CompCorrOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "corr_matrix_obj_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN compute_correlation_matrix
        returnVal = self.corr_util.compute_correlation_matrix(params)
        #END compute_correlation_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method compute_correlation_matrix return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def compute_correlation_across_matrices(self, ctx, params):
        """
        compute_correlation_across_matrices: compute correlation matrix across matrices
        :param params: instance of type "CompCorrMetriceParams" (Input of the
           compute_correlation_across_matrices function matrix_ref_1: object
           reference of a matrix matrix_ref_2: object reference of a matrix
           workspace_name: workspace name objects to be saved to
           corr_matrix_name: correlation matrix object name dimension:
           compute correlation on column or row, one of ['col', 'row']
           method: correlation method, one of ['pearson', 'kendall',
           'spearman'] plot_corr_matrix: plot correlation matrix in report,
           default False compute_significance: also compute Significance in
           addition to correlation matrix) -> structure: parameter
           "matrix_ref_1" of type "obj_ref" (An X/Y/Z style reference),
           parameter "matrix_ref_2" of type "obj_ref" (An X/Y/Z style
           reference), parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "corr_matrix_name" of
           String, parameter "dimension" of String, parameter "method" of
           String, parameter "plot_corr_matrix" of type "boolean" (A boolean
           - 0 for false, 1 for true.), parameter "compute_significance" of
           type "boolean" (A boolean - 0 for false, 1 for true.), parameter
           "corr_threshold" of Double
        :returns: instance of type "CompCorrOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "corr_matrix_obj_ref" of type "obj_ref" (An X/Y/Z style
           reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN compute_correlation_across_matrices
        returnVal = self.corr_util.compute_correlation_across_matrices(params)
        #END compute_correlation_across_matrices

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method compute_correlation_across_matrices return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def build_network(self, ctx, params):
        """
        build_network: filter correlation matrix and build network
        :param params: instance of type "BuildNetworkParams" (Input of the
           build_network function corr_matrix_ref: CorrelationMatrix object
           workspace_name: workspace name objects to be saved to
           network_obj_name: Network object name filter_on_threshold: Dictory
           holder that holds filter on thredshold params params in
           filter_on_threshold: coefficient_threshold: correlation
           coefficient threshold (select pairs with greater correlation
           coefficient)) -> structure: parameter "corr_matrix_ref" of type
           "obj_ref" (An X/Y/Z style reference), parameter "workspace_name"
           of type "workspace_name" (workspace name of the object), parameter
           "network_obj_name" of String, parameter "filter_on_threshold" of
           mapping from String to String
        :returns: instance of type "BuildNetworkOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "network_obj_ref" of type "obj_ref" (An X/Y/Z
           style reference)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN build_network
        returnVal = self.network_util.build_network(params)
        #END build_network

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method build_network return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def run_pca(self, ctx, params):
        """
        run_pca: PCA analysis on matrix
        :param params: instance of type "PCAParams" (Input of the run_pca
           function input_obj_ref: object reference of a matrix
           workspace_name: the name of the workspace pca_matrix_name: name of
           PCA (KBaseExperiments.PCAMatrix) object dimension: compute PCA on
           column or row, one of ['col', 'row'] n_components - number of
           components (default 2) attribute_mapping_obj_ref - associated
           attribute_mapping_obj_ref scale_size_by - used for PCA plot to
           scale data size color_marker_by - used for PCA plot to group data)
           -> structure: parameter "input_obj_ref" of type "obj_ref" (An
           X/Y/Z style reference), parameter "workspace_name" of String,
           parameter "pca_matrix_name" of String, parameter "dimension" of
           String, parameter "n_components" of Long, parameter
           "attribute_mapping_obj_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "scale_size_by" of mapping from String to
           String, parameter "color_marker_by" of mapping from String to
           String
        :returns: instance of type "PCAOutput" (Ouput of the run_pca function
           pca_ref: PCA object reference (as KBaseExperiments.PCAMatrix data
           type) report_name: report name generated by KBaseReport
           report_ref: report reference generated by KBaseReport) ->
           structure: parameter "pca_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_pca
        returnVal = self.pca_util.run_pca(params)
        #END run_pca

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_pca return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def run_mds(self, ctx, params):
        """
        run_mds: MDS analysis on matrix
        :param params: instance of type "MDSParams" (Input of the run_mds
           function input_obj_ref: object reference of a matrix
           workspace_name: the name of the workspace mds_matrix_name: name of
           MDS (KBaseExperiments.MDSMatrix) object dimension: compute MDS on
           column or row, one of ['col', 'row'] n_components - number of
           components (default 2) attribute_mapping_obj_ref - associated
           attribute_mapping_obj_ref scale_size_by - used for MDS plot to
           scale data size color_marker_by - used for MDS plot to group data)
           -> structure: parameter "input_obj_ref" of type "obj_ref" (An
           X/Y/Z style reference), parameter "workspace_name" of String,
           parameter "mds_matrix_name" of String, parameter "dimension" of
           String, parameter "n_components" of Long, parameter
           "attribute_mapping_obj_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "scale_size_by" of mapping from String to
           String, parameter "color_marker_by" of mapping from String to
           String
        :returns: instance of type "MDSOutput" (Ouput of the run_mds function
           mds_ref: MDS object reference (as KBaseExperiments.MDSMatrix data
           type) report_name: report name generated by KBaseReport
           report_ref: report reference generated by KBaseReport) ->
           structure: parameter "mds_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_mds
        returnVal = self.mds_util.run_mds(params)
        #END run_mds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_mds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def view_matrix(self, ctx, params):
        """
        view_matrix: generate a report for matrix viewer
        :param params: instance of type "ViewMatrixParams" -> structure:
           parameter "input_matrix_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "workspace_name" of String, parameter
           "with_attribute_info" of type "boolean" (A boolean - 0 for false,
           1 for true.)
        :returns: instance of type "ViewMatrixOutput" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN view_matrix
        returnVal = self.data_table_util.view_matrix_as_table(params)
        #END view_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method view_matrix return value ' +
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
