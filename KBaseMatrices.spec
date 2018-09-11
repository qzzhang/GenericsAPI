/*
@author jjeffryes
*/
module KBaseMatrices{
    /*
      The workspace ID for a Genome data object.
      @id ws KBaseGenomes.Genome
    */
    typedef string ws_genome_id;

    /*
      The workspace ID for a ConditionSet data object
      @id ws KBaseExperiments.ConditionSet
    */
    typedef string ws_conditionset_id;

    /*
      A simple 2D matrix of floating point numbers with labels/ids for rows and
      columns.  The matrix is stored as a list of lists, with the outer list
      containing rows, and the inner lists containing values for each column of
      that row.  Row/Col ids should be unique.

      row_ids - unique ids for rows.
      col_ids - unique ids for columns.
      values - two dimensional array indexed as: values[row][col]
      @metadata ws length(row_ids) as n_rows
      @metadata ws length(col_ids) as n_cols
    */
    typedef structure {
      list<string> row_ids;
      list<string> col_ids;
      list<list<float>> values;
    } FloatMatrix2D;

    /*
      The workspace id for a single end or paired end reads object
      @id ws KBaseMatrices.DifferentialExpressionMatrix KBaseFeatureValues.DifferentialExpressionMatrix
    */
    typedef string differential_expression_matrix_ref;

    /*
      A wrapper around a FloatMatrix2D designed for simple matricies of Expression
      data.  Rows map to features, and columns map to conditions.  The data type
      includes some information about normalization factors and contains
      mappings from row ids to features and col ids to conditions.

      KBaseMatrices Attributes:
      description - short optional description of the dataset
      scale - raw, ln, log2, log10
      col_normalization - mean_center, median_center, mode_center, zscore
      row_normalization - mean_center, median_center, mode_center, zscore
      col_mapping - map from col_id to an id in the col_condition_set
      row_mapping - map from row_id to a id in the row_condition_set
      col_conditionset_ref - a reference to a condition set that relates to the columns
      row_conditionset_ref - a reference to a condition set that relates to the rows

      data - contains values for (feature,condition) pairs, where
          features correspond to rows and conditions are columns
          (ie data.values[feature][condition])

      Additional attributes:
      genome_ref - a reference to the aligned genome
      feature_mapping - map from row_id to feature id in the genome
      diff_expr_matrix_ref - added to connect filtered expression matrix to differential expression matrix
          used for filtering

      Validation:
      @unique data.row_ids
      @unique data.col_ids
      @contains data.row_ids row_mapping
      @contains data.col_ids col_mapping
      @contains values(row_mapping) row_conditionset_ref:conditions
      @contains values(col_mapping) col_conditionset_ref:conditions
      @contains data.row_ids genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id
      @contains values(feature_mapping) genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id

      @optional description row_normalization col_normalization
      @optional col_mapping row_mapping col_conditionset_ref row_conditionset_ref
      @optional genome_ref feature_mapping diff_expr_matrix_ref

      @metadata ws scale
      @metadata ws row_normalization
      @metadata ws col_normalization
      @metadata ws genome_ref as genome
      @metadata ws col_conditionset_ref as col_conditionset
      @metadata ws row_conditionset_ref as row_conditionset
      @metadata ws length(data.row_ids) as feature_count
      @metadata ws length(data.col_ids) as condition_count
    */
    typedef structure {
      string description;
      string scale;
      string row_normalization;
      string col_normalization;
      mapping<string, string> col_mapping;
      ws_conditionset_id col_conditionset_ref;
      mapping<string, string> row_mapping;
      ws_conditionset_id row_conditionset_ref;
      ws_genome_id genome_ref;
      mapping<string, string> feature_mapping;
      differential_expression_matrix_ref diff_expr_matrix_ref;
      FloatMatrix2D data;
    } ExpressionMatrix;

