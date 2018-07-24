
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
 * <p>Original spec-file type: GenMatrixHTMLReturn</p>
 * <pre>
 * Ouput of the generate_matrix_html function
 * html_string: html as a string format
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "html_string"
})
public class GenMatrixHTMLReturn {

    @JsonProperty("html_string")
    private String htmlString;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("html_string")
    public String getHtmlString() {
        return htmlString;
    }

    @JsonProperty("html_string")
    public void setHtmlString(String htmlString) {
        this.htmlString = htmlString;
    }

    public GenMatrixHTMLReturn withHtmlString(String htmlString) {
        this.htmlString = htmlString;
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
        return ((((("GenMatrixHTMLReturn"+" [htmlString=")+ htmlString)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
