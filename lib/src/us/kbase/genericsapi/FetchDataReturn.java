
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
 * <p>Original spec-file type: FetchDataReturn</p>
 * <pre>
 * Ouput of the fetch_data function
 * data_matrix: a pandas dataframe in json format
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "data_matrix"
})
public class FetchDataReturn {

    @JsonProperty("data_matrix")
    private String dataMatrix;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("data_matrix")
    public String getDataMatrix() {
        return dataMatrix;
    }

    @JsonProperty("data_matrix")
    public void setDataMatrix(String dataMatrix) {
        this.dataMatrix = dataMatrix;
    }

    public FetchDataReturn withDataMatrix(String dataMatrix) {
        this.dataMatrix = dataMatrix;
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
        return ((((("FetchDataReturn"+" [dataMatrix=")+ dataMatrix)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
