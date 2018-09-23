
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
 * <p>Original spec-file type: CompCorrParams</p>
 * <pre>
 * Input of the filter_matrix function
 * input_obj_ref: object reference of a matrix
 * workspace_name: workspace name objects to be saved to
 * corr_matrix_name: correlation matrix object name
 * dimension: compute correlation on column or row, one of ['col', 'row']
 * method: correlation method, one of ['pearson', 'kendall', 'spearman']
 * plot_corr_matrix: plot correlation matrix in report, default False
 * plot_scatter_matrix: plot scatter matrix in report, default False
 * compute_significance: also compute Significance in addition to correlation matrix
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_obj_ref",
    "workspace_name",
    "corr_matrix_name",
    "dimension",
    "method",
    "plot_corr_matrix",
    "plot_scatter_matrix",
    "compute_significance"
})
public class CompCorrParams {

    @JsonProperty("input_obj_ref")
    private String inputObjRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("corr_matrix_name")
    private String corrMatrixName;
    @JsonProperty("dimension")
    private String dimension;
    @JsonProperty("method")
    private String method;
    @JsonProperty("plot_corr_matrix")
    private Long plotCorrMatrix;
    @JsonProperty("plot_scatter_matrix")
    private Long plotScatterMatrix;
    @JsonProperty("compute_significance")
    private Long computeSignificance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_obj_ref")
    public String getInputObjRef() {
        return inputObjRef;
    }

    @JsonProperty("input_obj_ref")
    public void setInputObjRef(String inputObjRef) {
        this.inputObjRef = inputObjRef;
    }

    public CompCorrParams withInputObjRef(String inputObjRef) {
        this.inputObjRef = inputObjRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CompCorrParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("corr_matrix_name")
    public String getCorrMatrixName() {
        return corrMatrixName;
    }

    @JsonProperty("corr_matrix_name")
    public void setCorrMatrixName(String corrMatrixName) {
        this.corrMatrixName = corrMatrixName;
    }

    public CompCorrParams withCorrMatrixName(String corrMatrixName) {
        this.corrMatrixName = corrMatrixName;
        return this;
    }

    @JsonProperty("dimension")
    public String getDimension() {
        return dimension;
    }

    @JsonProperty("dimension")
    public void setDimension(String dimension) {
        this.dimension = dimension;
    }

    public CompCorrParams withDimension(String dimension) {
        this.dimension = dimension;
        return this;
    }

    @JsonProperty("method")
    public String getMethod() {
        return method;
    }

    @JsonProperty("method")
    public void setMethod(String method) {
        this.method = method;
    }

    public CompCorrParams withMethod(String method) {
        this.method = method;
        return this;
    }

    @JsonProperty("plot_corr_matrix")
    public Long getPlotCorrMatrix() {
        return plotCorrMatrix;
    }

    @JsonProperty("plot_corr_matrix")
    public void setPlotCorrMatrix(Long plotCorrMatrix) {
        this.plotCorrMatrix = plotCorrMatrix;
    }

    public CompCorrParams withPlotCorrMatrix(Long plotCorrMatrix) {
        this.plotCorrMatrix = plotCorrMatrix;
        return this;
    }

    @JsonProperty("plot_scatter_matrix")
    public Long getPlotScatterMatrix() {
        return plotScatterMatrix;
    }

    @JsonProperty("plot_scatter_matrix")
    public void setPlotScatterMatrix(Long plotScatterMatrix) {
        this.plotScatterMatrix = plotScatterMatrix;
    }

    public CompCorrParams withPlotScatterMatrix(Long plotScatterMatrix) {
        this.plotScatterMatrix = plotScatterMatrix;
        return this;
    }

    @JsonProperty("compute_significance")
    public Long getComputeSignificance() {
        return computeSignificance;
    }

    @JsonProperty("compute_significance")
    public void setComputeSignificance(Long computeSignificance) {
        this.computeSignificance = computeSignificance;
    }

    public CompCorrParams withComputeSignificance(Long computeSignificance) {
        this.computeSignificance = computeSignificance;
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
        return ((((((((((((((((((("CompCorrParams"+" [inputObjRef=")+ inputObjRef)+", workspaceName=")+ workspaceName)+", corrMatrixName=")+ corrMatrixName)+", dimension=")+ dimension)+", method=")+ method)+", plotCorrMatrix=")+ plotCorrMatrix)+", plotScatterMatrix=")+ plotScatterMatrix)+", computeSignificance=")+ computeSignificance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
