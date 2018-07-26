
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
 * Optional arguments:
 * generics_type: the data type to be retrieved from
 * generics_type_name: the name of the data type to be retrieved from
 *                     e.g. for an given data type like below:
 *                     typedef structure {
 *                       FloatMatrix2D data;
 *                     } SomeGenericsMatrix;
 *                     generics_type should be 'FloatMatrix2D'
 *                     generics_type_name should be 'data'
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_ref",
    "generics_type",
    "generics_type_name"
})
public class FetchDataParams {

    @JsonProperty("obj_ref")
    private String objRef;
    @JsonProperty("generics_type")
    private String genericsType;
    @JsonProperty("generics_type_name")
    private String genericsTypeName;
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

    @JsonProperty("generics_type")
    public String getGenericsType() {
        return genericsType;
    }

    @JsonProperty("generics_type")
    public void setGenericsType(String genericsType) {
        this.genericsType = genericsType;
    }

    public FetchDataParams withGenericsType(String genericsType) {
        this.genericsType = genericsType;
        return this;
    }

    @JsonProperty("generics_type_name")
    public String getGenericsTypeName() {
        return genericsTypeName;
    }

    @JsonProperty("generics_type_name")
    public void setGenericsTypeName(String genericsTypeName) {
        this.genericsTypeName = genericsTypeName;
    }

    public FetchDataParams withGenericsTypeName(String genericsTypeName) {
        this.genericsTypeName = genericsTypeName;
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
        return ((((((((("FetchDataParams"+" [objRef=")+ objRef)+", genericsType=")+ genericsType)+", genericsTypeName=")+ genericsTypeName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
