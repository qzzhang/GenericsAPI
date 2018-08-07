
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
 * <p>Original spec-file type: MatrixFilterParams</p>
 * <pre>
 * Input of the matrix_filter function
 * matrix_obj_ref: object reference of a matrix
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "matrix_obj_ref"
})
public class MatrixFilterParams {

    @JsonProperty("matrix_obj_ref")
    private String matrixObjRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("matrix_obj_ref")
    public String getMatrixObjRef() {
        return matrixObjRef;
    }

    @JsonProperty("matrix_obj_ref")
    public void setMatrixObjRef(String matrixObjRef) {
        this.matrixObjRef = matrixObjRef;
    }

    public MatrixFilterParams withMatrixObjRef(String matrixObjRef) {
        this.matrixObjRef = matrixObjRef;
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
        return ((((("MatrixFilterParams"+" [matrixObjRef=")+ matrixObjRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
