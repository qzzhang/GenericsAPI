
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
 * <p>Original spec-file type: ValidateOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "validated",
    "failed_constraint"
})
public class ValidateOutput {

    @JsonProperty("validated")
    private Long validated;
    @JsonProperty("failed_constraint")
    private Map<String, String> failedConstraint;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("validated")
    public Long getValidated() {
        return validated;
    }

    @JsonProperty("validated")
    public void setValidated(Long validated) {
        this.validated = validated;
    }

    public ValidateOutput withValidated(Long validated) {
        this.validated = validated;
        return this;
    }

    @JsonProperty("failed_constraint")
    public Map<String, String> getFailedConstraint() {
        return failedConstraint;
    }

    @JsonProperty("failed_constraint")
    public void setFailedConstraint(Map<String, String> failedConstraint) {
        this.failedConstraint = failedConstraint;
    }

    public ValidateOutput withFailedConstraint(Map<String, String> failedConstraint) {
        this.failedConstraint = failedConstraint;
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
        return ((((((("ValidateOutput"+" [validated=")+ validated)+", failedConstraint=")+ failedConstraint)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
