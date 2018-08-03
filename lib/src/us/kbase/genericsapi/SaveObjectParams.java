
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
 * <p>Original spec-file type: SaveObjectParams</p>
 * <pre>
 * Input of the import_matrix_from_excel function
 * obj_type: saving object data type
 * obj_name: saving object name
 * data: data to be saved
 * workspace_name: workspace name matrix object to be saved to
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_type",
    "obj_name",
    "data",
    "workspace_name"
})
public class SaveObjectParams {

    @JsonProperty("obj_type")
    private java.lang.String objType;
    @JsonProperty("obj_name")
    private java.lang.String objName;
    @JsonProperty("data")
    private Map<String, String> data;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("obj_type")
    public java.lang.String getObjType() {
        return objType;
    }

    @JsonProperty("obj_type")
    public void setObjType(java.lang.String objType) {
        this.objType = objType;
    }

    public SaveObjectParams withObjType(java.lang.String objType) {
        this.objType = objType;
        return this;
    }

    @JsonProperty("obj_name")
    public java.lang.String getObjName() {
        return objName;
    }

    @JsonProperty("obj_name")
    public void setObjName(java.lang.String objName) {
        this.objName = objName;
    }

    public SaveObjectParams withObjName(java.lang.String objName) {
        this.objName = objName;
        return this;
    }

    @JsonProperty("data")
    public Map<String, String> getData() {
        return data;
    }

    @JsonProperty("data")
    public void setData(Map<String, String> data) {
        this.data = data;
    }

    public SaveObjectParams withData(Map<String, String> data) {
        this.data = data;
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

    public SaveObjectParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
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
        return ((((((((((("SaveObjectParams"+" [objType=")+ objType)+", objName=")+ objName)+", data=")+ data)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
