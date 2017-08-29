import requests as req

from retrieva.auth import add_api_signature

from typing import Dict, Callable

import json


class PredictorAPIClient:
    “”"
    PredictorのAPIクライアント
    “”"

    def __init__(
        self, model_id: int,
        api_key: str,
        secret_key: str,
        host: str
    ):
        self.model_id = model_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = ‘http://{}/predictor’.format(host)

    def training_data_create(
        self, annotation: str,
        input_fields: Dict[str, str]
    ) -> int:
        “”"
        訓練データの登録
        :param annotation: アノテーション
        :param input_fields: 入力フィールド（dictionary)
        :return: 訓練データのID
        “”"
        endpoint = ‘/v2/models/{}/training_data’.format(self.model_id)
        body_dict = {
            ‘annotation’: annotation,
            ‘data’: self._remove_undesireble_chars(input_fields)
        }
        return self._post_handle_res(endpoint, body_dict, lambda res: int(res[‘training_data_id’]))

    def _post_handle_res(
        self, endpoint: str,
        body_dict: Dict, handler: Callable
    ):
        body_data = json.dumps(body_dict)
        base_url, header = add_api_signature(
            self.base_url + endpoint, body_data, self.api_key, self.secret_key
        )
        response = req.post(base_url, data=body_data, headers=header)
        if response.status_code >= 300:
            request = response.request
            command = “curl -X {method} -H {headers} -d ‘{data}’ ‘{uri}‘”
            method = request.method
            uri = request.url
            data = request.body
            headers = [‘“{0}: {1}“‘.format(k, v) for k, v in request.headers.items()]
            headers = ” -H “.join(headers)
            print(“req: {}“.format(command.format(method=method, headers=headers, data=data, uri=uri)))
            print(“res: {}“.format(response.json()))
        return handler(response.json())

    def _remove_undesireble_chars(self, body_dict: Dict[str, str]) -> Dict[str, str]:
        #  リクエストでエラーになるため、一時的なパッチとしてパーセント文字列を除外
        return {k: body_dict[k].replace(‘%’, ‘’) for k in body_dict}