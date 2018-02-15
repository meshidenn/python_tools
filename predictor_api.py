import requests as req
import json

from typing import Dict, Callable

def training_data_create(model_id: int, annotation: str, input_fields: Dict[str, str]) -> int:
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
    return


def model_list():
    endpoint = '/v2/models'
    
                         