    /*
      A wrapper around a FloatMatrix2D designed for simple matricies of Differential
      Expression data.  Rows map to features, and columns map to conditions.  The
      data type includes some information about normalization factors and contains
      mappings from row ids to features and col ids to conditions.

      KBaseMatrices Attributes:
      description - short optional description of the dataset
      scale - raw, ln, log2, log10
      col_normalization - mean_center, median_center, mode_center, zscore
      row_normalization - mean_center, median_center, mode_center, zscore
      col_mapping - map from col_id to an id in the col_condition_set
      row_mapping - map from row_id to a id in the row_condition_set
      col_conditionset_ref - a reference to a condition set that relates to the columns
      row_conditionset_ref - a reference to a condition set that relates to the rows

      data - contains values for (feature,condition) pairs, where
          features correspond to rows and conditions are columns
          (ie data.values[feature][condition])

      Additional attributes:
      genome_ref - a reference to the aligned genome
      feature_mapping - map from row_id to feature id in the genome

      Validation:
      @unique data.row_ids
      @unique data.col_ids
      @contains data.row_ids row_mapping
      @contains data.col_ids col_mapping
      @contains values(row_mapping) row_conditionset_ref:conditions
      @contains values(col_mapping) col_conditionset_ref:conditions
      @contains data.row_ids genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id
      @contains values(feature_mapping) genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id

      @optional description row_normalization col_normalization
      @optional col_mapping row_mapping col_conditionset_ref row_conditionset_ref
      @optional genome_ref feature_mapping

      @metadata ws scale
      @metadata ws row_normalization
      @metadata ws col_normalization
      @metadata ws genome_ref as genome
      @metadata ws col_conditionset_ref as col_conditionset
      @metadata ws row_conditionset_ref as row_conditionset
      @metadata ws length(data.row_ids) as feature_count
      @metadata ws length(data.col_ids) as condition_count
    */
    typedef structure {
      string description;
      string scale;
      string row_normalization;
      string col_normalization;
      mapping<string, string> col_mapping;
      ws_conditionset_id col_conditionset_ref;
      mapping<string, string> row_mapping;
      ws_conditionset_id row_conditionset_ref;
      ws_genome_id genome_ref;
      mapping<string, string> feature_mapping;
      FloatMatrix2D data;
    } DifferentialExpressionMatrix;

    /*
      A wrapper around a FloatMatrix2D designed for simple matricies of Fitness data
      for gene/feature knockouts.  Generally fitness is measured as growth rate
      for the knockout strain relative to wildtype.

      KBaseMatrices Attributes:
      description - short optional description of the dataset
      scale - raw, ln, log2, log10
      col_normalization - mean_center, median_center, mode_center, zscore
      row_normalization - mean_center, median_center, mode_center, zscore
      col_mapping - map from col_id to an id in the col_condition_set
      row_mapping - map from row_id to a id in the row_condition_set
      col_conditionset_ref - a reference to a condition set that relates to the columns
      row_conditionset_ref - a reference to a condition set that relates to the rows

      data - contains values for (feature,condition) pairs, where
          features correspond to rows and conditions are columns
          (ie data.values[feature][condition])

      Additional attributes:
      genome_ref - a reference to the aligned genome
      feature_mapping - map from row_id to a set feature ids in the genome

      Validation:
      @unique data.row_ids
      @unique data.col_ids
      @contains data.row_ids row_mapping
      @contains data.col_ids col_mapping
      @contains values(row_mapping) row_conditionset_ref:conditions
      @contains values(col_mapping) col_conditionset_ref:conditions
      @contains data.row_ids genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id
      @contains values(feature_mapping) genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id

      @optional description row_normalization col_normalization
      @optional col_mapping row_mapping col_conditionset_ref row_conditionset_ref
      @optional genome_ref feature_mapping

      @metadata ws scale
      @metadata ws row_normalization
      @metadata ws col_normalization
      @metadata ws genome_ref as genome
      @metadata ws col_conditionset_ref as col_conditionset
      @metadata ws row_conditionset_ref as row_conditionset
      @metadata ws length(data.row_ids) as feature_count
      @metadata ws length(data.col_ids) as condition_count
    */
    typedef structure {
      string description;
      string scale;
      string row_normalization;
      string col_normalization;
      mapping<string, string> col_mapping;
      ws_conditionset_id col_conditionset_ref;
      mapping<string, string> row_mapping;
      ws_conditionset_id row_conditionset_ref;
      ws_genome_id genome_ref;
      mapping<string, list<string>> feature_mapping;
      FloatMatrix2D data;
    } FitnessMatrix;
};