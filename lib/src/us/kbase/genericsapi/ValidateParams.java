
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
 * <p>Original spec-file type: ValidateParams</p>
 * <pre>
 * Input of the validate_data function
 * obj_type: obj type e.g.: 'KBaseMatrices.ExpressionMatrix-1.1'
 * data: data to be validated
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_type",
    "data"
})
public class ValidateParams {

    @JsonProperty("obj_type")
    private java.lang.String objType;
    @JsonProperty("data")
    private Map<String, String> data;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("obj_type")
    public java.lang.String getObjType() {
        return objType;
    }

    @JsonProperty("obj_type")
    public void setObjType(java.lang.String objType) {
        this.objType = objType;
    }

    public ValidateParams withObjType(java.lang.String objType) {
        this.objType = objType;
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

    public ValidateParams withData(Map<String, String> data) {
        this.data = data;
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
        return ((((((("ValidateParams"+" [objType=")+ objType)+", data=")+ data)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
