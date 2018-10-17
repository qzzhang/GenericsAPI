
package us.kbase.genericsapi;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ImportMatrixParams</p>
 * <pre>
 * Input of the import_matrix_from_excel function
 * obj_type: a type in KBaseMatrices
 * input_shock_id: file shock id
 * input_file_path: absolute file path
 * input_staging_file_path: staging area file path
 * matrix_name: matrix object name
 * description: optional, a description of the matrix
 * workspace_name: workspace name matrix object to be saved to
 * optional:
 * col_attributemapping_ref: column AttributeMapping reference
 * row_attributemapping_ref: row AttributeMapping reference
 * genome_ref: genome reference
 * diff_expr_matrix_ref: DifferentialExpressionMatrix reference
 * biochemistry_ref: (for MetaboliteMatrix)
 * reads_set_ref: (raw data for AmpliconMatrix)
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_type",
    "input_shock_id",
    "input_file_path",
    "input_staging_file_path",
    "matrix_name",
    "scale",
    "description",
    "workspace_name",
    "genome_ref",
    "col_attributemapping_ref",
    "row_attributemapping_ref",
    "diff_expr_matrix_ref",
    "biochemistry_ref",
    "reads_set_ref"
})
public class ImportMatrixParams {

    @JsonProperty("obj_type")
    private String objType;
    @JsonProperty("input_shock_id")
    private String inputShockId;
    @JsonProperty("input_file_path")
    private String inputFilePath;
    @JsonProperty("input_staging_file_path")
    private String inputStagingFilePath;
    @JsonProperty("matrix_name")
    private String matrixName;
    @JsonProperty("scale")
    private String scale;
    @JsonProperty("description")
    private String description;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("genome_ref")
    private String genomeRef;
    @JsonProperty("col_attributemapping_ref")
    private String colAttributemappingRef;
    @JsonProperty("row_attributemapping_ref")
    private String rowAttributemappingRef;
    @JsonProperty("diff_expr_matrix_ref")
    private String diffExprMatrixRef;
    @JsonProperty("biochemistry_ref")
    private String biochemistryRef;
    @JsonProperty("reads_set_ref")
    private String readsSetRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("obj_type")
    public String getObjType() {
        return objType;
    }

    @JsonProperty("obj_type")
    public void setObjType(String objType) {
        this.objType = objType;
    }

    public ImportMatrixParams withObjType(String objType) {
        this.objType = objType;
        return this;
    }

    @JsonProperty("input_shock_id")
    public String getInputShockId() {
        return inputShockId;
    }

    @JsonProperty("input_shock_id")
    public void setInputShockId(String inputShockId) {
        this.inputShockId = inputShockId;
    }

    public ImportMatrixParams withInputShockId(String inputShockId) {
        this.inputShockId = inputShockId;
        return this;
    }

    @JsonProperty("input_file_path")
    public String getInputFilePath() {
        return inputFilePath;
    }

    @JsonProperty("input_file_path")
    public void setInputFilePath(String inputFilePath) {
        this.inputFilePath = inputFilePath;
    }

    public ImportMatrixParams withInputFilePath(String inputFilePath) {
        this.inputFilePath = inputFilePath;
        return this;
    }

    @JsonProperty("input_staging_file_path")
    public String getInputStagingFilePath() {
        return inputStagingFilePath;
    }

    @JsonProperty("input_staging_file_path")
    public void setInputStagingFilePath(String inputStagingFilePath) {
        this.inputStagingFilePath = inputStagingFilePath;
    }

    public ImportMatrixParams withInputStagingFilePath(String inputStagingFilePath) {
        this.inputStagingFilePath = inputStagingFilePath;
        return this;
    }

    @JsonProperty("matrix_name")
    public String getMatrixName() {
        return matrixName;
    }

    @JsonProperty("matrix_name")
    public void setMatrixName(String matrixName) {
        this.matrixName = matrixName;
    }

