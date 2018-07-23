import time
import json

from DataFileUtil.DataFileUtilClient import DataFileUtil
from biokbase.workspace.client import Workspace as workspaceService


def log(message, prefix_newline=False):
    print(('\n' if prefix_newline else '') + str(time.time()) + ': ' + message)


class GenericsUtil:

    def _validate_fetch_data_params(self, params):
        """
        _validate_fetch_data_params:
            validates params passed to fetch_data method
        """

        log('start validating fetch_data params')

        # check for required parameters
        for p in ['obj_ref', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)
        self.wsClient = workspaceService(self.ws_url)

    def fetch_data(self, params):
        """
        fetch_data: fetch generics data as pandas dataframe for a generics data object

        arguments:
        obj_ref: generics object reference
        workspace_name: the name of the workspace

        optional arguments:
        target_data_field: the data field to be retrieved from.
                           fetch_data will try to auto find this field.
                            e.g. for an given data type like below:
                            typedef structure {
                              FloatMatrix2D data;
                            } SomeGenericsMatrix;
                            data should be the target data field.

        return:
        data_matrix: a pandas dataframe
        """

        log('--->\nrunning GenericsUtil.fetch_data\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_fetch_data_params(params)

        obj_ref = params.get('obj_ref')
        workspace_name = params.get('workspace_name')

        returnVal = dict()

        return returnVal
