
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
 * <p>Original spec-file type: FileToAttributeMappingOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "attribute_mapping_ref"
})
public class FileToAttributeMappingOutput {

    @JsonProperty("attribute_mapping_ref")
    private String attributeMappingRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("attribute_mapping_ref")
    public String getAttributeMappingRef() {
        return attributeMappingRef;
    }

    @JsonProperty("attribute_mapping_ref")
    public void setAttributeMappingRef(String attributeMappingRef) {
        this.attributeMappingRef = attributeMappingRef;
    }

    public FileToAttributeMappingOutput withAttributeMappingRef(String attributeMappingRef) {
        this.attributeMappingRef = attributeMappingRef;
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
        return ((((("FileToAttributeMappingOutput"+" [attributeMappingRef=")+ attributeMappingRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
