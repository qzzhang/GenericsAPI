
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
 * <p>Original spec-file type: MatrixSelectorParams</p>
 * <pre>
 * Input of the search_matrix function
 * matrix_obj_ref: object reference of a matrix
 * workspace_name: workspace name objects to be saved to
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "matrix_obj_ref",
    "workspace_name"
})
public class MatrixSelectorParams {

    @JsonProperty("matrix_obj_ref")
    private String matrixObjRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("matrix_obj_ref")
    public String getMatrixObjRef() {
        return matrixObjRef;
    }

    @JsonProperty("matrix_obj_ref")
    public void setMatrixObjRef(String matrixObjRef) {
        this.matrixObjRef = matrixObjRef;
    }

    public MatrixSelectorParams withMatrixObjRef(String matrixObjRef) {
        this.matrixObjRef = matrixObjRef;
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

    public MatrixSelectorParams withWorkspaceName(String workspaceName) {
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
        return ((((((("MatrixSelectorParams"+" [matrixObjRef=")+ matrixObjRef)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
