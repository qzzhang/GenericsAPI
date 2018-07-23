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
    workspace_name: the name of the workspace

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
    string workspace_name;

    string target_data_field;
  } FetchDataParams;


  /* Ouput of the fetch_data function
    data_matrix: a pandas dataframe
  */
  typedef structure {
    mapping<string, string> data_matrix;
  } FetchData;

  /* fetch_data: fetch generics data as pandas dataframe for a generics data object*/
  funcdef fetch_data(FetchDataParams params) returns(FetchData returnVal) authentication required;
};