    public ImportMatrixParams withMatrixName(String matrixName) {
        this.matrixName = matrixName;
        return this;
    }

    @JsonProperty("scale")
    public String getScale() {
        return scale;
    }

    @JsonProperty("scale")
    public void setScale(String scale) {
        this.scale = scale;
    }

    public ImportMatrixParams withScale(String scale) {
        this.scale = scale;
        return this;
    }

    @JsonProperty("description")
    public String getDescription() {
        return description;
    }

    @JsonProperty("description")
    public void setDescription(String description) {
        this.description = description;
    }

    public ImportMatrixParams withDescription(String description) {
        this.description = description;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ImportMatrixParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("genome_ref")
    public String getGenomeRef() {
        return genomeRef;
    }

    @JsonProperty("genome_ref")
    public void setGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
    }

    public ImportMatrixParams withGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
        return this;
    }

    @JsonProperty("col_attributemapping_ref")
    public String getColAttributemappingRef() {
        return colAttributemappingRef;
    }

    @JsonProperty("col_attributemapping_ref")
    public void setColAttributemappingRef(String colAttributemappingRef) {
        this.colAttributemappingRef = colAttributemappingRef;
    }

    public ImportMatrixParams withColAttributemappingRef(String colAttributemappingRef) {
        this.colAttributemappingRef = colAttributemappingRef;
        return this;
    }

    @JsonProperty("row_attributemapping_ref")
    public String getRowAttributemappingRef() {
        return rowAttributemappingRef;
    }

    @JsonProperty("row_attributemapping_ref")
    public void setRowAttributemappingRef(String rowAttributemappingRef) {
        this.rowAttributemappingRef = rowAttributemappingRef;
    }

    public ImportMatrixParams withRowAttributemappingRef(String rowAttributemappingRef) {
        this.rowAttributemappingRef = rowAttributemappingRef;
        return this;
    }

    @JsonProperty("diff_expr_matrix_ref")
    public String getDiffExprMatrixRef() {
        return diffExprMatrixRef;
    }

    @JsonProperty("diff_expr_matrix_ref")
    public void setDiffExprMatrixRef(String diffExprMatrixRef) {
        this.diffExprMatrixRef = diffExprMatrixRef;
    }

    public ImportMatrixParams withDiffExprMatrixRef(String diffExprMatrixRef) {
        this.diffExprMatrixRef = diffExprMatrixRef;
        return this;
    }

    @JsonProperty("biochemistry_ref")
    public String getBiochemistryRef() {
        return biochemistryRef;
    }

    @JsonProperty("biochemistry_ref")
    public void setBiochemistryRef(String biochemistryRef) {
        this.biochemistryRef = biochemistryRef;
    }

    public ImportMatrixParams withBiochemistryRef(String biochemistryRef) {
        this.biochemistryRef = biochemistryRef;
        return this;
    }

    @JsonProperty("reads_set_ref")
    public String getReadsSetRef() {
        return readsSetRef;
    }

    @JsonProperty("reads_set_ref")
    public void setReadsSetRef(String readsSetRef) {
        this.readsSetRef = readsSetRef;
    }

    public ImportMatrixParams withReadsSetRef(String readsSetRef) {
        this.readsSetRef = readsSetRef;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((((((("ImportMatrixParams"+" [objType=")+ objType)+", inputShockId=")+ inputShockId)+", inputFilePath=")+ inputFilePath)+", inputStagingFilePath=")+ inputStagingFilePath)+", matrixName=")+ matrixName)+", scale=")+ scale)+", description=")+ description)+", workspaceName=")+ workspaceName)+", genomeRef=")+ genomeRef)+", colAttributemappingRef=")+ colAttributemappingRef)+", rowAttributemappingRef=")+ rowAttributemappingRef)+", diffExprMatrixRef=")+ diffExprMatrixRef)+", biochemistryRef=")+ biochemistryRef)+", readsSetRef=")+ readsSetRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
