/*
A KBase module: GenericsAPI
*/

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

  /* Input of the generate_matrix_html function
    df: a pandas dataframe
  */
  typedef structure {
    mapping<string, string> df;
  } GenMatrixHTMLParams;

  /* Ouput of the generate_matrix_html function
    html_string: html as a string format
  */
  typedef structure {
    string html_string;
  } GenMatrixHTMLReturn;

  /* generate_matrix_html: generate a html page for given data*/
  funcdef generate_matrix_html(GenMatrixHTMLParams params) returns(GenMatrixHTMLReturn returnVal) authentication required;


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
    obj_type: one of ExpressionMatrix, FitnessMatrix, DifferentialExpressionMatrix
    input_shock_id: file shock id
    input_file_path: absolute file path
    input_staging_file_path: staging area file path
    matrix_name: matrix object name
    workspace_name: workspace name matrix object to be saved to
  */
  typedef structure {
      string obj_type;
      string input_shock_id;
      string input_file_path;
      string input_staging_file_path;
      string matrix_name;
      workspace_name workspace_name;
  } ImportMatrixParams;

  typedef structure {
      string report_name;
      string report_ref;
      obj_ref matrix_obj_ref;
  } ImportMatrixOutput;

  /* import_matrix_from_excel: import matrix object from excel*/
  funcdef import_matrix_from_excel (ImportMatrixParams params) returns (ImportMatrixOutput returnVal) authentication required;

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
};
