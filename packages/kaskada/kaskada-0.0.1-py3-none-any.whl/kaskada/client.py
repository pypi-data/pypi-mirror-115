"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from __future__ import print_function
import logging

import grpc
import http.client
import json

import kaskada.api.v1alpha.compute_pb2_grpc as compute_grpc
import kaskada.api.v1alpha.table_pb2_grpc as table_grpc
import kaskada.api.v1alpha.view_pb2_grpc as view_grpc

class Client(object):
    LEGACY_ENGINE = 'LEGACY'

    class AccessToken(object):
        def __init__(self, json_data: str):
            data = json.loads(json_data)
            if 'access_token' not in data and 'expires_in' not in data and 'token_type' not in data:
                raise PermissionError('Unable to validate access token. Token details: {}'.format(json_data))
            self.access_token = data['access_token']
            self.expires_in = data['expires_in']
            self.token_type = data['token_type']

    def getBearerToken(endpoint: str, audience: str, client_id: str, client_secret: str):
        conn = http.client.HTTPSConnection(endpoint)
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'audience': audience, 
            'grant_type': 'client_credentials',
        }
        headers = {
            'content-type': 'application/json',
        }
        conn.request('POST', '/oauth/token', json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        return Client.AccessToken(data)

    def __init__(self, metadata: [(str, str)], **kwags):
        engine = kwags.pop('engine', None)
        endpoint = kwags.pop('endpoint', 'api.kaskada.com:50051')
        is_secure = kwags.pop('is_secure', True)
        if is_secure:
            channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
        else:
            channel = grpc.insecure_channel(endpoint)
        self.computeStub = compute_grpc.ComputeServiceStub(channel)
        self.tableStub = table_grpc.TableServiceStub(channel)
        self.viewStub = view_grpc.ViewServiceStub(channel)
        self.metadata = metadata
        if engine is not None:
            self.metadata.append(('x-engine', engine))

    def authorized(**kwags):
        credentials_exchange_endpoint = kwags.pop('exchange_endpoint', 'prod-kaskada.us.auth0.com')
        credentials_audience = kwags.pop('audience', 'https://api.prod.kaskada.com')
        client_id = kwags.pop('client_id')
        client_secret = kwags.pop('client_secret')
        token = Client.getBearerToken(credentials_exchange_endpoint, credentials_audience, client_id, client_secret)
        metadata = [('authorization', token.access_token)]
        return Client(metadata, **kwags)

    def demo_only(**kwags):
        client_id = kwags.pop('client_id', 'lWYFx0020u4oulh7Z9UB8C5YXVRHNyk4')
        metadata = [('client-id', client_id)]
        return Client(metadata, **kwags)
