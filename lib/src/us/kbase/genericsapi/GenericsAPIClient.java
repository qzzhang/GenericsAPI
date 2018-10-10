package us.kbase.genericsapi;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: GenericsAPI</p>
 * <pre>
 * </pre>
 */
public class GenericsAPIClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public GenericsAPIClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public GenericsAPIClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenericsAPIClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenericsAPIClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: fetch_data</p>
     * <pre>
     * fetch_data: fetch generics data as pandas dataframe for a generics data object
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.FetchDataParams FetchDataParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.FetchDataReturn FetchDataReturn}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public FetchDataReturn fetchData(FetchDataParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<FetchDataReturn>> retType = new TypeReference<List<FetchDataReturn>>() {};
        List<FetchDataReturn> res = caller.jsonrpcCall("GenericsAPI.fetch_data", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_matrix</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ExportParams ExportParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportMatrix(ExportParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("GenericsAPI.export_matrix", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: validate_data</p>
     * <pre>
     * validate_data: validate data
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ValidateParams ValidateParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.ValidateOutput ValidateOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ValidateOutput validateData(ValidateParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ValidateOutput>> retType = new TypeReference<List<ValidateOutput>>() {};
        List<ValidateOutput> res = caller.jsonrpcCall("GenericsAPI.validate_data", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: import_matrix_from_excel</p>
     * <pre>
     * import_matrix_from_excel: import matrix object from excel
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ImportMatrixParams ImportMatrixParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.ImportMatrixOutput ImportMatrixOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ImportMatrixOutput importMatrixFromExcel(ImportMatrixParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ImportMatrixOutput>> retType = new TypeReference<List<ImportMatrixOutput>>() {};
        List<ImportMatrixOutput> res = caller.jsonrpcCall("GenericsAPI.import_matrix_from_excel", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: save_object</p>
     * <pre>
     * save_object: validate data constraints and save matrix object
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.SaveObjectParams SaveObjectParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.SaveObjectOutput SaveObjectOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SaveObjectOutput saveObject(SaveObjectParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<SaveObjectOutput>> retType = new TypeReference<List<SaveObjectOutput>>() {};
        List<SaveObjectOutput> res = caller.jsonrpcCall("GenericsAPI.save_object", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: search_matrix</p>
     * <pre>
     * search_matrix: generate a HTML report that allows users to select feature ids
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.MatrixSelectorParams MatrixSelectorParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.MatrixSelectorOutput MatrixSelectorOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public MatrixSelectorOutput searchMatrix(MatrixSelectorParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<MatrixSelectorOutput>> retType = new TypeReference<List<MatrixSelectorOutput>>() {};
        List<MatrixSelectorOutput> res = caller.jsonrpcCall("GenericsAPI.search_matrix", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: filter_matrix</p>
     * <pre>
     * filter_matrix: create sub-matrix based on input filter_ids
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.MatrixFilterParams MatrixFilterParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.MatrixFilterOutput MatrixFilterOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public MatrixFilterOutput filterMatrix(MatrixFilterParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<MatrixFilterOutput>> retType = new TypeReference<List<MatrixFilterOutput>>() {};
        List<MatrixFilterOutput> res = caller.jsonrpcCall("GenericsAPI.filter_matrix", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: file_to_attribute_mapping</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.FileToAttributeMappingParams FileToAttributeMappingParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.FileToAttributeMappingOutput FileToAttributeMappingOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public FileToAttributeMappingOutput fileToAttributeMapping(FileToAttributeMappingParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<FileToAttributeMappingOutput>> retType = new TypeReference<List<FileToAttributeMappingOutput>>() {};
        List<FileToAttributeMappingOutput> res = caller.jsonrpcCall("GenericsAPI.file_to_attribute_mapping", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: attribute_mapping_to_tsv_file</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.AttributeMappingToTsvFileParams AttributeMappingToTsvFileParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.AttributeMappingToTsvFileOutput AttributeMappingToTsvFileOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public AttributeMappingToTsvFileOutput attributeMappingToTsvFile(AttributeMappingToTsvFileParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<AttributeMappingToTsvFileOutput>> retType = new TypeReference<List<AttributeMappingToTsvFileOutput>>() {};
        List<AttributeMappingToTsvFileOutput> res = caller.jsonrpcCall("GenericsAPI.attribute_mapping_to_tsv_file", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_attribute_mapping_tsv</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ExportObjectParams ExportObjectParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportAttributeMappingTsv(ExportObjectParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("GenericsAPI.export_attribute_mapping_tsv", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_attribute_mapping_excel</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ExportObjectParams ExportObjectParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportAttributeMappingExcel(ExportObjectParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("GenericsAPI.export_attribute_mapping_excel", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_cluster_set_excel</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ExportObjectParams ExportObjectParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportClusterSetExcel(ExportObjectParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("GenericsAPI.export_cluster_set_excel", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: export_corr_matrix_excel</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.ExportObjectParams ExportObjectParams}
     * @return   parameter "result" of type {@link us.kbase.genericsapi.ExportOutput ExportOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ExportOutput exportCorrMatrixExcel(ExportObjectParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ExportOutput>> retType = new TypeReference<List<ExportOutput>>() {};
        List<ExportOutput> res = caller.jsonrpcCall("GenericsAPI.export_corr_matrix_excel", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: compute_correlation_matrix</p>
     * <pre>
     * compute_correlation_matrix: create sub-matrix based on input filter_ids
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.CompCorrParams CompCorrParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.CompCorrOutput CompCorrOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public CompCorrOutput computeCorrelationMatrix(CompCorrParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<CompCorrOutput>> retType = new TypeReference<List<CompCorrOutput>>() {};
        List<CompCorrOutput> res = caller.jsonrpcCall("GenericsAPI.compute_correlation_matrix", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: build_network</p>
     * <pre>
     * build_network: filter correlation matrix and build network
     * </pre>
     * @param   params   instance of type {@link us.kbase.genericsapi.BuildNetworkParams BuildNetworkParams}
     * @return   parameter "returnVal" of type {@link us.kbase.genericsapi.BuildNetworkOutput BuildNetworkOutput}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public BuildNetworkOutput buildNetwork(BuildNetworkParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<BuildNetworkOutput>> retType = new TypeReference<List<BuildNetworkOutput>>() {};
        List<BuildNetworkOutput> res = caller.jsonrpcCall("GenericsAPI.build_network", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("GenericsAPI.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
