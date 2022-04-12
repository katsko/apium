import json
from uuid import uuid4


class RpcTestingClient():

    def __init__(self, url, django_client):
        self.url = url
        self.django_client = django_client

    def __getattr__(self, rpc_method):

        def send_post(**kwargs):
            payload = json.dumps({
                'jsonrpc': '2.0',
                'method': rpc_method,
                'params': kwargs,
                'id': str(uuid4()),
            })
            response = self.django_client.post(
                self.url,
                payload,
                content_type='application/json',
            ).json()
            return response

        return send_post
