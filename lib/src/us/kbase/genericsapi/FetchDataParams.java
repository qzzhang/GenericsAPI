
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
 * <p>Original spec-file type: FetchDataParams</p>
 * <pre>
 * Input of the fetch_data function
 * obj_ref: generics object reference
 * workspace_name: the name of the workspace
 * Optional arguments:
 * target_data_field: the data field to be retrieved from.
 *                    fetch_data will try to auto find this field.
 *                     e.g. for an given data type like below:
 *                     typedef structure {
 *                       FloatMatrix2D data;
 *                     } SomeGenericsMatrix;
 *                     data should be the target data field.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_ref",
    "workspace_name",
    "target_data_field"
})
public class FetchDataParams {

    @JsonProperty("obj_ref")
    private String objRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("target_data_field")
    private String targetDataField;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("obj_ref")
    public String getObjRef() {
        return objRef;
    }

    @JsonProperty("obj_ref")
    public void setObjRef(String objRef) {
        this.objRef = objRef;
    }

    public FetchDataParams withObjRef(String objRef) {
        this.objRef = objRef;
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

    public FetchDataParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("target_data_field")
    public String getTargetDataField() {
        return targetDataField;
    }

    @JsonProperty("target_data_field")
    public void setTargetDataField(String targetDataField) {
        this.targetDataField = targetDataField;
    }

    public FetchDataParams withTargetDataField(String targetDataField) {
        this.targetDataField = targetDataField;
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
        return ((((((((("FetchDataParams"+" [objRef=")+ objRef)+", workspaceName=")+ workspaceName)+", targetDataField=")+ targetDataField)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
