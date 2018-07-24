
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
 * <p>Original spec-file type: GenMatrixHTMLParams</p>
 * <pre>
 * Input of the generate_matrix_html function
 * df: a pandas dataframe
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "df"
})
public class GenMatrixHTMLParams {

    @JsonProperty("df")
    private Map<String, String> df;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("df")
    public Map<String, String> getDf() {
        return df;
    }

    @JsonProperty("df")
    public void setDf(Map<String, String> df) {
        this.df = df;
    }

    public GenMatrixHTMLParams withDf(Map<String, String> df) {
        this.df = df;
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
        return ((((("GenMatrixHTMLParams"+" [df=")+ df)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
