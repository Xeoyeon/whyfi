import os

import requests
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from typing import List
from tqdm import tqdm
import pandas as pd

load_dotenv()

class EmbAPIError(Exception) :
    pass
class EmbTooManyRequestError(EmbAPIError) :
    pass
class EmbTooLongError(EmbTooManyRequestError) :
    pass

class BGEM3EmbeddingFunction :
    def __init__(self) :
        self._api_key_primary_val = os.environ['HYPER_PRIMARY_VAL']
        self._api_key_token =os.environ['EMB_V2_API_KEY']
        self._request_id_emb = os.environ['EMB_REQUEST_ID']

    def emb_request(self, txt) :

        emb_url = os.environ['EMB_V2_API_URL']

        data = {'text' : txt}
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key_token,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id_emb
            }
            
        req = requests.post(emb_url, headers=headers, json=data)

        if req.status_code == 200 :
            return req.json()['result']['embedding']

        else :
            if req.status_code == 429 :
                raise EmbTooManyRequestError
            else :
                raise EmbAPIError
                    
    @retry(retry = retry_if_exception_type(EmbTooManyRequestError), wait=wait_fixed(1), stop=stop_after_attempt(10))            
    def embed_query(self, document: str) : 
        embedding = self.emb_request(document)

        return embedding
    
    def embed_documents(self, documents: List[str]) :
        embeddings = [self.embed_query(document) for document in tqdm(documents)]

        return embeddings
    
    def embed_df(self, df: pd.DataFrame, col: str) :
        tqdm.pandas()
        embeddings = df.progress_apply(lambda x: self.embed_query(x[col]), axis=1)

        return embeddings
