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
                    {'FloatMatrix2D': 'data',
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
                        {'FloatMatrix2D': 'data'}
  */
  typedef structure {
      obj_ref obj_ref;
      mapping<string, string> generics_module;
  } ExportParams;

  typedef structure {
      string shock_id;
  } ExportOutput;

  funcdef export_matrix (ExportParams params) returns (ExportOutput returnVal) authentication required;
};
