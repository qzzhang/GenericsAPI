
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
 * <p>Original spec-file type: FileToAttributeMappingParams</p>
 * <pre>
 * input_shock_id and input_file_path - alternative input params,
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_shock_id",
    "input_file_path",
    "output_ws_id",
    "output_obj_name"
})
public class FileToAttributeMappingParams {

    @JsonProperty("input_shock_id")
    private String inputShockId;
    @JsonProperty("input_file_path")
    private String inputFilePath;
    @JsonProperty("output_ws_id")
    private String outputWsId;
    @JsonProperty("output_obj_name")
    private String outputObjName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_shock_id")
    public String getInputShockId() {
        return inputShockId;
    }

    @JsonProperty("input_shock_id")
    public void setInputShockId(String inputShockId) {
        this.inputShockId = inputShockId;
    }

    public FileToAttributeMappingParams withInputShockId(String inputShockId) {
        this.inputShockId = inputShockId;
        return this;
    }

    @JsonProperty("input_file_path")
    public String getInputFilePath() {
        return inputFilePath;
    }

    @JsonProperty("input_file_path")
    public void setInputFilePath(String inputFilePath) {
        this.inputFilePath = inputFilePath;
    }

    public FileToAttributeMappingParams withInputFilePath(String inputFilePath) {
        this.inputFilePath = inputFilePath;
        return this;
    }

    @JsonProperty("output_ws_id")
    public String getOutputWsId() {
        return outputWsId;
    }

    @JsonProperty("output_ws_id")
    public void setOutputWsId(String outputWsId) {
        this.outputWsId = outputWsId;
    }

    public FileToAttributeMappingParams withOutputWsId(String outputWsId) {
        this.outputWsId = outputWsId;
        return this;
    }

    @JsonProperty("output_obj_name")
    public String getOutputObjName() {
        return outputObjName;
    }

    @JsonProperty("output_obj_name")
    public void setOutputObjName(String outputObjName) {
        this.outputObjName = outputObjName;
    }

    public FileToAttributeMappingParams withOutputObjName(String outputObjName) {
        this.outputObjName = outputObjName;
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
        return ((((((((((("FileToAttributeMappingParams"+" [inputShockId=")+ inputShockId)+", inputFilePath=")+ inputFilePath)+", outputWsId=")+ outputWsId)+", outputObjName=")+ outputObjName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
