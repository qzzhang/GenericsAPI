
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
 * <p>Original spec-file type: ExportParams</p>
 * <pre>
 * Input of the export_matrix function
 * obj_ref: generics object reference
 * Optional arguments:
 * generics_module: select the generics data to be retrieved from
 *                     e.g. for an given data type like below:
 *                     typedef structure {
 *                       FloatMatrix2D data;
 *                       condition_set_ref condition_set_ref;
 *                     } SomeGenericsMatrix;
 *                     and only 'FloatMatrix2D' is needed
 *                     generics_module should be
 *                     {'data': FloatMatrix2D'}
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_ref",
    "generics_module"
})
public class ExportParams {

    @JsonProperty("obj_ref")
    private java.lang.String objRef;
    @JsonProperty("generics_module")
    private Map<String, String> genericsModule;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("obj_ref")
    public java.lang.String getObjRef() {
        return objRef;
    }

    @JsonProperty("obj_ref")
    public void setObjRef(java.lang.String objRef) {
        this.objRef = objRef;
    }

    public ExportParams withObjRef(java.lang.String objRef) {
        this.objRef = objRef;
        return this;
    }

    @JsonProperty("generics_module")
    public Map<String, String> getGenericsModule() {
        return genericsModule;
    }

    @JsonProperty("generics_module")
    public void setGenericsModule(Map<String, String> genericsModule) {
        this.genericsModule = genericsModule;
    }

    public ExportParams withGenericsModule(Map<String, String> genericsModule) {
        this.genericsModule = genericsModule;
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
        return ((((((("ExportParams"+" [objRef=")+ objRef)+", genericsModule=")+ genericsModule)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
