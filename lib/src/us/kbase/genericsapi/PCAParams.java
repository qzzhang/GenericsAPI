
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
 * <p>Original spec-file type: PCAParams</p>
 * <pre>
 * Input of the run_pca function
 * input_obj_ref: object reference of a matrix
 * workspace_name: the name of the workspace
 * pca_matrix_name: name of PCA (KBaseExperiments.PCAMatrix) object
 * n_components - number of components (default 2)
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_obj_ref",
    "workspace_name",
    "pca_matrix_name",
    "n_components"
})
public class PCAParams {

    @JsonProperty("input_obj_ref")
    private String inputObjRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("pca_matrix_name")
    private String pcaMatrixName;
    @JsonProperty("n_components")
    private Long nComponents;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_obj_ref")
    public String getInputObjRef() {
        return inputObjRef;
    }

    @JsonProperty("input_obj_ref")
    public void setInputObjRef(String inputObjRef) {
        this.inputObjRef = inputObjRef;
    }

    public PCAParams withInputObjRef(String inputObjRef) {
        this.inputObjRef = inputObjRef;
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

    public PCAParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("pca_matrix_name")
    public String getPcaMatrixName() {
        return pcaMatrixName;
    }

    @JsonProperty("pca_matrix_name")
    public void setPcaMatrixName(String pcaMatrixName) {
        this.pcaMatrixName = pcaMatrixName;
    }

    public PCAParams withPcaMatrixName(String pcaMatrixName) {
        this.pcaMatrixName = pcaMatrixName;
        return this;
    }

    @JsonProperty("n_components")
    public Long getNComponents() {
        return nComponents;
    }

    @JsonProperty("n_components")
    public void setNComponents(Long nComponents) {
        this.nComponents = nComponents;
    }

    public PCAParams withNComponents(Long nComponents) {
        this.nComponents = nComponents;
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
        return ((((((((((("PCAParams"+" [inputObjRef=")+ inputObjRef)+", workspaceName=")+ workspaceName)+", pcaMatrixName=")+ pcaMatrixName)+", nComponents=")+ nComponents)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
