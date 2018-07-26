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
    target_data_field: the data field to be retrieved from.
                       fetch_data will try to auto find this field.
                        e.g. for an given data type like below:
                        typedef structure {
                          FloatMatrix2D data;
                        } SomeGenericsMatrix;
                        data should be the target data field.
  */
  typedef structure {
    obj_ref obj_ref;
    string target_data_field;
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
};
