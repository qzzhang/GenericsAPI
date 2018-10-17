
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
 * <p>Original spec-file type: PCAParams</p>
 * <pre>
 * Input of the run_pca function
 * input_obj_ref: object reference of a matrix
 * workspace_name: the name of the workspace
 * pca_matrix_name: name of PCA (KBaseExperiments.PCAMatrix) object
 * dimension: compute PCA on column or row, one of ['col', 'row']
 * n_components - number of components (default 2)
 * attribute_mapping_obj_ref - associated attribute_mapping_obj_ref
 * customize_instance_group - customer and select which instance group to plot
 * scale_size_by - used for PCA plot to scale data size
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_obj_ref",
    "workspace_name",
    "pca_matrix_name",
    "dimension",
    "n_components",
    "attribute_mapping_obj_ref",
    "customize_instance_group",
    "scale_size_by"
})
public class PCAParams {

    @JsonProperty("input_obj_ref")
    private java.lang.String inputObjRef;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("pca_matrix_name")
    private java.lang.String pcaMatrixName;
    @JsonProperty("dimension")
    private java.lang.String dimension;
    @JsonProperty("n_components")
    private Long nComponents;
    @JsonProperty("attribute_mapping_obj_ref")
    private java.lang.String attributeMappingObjRef;
    @JsonProperty("customize_instance_group")
    private List<Map<String, String>> customizeInstanceGroup;
    @JsonProperty("scale_size_by")
    private Map<String, String> scaleSizeBy;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("input_obj_ref")
    public java.lang.String getInputObjRef() {
        return inputObjRef;
    }

    @JsonProperty("input_obj_ref")
    public void setInputObjRef(java.lang.String inputObjRef) {
        this.inputObjRef = inputObjRef;
    }

    public PCAParams withInputObjRef(java.lang.String inputObjRef) {
        this.inputObjRef = inputObjRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public PCAParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("pca_matrix_name")
    public java.lang.String getPcaMatrixName() {
        return pcaMatrixName;
    }

    @JsonProperty("pca_matrix_name")
    public void setPcaMatrixName(java.lang.String pcaMatrixName) {
        this.pcaMatrixName = pcaMatrixName;
    }

    public PCAParams withPcaMatrixName(java.lang.String pcaMatrixName) {
        this.pcaMatrixName = pcaMatrixName;
        return this;
    }

    @JsonProperty("dimension")
    public java.lang.String getDimension() {
        return dimension;
    }

    @JsonProperty("dimension")
    public void setDimension(java.lang.String dimension) {
        this.dimension = dimension;
    }

    public PCAParams withDimension(java.lang.String dimension) {
        this.dimension = dimension;
        return this;
    }

    @JsonProperty("n_components")
    public Long getNComponents() {
        return nComponents;
    }

    @JsonProperty("n_components")
    public void setNComponents(Long nComponents) {
        this.nComponents = nComponents;
    }

    public PCAParams withNComponents(Long nComponents) {
        this.nComponents = nComponents;
        return this;
    }

    @JsonProperty("attribute_mapping_obj_ref")
    public java.lang.String getAttributeMappingObjRef() {
        return attributeMappingObjRef;
    }

    @JsonProperty("attribute_mapping_obj_ref")
    public void setAttributeMappingObjRef(java.lang.String attributeMappingObjRef) {
        this.attributeMappingObjRef = attributeMappingObjRef;
    }

    public PCAParams withAttributeMappingObjRef(java.lang.String attributeMappingObjRef) {
        this.attributeMappingObjRef = attributeMappingObjRef;
        return this;
    }

    @JsonProperty("customize_instance_group")
    public List<Map<String, String>> getCustomizeInstanceGroup() {
        return customizeInstanceGroup;
    }

    @JsonProperty("customize_instance_group")
    public void setCustomizeInstanceGroup(List<Map<String, String>> customizeInstanceGroup) {
        this.customizeInstanceGroup = customizeInstanceGroup;
    }

    public PCAParams withCustomizeInstanceGroup(List<Map<String, String>> customizeInstanceGroup) {
        this.customizeInstanceGroup = customizeInstanceGroup;
        return this;
    }

    @JsonProperty("scale_size_by")
    public Map<String, String> getScaleSizeBy() {
        return scaleSizeBy;
    }

    @JsonProperty("scale_size_by")
    public void setScaleSizeBy(Map<String, String> scaleSizeBy) {
        this.scaleSizeBy = scaleSizeBy;
    }

    public PCAParams withScaleSizeBy(Map<String, String> scaleSizeBy) {
        this.scaleSizeBy = scaleSizeBy;
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
        return ((((((((((((((((((("PCAParams"+" [inputObjRef=")+ inputObjRef)+", workspaceName=")+ workspaceName)+", pcaMatrixName=")+ pcaMatrixName)+", dimension=")+ dimension)+", nComponents=")+ nComponents)+", attributeMappingObjRef=")+ attributeMappingObjRef)+", customizeInstanceGroup=")+ customizeInstanceGroup)+", scaleSizeBy=")+ scaleSizeBy)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
