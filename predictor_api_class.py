import requests as req
import json

from typing import Dict, Callable

class PredictorAPIClient:
    """
    PredictorのAPIクライアント
    """

    def __init__(self, model_id, api_key, host):
        self.model_id = model_id
        self.api_key = api_key
        self.base_url = 'http://{}/predictor'.format(host)

    def model_list(self, page = 1, per_page = 10):
        endpoint = '/v2/models'
        params = {
            'page': page,
            'per_page': per_page
        }
        return self._get_handle_res(endpoint, params)

    def model_get(self):
        endpoint = '/v2/models/{}'.format(self.model_id)
        return self._get_handle_res(endpoint)

    def model_create(self, model_conf):
        endpoint = '/v2/models'
        return self._post_handle_res(endpoint, body_dict=model_conf)
    
    def model_update(self, update_conf):
        endpoint = '/v2/models/{}'.format(self.model_id)
        return self._put_handle_res(endpoint, body_dict=update_conf)

    def model_delete(self):
        endpoint = '/v2/models/{}'.format(self.model_id)
        return self._delete_handle_res(endpoint)

    def config_list(self,  page = 1, per_page = 10):
        endpoint = '/v2/models/{}/configs'.format(self.model_id)
        params = {
            'page': page,
            'per_page': per_page
        }
        return self._get_handle_res(endpoint, params)

    def config_get(self, config_id):
        endpoint = '/v2/models/{0}/configs/{1}'.format(self.model_id, config_id)
        return self._get_handle_res(endpoint)

    def config_create(self, create_conf):
        endpoint = '/v2/models/{}/config'.format(self.model_id)
        return self._post_handle_res(endpoint, create_conf)

    def config_update(self, config_id, update_conf):
        endpoint = '/v2/models/{0}/config/{1}'.format(self.model_id, config_id)
        return self._put_handle_res(endpoint, update)

    def config_delete(self, config_id):
        endpoint = '/v2/models/{0}/configs/{1}'.format(self.model_id, config_id)
        return self._delete_handle_res(endpoint)

    def config_query(self, config_id, data):
        endpoint = '/v2/models/{0}/configs/{1}/query'.format(self.model_id, config_id)
        return self._post_handle_res(endpoint, body_dict=data)
    
    def training_data_create(self, annotation, input_fields, update_conf):
        """
        訓練データの登録
        :param annotation: アノテーション
        :param input_fields: 入力フィールド(dictionary)
        :return: 訓練データのID
        """
        endpoint = '/v2/models/{}/training_data'.format(self.model_id)
        body_dict = {
            'annotation': annotation,
            'data': input_fields
        }
        return self._post_handle_res(endpoint, body_dict)

    def _get_handle_res(self, endpoint, params=None):
        api_key = 'api_key={}'.format(self.api_key)
        if params:
            parameter= '&'.join(['{}={}'.format(k,v) for k, v in params.items()])
            base_url = self.base_url + endpoint + '?' + api_key + '&' + parameter
        else:
            base_url = self.base_url + endpoint + '?' + api_key
        response = req.get(base_url)
        return response.json()


    def _post_handle_res(self, endpoint, body_dict,  params=None):
        body_data = json.dumps(body_dict)
        headers = {'content-type': 'application/json'}
        api_key = 'api_key={}'.format(self.api_key)
        if params:
            parameter= '&'.join(['{}={}'.format(k,v) for k, v in params.items()])
            base_url = self.base_url + endpoint + '?' + api_key + '&' + parameter
        else:
            base_url = self.base_url + endpoint + '?' + api_key
        response = req.post(base_url, data=body_data, headers=headers)
        return response.json()

    def _put_handle_res(self, endpoint, body_dict, params=None):
        body_data = json.dumps(body_dict)
        headers = {'content-type': 'application/json'}
        api_key = 'api_key={}'.format(self.api_key)
        if params:
            parameter= '&'.join(['{}={}'.format(k,v) for k, v in params.items()])
            base_url = self.base_url + endpoint + '?' + api_key + '&' + parameter
        else:
            base_url = self.base_url + endpoint + '?' + api_key
        response = req.put(base_url, data=body_data, headers=headers)
        return response.json()
        
    def _delete_handle_res(self, endpoint, params=None):
        api_key = 'api_key={}'.format(self.api_key)
        base_url = self.base_url + endpoint + '?' + api_key
        response = req.delete(base_url)
        return response.json()
            
                         
