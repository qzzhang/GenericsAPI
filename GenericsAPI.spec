/*
A KBase module: GenericsAPI
*/
#include <KBaseExperiments.spec>

module GenericsAPI {
  /* A boolean - 0 for false, 1 for true.
    @range (0, 1)
  */
  typedef int boolean;

  /* An X/Y/Z style reference
  */
  typedef string obj_ref;

  /* workspace name of the object */
  typedef string workspace_name;

  /* Input of the fetch_data function
    obj_ref: generics object reference

    Optional arguments:
    generics_module: the generics data module to be retrieved from
                    e.g. for an given data type like below:
                    typedef structure {
                      FloatMatrix2D data;
                      condition_set_ref condition_set_ref;
                    } SomeGenericsMatrix;
                    generics_module should be
                    {'data': 'FloatMatrix2D',
                     'condition_set_ref': 'condition_set_ref'}
  */
  typedef structure {
    obj_ref obj_ref;
    mapping<string, string> generics_module;
  } FetchDataParams;

  /* Ouput of the fetch_data function
    data_matrix: a pandas dataframe in json format
  */
  typedef structure {
    string data_matrix;
  } FetchDataReturn;

  /* fetch_data: fetch generics data as pandas dataframe for a generics data object*/
  funcdef fetch_data(FetchDataParams params) returns(FetchDataReturn returnVal) authentication required;

  /* Input of the export_matrix function
    obj_ref: generics object reference

    Optional arguments:
    generics_module: select the generics data to be retrieved from
                        e.g. for an given data type like below:
                        typedef structure {
                          FloatMatrix2D data;
                          condition_set_ref condition_set_ref;
                        } SomeGenericsMatrix;
                        and only 'FloatMatrix2D' is needed
                        generics_module should be
                        {'data': FloatMatrix2D'}
  */
  typedef structure {
      obj_ref obj_ref;
      mapping<string, string> generics_module;
  } ExportParams;

  typedef structure {
      string shock_id;
  } ExportOutput;

  funcdef export_matrix (ExportParams params) returns (ExportOutput returnVal) authentication required;
  
  /* Input of the validate_data function
    obj_type: obj type e.g.: 'KBaseMatrices.ExpressionMatrix-1.1'
    data: data to be validated
  */
  typedef structure {
      string obj_type;
      mapping<string, string> data;
  } ValidateParams;

  typedef structure {
      boolean validated;
      mapping<string, string> failed_constraint;
  } ValidateOutput;

  /* validate_data: validate data*/
  funcdef validate_data (ValidateParams params) returns (ValidateOutput returnVal) authentication required;


  /* Input of the import_matrix_from_excel function
    obj_type: a type in KBaseMatrices
    input_shock_id: file shock id
    input_file_path: absolute file path
    input_staging_file_path: staging area file path
    matrix_name: matrix object name
    description: optional, a description of the matrix
    workspace_name: workspace name matrix object to be saved to

    optional:
    col_attributemapping_ref: column AttributeMapping reference
    row_attributemapping_ref: row AttributeMapping reference
    genome_ref: genome reference
    diff_expr_matrix_ref: DifferentialExpressionMatrix reference
    biochemistry_ref: (for MetaboliteMatrix)
    reads_set_ref: (raw data for AmpliconMatrix)

  */
  typedef structure {
      string obj_type;
      string input_shock_id;
      string input_file_path;
      string input_staging_file_path;
      string matrix_name;
      string scale;
      string description;
      workspace_name workspace_name;

      obj_ref genome_ref;
      obj_ref col_attributemapping_ref;
      obj_ref row_attributemapping_ref;
      obj_ref diff_expr_matrix_ref;
      obj_ref biochemistry_ref;
      obj_ref reads_set_ref;
  } ImportMatrixParams;

  typedef structure {
      string report_name;
      string report_ref;
      obj_ref matrix_obj_ref;
  } ImportMatrixOutput;

  /* import_matrix_from_excel: import matrix object from excel*/
  funcdef import_matrix_from_excel (ImportMatrixParams params) returns (ImportMatrixOutput returnVal) authentication required;

  /* import_matrix_from_biom: import matrix object from BIOM file format*/
  funcdef import_matrix_from_biom (ImportMatrixParams params) returns (ImportMatrixOutput returnVal) authentication required;

  /* Input of the import_matrix_from_excel function
    obj_type: saving object data type
    obj_name: saving object name
    data: data to be saved
    workspace_name: workspace name matrix object to be saved to
  */
  typedef structure {
      string obj_type;
      string obj_name;
      mapping<string, string> data;
      workspace_name workspace_name;
  } SaveObjectParams;

  typedef structure {
      obj_ref obj_ref;
  } SaveObjectOutput;

  /* save_object: validate data constraints and save matrix object*/
  funcdef save_object (SaveObjectParams params) returns (SaveObjectOutput returnVal) authentication required;

  /* Input of the search_matrix function
    matrix_obj_ref: object reference of a matrix
    workspace_name: workspace name objects to be saved to
  */
  typedef structure {
      obj_ref matrix_obj_ref;
      workspace_name workspace_name;
  } MatrixSelectorParams;

  typedef structure {
      string report_name;
      string report_ref;
  } MatrixSelectorOutput;

  /* search_matrix: generate a HTML report that allows users to select feature ids*/
  funcdef search_matrix (MatrixSelectorParams params) returns (MatrixSelectorOutput returnVal) authentication required;

