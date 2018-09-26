
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
 * <p>Original spec-file type: BuildNetworkParams</p>
 * <pre>
 * Input of the build_network function
 * corr_matrix_ref: CorrelationMatrix object
 * workspace_name: workspace name objects to be saved to
 * network_obj_name: Network object name
 * filter_on_threshold: Dictory holder that holds filter on thredshold params
 * params in filter_on_threshold:
 *   coefficient_threshold: correlation coefficient threshold (select pairs with greater correlation coefficient)
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "corr_matrix_ref",
    "workspace_name",
    "network_obj_name",
    "filter_on_threshold"
})
public class BuildNetworkParams {

    @JsonProperty("corr_matrix_ref")
    private java.lang.String corrMatrixRef;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("network_obj_name")
    private java.lang.String networkObjName;
    @JsonProperty("filter_on_threshold")
    private Map<String, String> filterOnThreshold;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("corr_matrix_ref")
    public java.lang.String getCorrMatrixRef() {
        return corrMatrixRef;
    }

    @JsonProperty("corr_matrix_ref")
    public void setCorrMatrixRef(java.lang.String corrMatrixRef) {
        this.corrMatrixRef = corrMatrixRef;
    }

    public BuildNetworkParams withCorrMatrixRef(java.lang.String corrMatrixRef) {
        this.corrMatrixRef = corrMatrixRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public BuildNetworkParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("network_obj_name")
    public java.lang.String getNetworkObjName() {
        return networkObjName;
    }

    @JsonProperty("network_obj_name")
    public void setNetworkObjName(java.lang.String networkObjName) {
        this.networkObjName = networkObjName;
    }

    public BuildNetworkParams withNetworkObjName(java.lang.String networkObjName) {
        this.networkObjName = networkObjName;
        return this;
    }

    @JsonProperty("filter_on_threshold")
    public Map<String, String> getFilterOnThreshold() {
        return filterOnThreshold;
    }

    @JsonProperty("filter_on_threshold")
    public void setFilterOnThreshold(Map<String, String> filterOnThreshold) {
        this.filterOnThreshold = filterOnThreshold;
    }

    public BuildNetworkParams withFilterOnThreshold(Map<String, String> filterOnThreshold) {
        this.filterOnThreshold = filterOnThreshold;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((("BuildNetworkParams"+" [corrMatrixRef=")+ corrMatrixRef)+", workspaceName=")+ workspaceName)+", networkObjName=")+ networkObjName)+", filterOnThreshold=")+ filterOnThreshold)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
