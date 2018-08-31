
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
 * <p>Original spec-file type: MatrixFilterParams</p>
 * <pre>
 * Input of the filter_matrix function
 * matrix_obj_ref: object reference of a matrix
 * workspace_name: workspace name objects to be saved to
 * filter_ids: string of column or row ids that result matrix contains
 * filtered_matrix_name: name of newly created filtered matrix object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "matrix_obj_ref",
    "workspace_name",
    "filter_ids",
    "filtered_matrix_name"
})
public class MatrixFilterParams {

    @JsonProperty("matrix_obj_ref")
    private String matrixObjRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("filter_ids")
    private String filterIds;
    @JsonProperty("filtered_matrix_name")
    private String filteredMatrixName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("matrix_obj_ref")
    public String getMatrixObjRef() {
        return matrixObjRef;
    }

    @JsonProperty("matrix_obj_ref")
    public void setMatrixObjRef(String matrixObjRef) {
        this.matrixObjRef = matrixObjRef;
    }

    public MatrixFilterParams withMatrixObjRef(String matrixObjRef) {
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

    public MatrixFilterParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("filter_ids")
    public String getFilterIds() {
        return filterIds;
    }

    @JsonProperty("filter_ids")
    public void setFilterIds(String filterIds) {
        this.filterIds = filterIds;
    }

    public MatrixFilterParams withFilterIds(String filterIds) {
        this.filterIds = filterIds;
        return this;
    }

    @JsonProperty("filtered_matrix_name")
    public String getFilteredMatrixName() {
        return filteredMatrixName;
    }

    @JsonProperty("filtered_matrix_name")
    public void setFilteredMatrixName(String filteredMatrixName) {
        this.filteredMatrixName = filteredMatrixName;
    }

    public MatrixFilterParams withFilteredMatrixName(String filteredMatrixName) {
        this.filteredMatrixName = filteredMatrixName;
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
        return ((((((((((("MatrixFilterParams"+" [matrixObjRef=")+ matrixObjRef)+", workspaceName=")+ workspaceName)+", filterIds=")+ filterIds)+", filteredMatrixName=")+ filteredMatrixName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