  /* Input of the filter_matrix function
    matrix_obj_ref: object reference of a matrix
    workspace_name: workspace name objects to be saved to
    filter_ids: string of column or row ids that result matrix contains
    filtered_matrix_name: name of newly created filtered matrix object
  */
  typedef structure {
      obj_ref matrix_obj_ref;
      workspace_name workspace_name;
      string filter_ids;
      string filtered_matrix_name;
  } MatrixFilterParams;

  typedef structure {
      string report_name;
      string report_ref;
      list<obj_ref> matrix_obj_refs;
  } MatrixFilterOutput;

  /* filter_matrix: create sub-matrix based on input filter_ids*/
  funcdef filter_matrix (MatrixFilterParams params) returns (MatrixFilterOutput returnVal) authentication required;

  /* ATTRIBUTE MAPPING */

    /*
        input_shock_id and input_file_path - alternative input params,
    */
    typedef structure {
        string input_shock_id;
        string input_file_path;
        string output_ws_id;
        string output_obj_name;
    } FileToAttributeMappingParams;

    typedef structure {
        obj_ref attribute_mapping_ref;
    } FileToAttributeMappingOutput;

    funcdef file_to_attribute_mapping(FileToAttributeMappingParams params)
        returns (FileToAttributeMappingOutput result) authentication required;

    typedef structure {
        obj_ref input_ref;
        string destination_dir;
    } AttributeMappingToTsvFileParams;

    typedef structure {
        string file_path;
    } AttributeMappingToTsvFileOutput;

    funcdef attribute_mapping_to_tsv_file(AttributeMappingToTsvFileParams params)
        returns (AttributeMappingToTsvFileOutput result) authentication required;

    typedef structure {
        obj_ref input_ref;
    } ExportObjectParams;

    funcdef export_attribute_mapping_tsv(ExportObjectParams params)
        returns (ExportOutput result) authentication required;

    funcdef export_attribute_mapping_excel(ExportObjectParams params)
        returns (ExportOutput result) authentication required;

    funcdef export_cluster_set_excel(ExportObjectParams params)
        returns (ExportOutput result) authentication required;

    funcdef export_corr_matrix_excel(ExportObjectParams params)
        returns (ExportOutput result) authentication required;

    funcdef export_pca_matrix_excel(ExportObjectParams params)
        returns (ExportOutput result) authentication required;


  /* Input of the filter_matrix function
    input_obj_ref: object reference of a matrix
    workspace_name: workspace name objects to be saved to
    corr_matrix_name: correlation matrix object name
    dimension: compute correlation on column or row, one of ['col', 'row']
    method: correlation method, one of ['pearson', 'kendall', 'spearman']
    plot_corr_matrix: plot correlation matrix in report, default False
    plot_scatter_matrix: plot scatter matrix in report, default False
    compute_significance: also compute Significance in addition to correlation matrix
  */
  typedef structure {
      obj_ref input_obj_ref;
      workspace_name workspace_name;
      string corr_matrix_name;
      string dimension;
      string method;
      boolean plot_corr_matrix;
      boolean plot_scatter_matrix;
      boolean compute_significance;
  } CompCorrParams;

  typedef structure {
      string report_name;
      string report_ref;
      obj_ref corr_matrix_obj_ref;
  } CompCorrOutput;

  /* compute_correlation_matrix: create sub-matrix based on input filter_ids*/
  funcdef compute_correlation_matrix (CompCorrParams params) returns (CompCorrOutput returnVal) authentication required;


  /* Input of the build_network function
    corr_matrix_ref: CorrelationMatrix object
    workspace_name: workspace name objects to be saved to
    network_obj_name: Network object name
    filter_on_threshold: Dictory holder that holds filter on thredshold params
    params in filter_on_threshold:
      coefficient_threshold: correlation coefficient threshold (select pairs with greater correlation coefficient)
  */
  typedef structure {
      obj_ref corr_matrix_ref;
      workspace_name workspace_name;
      string network_obj_name;
      mapping<string, string> filter_on_threshold;
  } BuildNetworkParams;

  typedef structure {
      string report_name;
      string report_ref;
      obj_ref network_obj_ref;
  } BuildNetworkOutput;

  /* build_network: filter correlation matrix and build network*/
  funcdef build_network (BuildNetworkParams params) returns (BuildNetworkOutput returnVal) authentication required;

  /* Input of the run_pca function
    input_obj_ref: object reference of a matrix
    workspace_name: the name of the workspace
    pca_matrix_name: name of PCA (KBaseExperiments.PCAMatrix) object
    dimension: compute PCA on column or row, one of ['col', 'row']
    n_components - number of components (default 2)
    attribute_mapping_obj_ref - associated attribute_mapping_obj_ref
    scale_size_by - used for PCA plot to scale data size
    color_marker_by - used for PCA plot to group data
  */
  typedef structure {
    obj_ref input_obj_ref;
    string workspace_name;
    string pca_matrix_name;
    string dimension;
    int n_components;
    obj_ref attribute_mapping_obj_ref;
    mapping<string, string> scale_size_by;
    mapping<string, string> color_marker_by;
  } PCAParams;

  /* Ouput of the run_pca function
    pca_ref: PCA object reference (as KBaseExperiments.PCAMatrix data type)
    report_name: report name generated by KBaseReport
    report_ref: report reference generated by KBaseReport
  */
  typedef structure {
    obj_ref pca_ref;
    string report_name;
    string report_ref;
  } PCAOutput;

  /* run_pca: PCA analysis on matrix*/
  funcdef run_pca (PCAParams params) returns (PCAOutput returnVal) authentication required;

};
