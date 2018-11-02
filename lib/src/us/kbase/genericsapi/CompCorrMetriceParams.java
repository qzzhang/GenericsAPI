
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
 * <p>Original spec-file type: CompCorrMetriceParams</p>
 * <pre>
 * Input of the compute_correlation_across_matrices function
 * matrix_ref_1: object reference of a matrix
 * matrix_ref_2: object reference of a matrix
 * workspace_name: workspace name objects to be saved to
 * corr_matrix_name: correlation matrix object name
 * dimension: compute correlation on column or row, one of ['col', 'row']
 * method: correlation method, one of ['pearson', 'kendall', 'spearman']
 * plot_corr_matrix: plot correlation matrix in report, default False
 * compute_significance: also compute Significance in addition to correlation matrix
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "matrix_ref_1",
    "matrix_ref_2",
    "workspace_name",
    "corr_matrix_name",
    "dimension",
    "method",
    "plot_corr_matrix",
    "compute_significance"
})
public class CompCorrMetriceParams {

    @JsonProperty("matrix_ref_1")
    private String matrixRef1;
    @JsonProperty("matrix_ref_2")
    private String matrixRef2;
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
    @JsonProperty("compute_significance")
    private Long computeSignificance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("matrix_ref_1")
    public String getMatrixRef1() {
        return matrixRef1;
    }

    @JsonProperty("matrix_ref_1")
    public void setMatrixRef1(String matrixRef1) {
        this.matrixRef1 = matrixRef1;
    }

    public CompCorrMetriceParams withMatrixRef1(String matrixRef1) {
        this.matrixRef1 = matrixRef1;
        return this;
    }

    @JsonProperty("matrix_ref_2")
    public String getMatrixRef2() {
        return matrixRef2;
    }

    @JsonProperty("matrix_ref_2")
    public void setMatrixRef2(String matrixRef2) {
        this.matrixRef2 = matrixRef2;
    }

    public CompCorrMetriceParams withMatrixRef2(String matrixRef2) {
        this.matrixRef2 = matrixRef2;
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

    public CompCorrMetriceParams withWorkspaceName(String workspaceName) {
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

    public CompCorrMetriceParams withCorrMatrixName(String corrMatrixName) {
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

    public CompCorrMetriceParams withDimension(String dimension) {
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

    public CompCorrMetriceParams withMethod(String method) {
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

    public CompCorrMetriceParams withPlotCorrMatrix(Long plotCorrMatrix) {
        this.plotCorrMatrix = plotCorrMatrix;
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

    public CompCorrMetriceParams withComputeSignificance(Long computeSignificance) {
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
        return ((((((((((((((((((("CompCorrMetriceParams"+" [matrixRef1=")+ matrixRef1)+", matrixRef2=")+ matrixRef2)+", workspaceName=")+ workspaceName)+", corrMatrixName=")+ corrMatrixName)+", dimension=")+ dimension)+", method=")+ method)+", plotCorrMatrix=")+ plotCorrMatrix)+", computeSignificance=")+ computeSignificance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
