
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
 * obj_type: one of ExpressionMatrix, FitnessMatrix, DifferentialExpressionMatrix
 * input_shock_id: file shock id
 * input_file_path: absolute file path
 * input_staging_file_path: staging area file path
 * matrix_name: matrix object name
 * workspace_name: workspace name matrix object to be saved to
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
    "workspace_name"
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
    @JsonProperty("workspace_name")
    private String workspaceName;
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
        return ((((((((((((((("ImportMatrixParams"+" [objType=")+ objType)+", inputShockId=")+ inputShockId)+", inputFilePath=")+ inputFilePath)+", inputStagingFilePath=")+ inputStagingFilePath)+", matrixName=")+ matrixName)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
