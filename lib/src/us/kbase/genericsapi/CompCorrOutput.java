
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
 * <p>Original spec-file type: CompCorrOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "report_name",
    "report_ref",
    "corr_matrix_obj_ref"
})
public class CompCorrOutput {

    @JsonProperty("report_name")
    private String reportName;
    @JsonProperty("report_ref")
    private String reportRef;
    @JsonProperty("corr_matrix_obj_ref")
    private String corrMatrixObjRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("report_name")
    public String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(String reportName) {
        this.reportName = reportName;
    }

    public CompCorrOutput withReportName(String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(String reportRef) {
        this.reportRef = reportRef;
    }

    public CompCorrOutput withReportRef(String reportRef) {
        this.reportRef = reportRef;
        return this;
    }

    @JsonProperty("corr_matrix_obj_ref")
    public String getCorrMatrixObjRef() {
        return corrMatrixObjRef;
    }

    @JsonProperty("corr_matrix_obj_ref")
    public void setCorrMatrixObjRef(String corrMatrixObjRef) {
        this.corrMatrixObjRef = corrMatrixObjRef;
    }

    public CompCorrOutput withCorrMatrixObjRef(String corrMatrixObjRef) {
        this.corrMatrixObjRef = corrMatrixObjRef;
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
        return ((((((((("CompCorrOutput"+" [reportName=")+ reportName)+", reportRef=")+ reportRef)+", corrMatrixObjRef=")+ corrMatrixObjRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
