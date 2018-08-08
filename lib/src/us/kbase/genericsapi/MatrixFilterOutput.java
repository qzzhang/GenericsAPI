
package us.kbase.genericsapi;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MatrixFilterOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "report_name",
    "report_ref",
    "matrix_obj_refs"
})
public class MatrixFilterOutput {

    @JsonProperty("report_name")
    private java.lang.String reportName;
    @JsonProperty("report_ref")
    private java.lang.String reportRef;
    @JsonProperty("matrix_obj_refs")
    private List<String> matrixObjRefs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("report_name")
    public java.lang.String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(java.lang.String reportName) {
        this.reportName = reportName;
    }

    public MatrixFilterOutput withReportName(java.lang.String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public java.lang.String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
    }

    public MatrixFilterOutput withReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
        return this;
    }

    @JsonProperty("matrix_obj_refs")
    public List<String> getMatrixObjRefs() {
        return matrixObjRefs;
    }

    @JsonProperty("matrix_obj_refs")
    public void setMatrixObjRefs(List<String> matrixObjRefs) {
        this.matrixObjRefs = matrixObjRefs;
    }

    public MatrixFilterOutput withMatrixObjRefs(List<String> matrixObjRefs) {
        this.matrixObjRefs = matrixObjRefs;
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
        return ((((((((("MatrixFilterOutput"+" [reportName=")+ reportName)+", reportRef=")+ reportRef)+", matrixObjRefs=")+ matrixObjRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
