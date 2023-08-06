"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from kaskada.client import Client
import kaskada
import kaskada.api.v1alpha.table_pb2 as table_pb

import datetime
import grpc
import io
import os
import pandas as pd
import random
import requests
import tempfile


def list_tables(**kwargs):
    """
    Lists all the tables
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.ListTablesRequest(**kwargs)
        return client.tableStub.ListTables(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def get_table(**kwargs):
    """
    Gets a table by name
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.GetTableRequest(**kwargs)
        return client.tableStub.GetTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def create_table(**kwargs):
    """
    Creates a table
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.CreateTableRequest(table = table_pb.Table(**kwargs))
        return client.tableStub.CreateTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def delete_table(**kwargs):
    """
    Deletes a table
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = table_pb.DeleteTableRequest(**kwargs)
        return client.tableStub.DeleteTable(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def upload_data(client: Client, table_name: str, f: io.BufferedReader, file_name: str):
    """
    Generic upload data to a table
    """
    try:
        kaskada.validate_client(client)
        upload_url_req = table_pb.GetUploadUrlRequest(
            table_name = table_name,
            file_name = file_name
        )

        upload_url_res = client.tableStub.GetUploadUrl(upload_url_req, metadata=client.metadata)

        upload_url = upload_url_res.url
        headers = {'X-Amz-Meta-Filename': file_name}
        http_response = requests.put(upload_url, headers=headers, data=f)

        # TODO: Determine the return model of this method
        if http_response.status_code == 200:
            return 'Success'
        return 'Unable to upload file. Resulted in status code: {} and message: {}'.format(http_response.status_code, http_response.content)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def upload_file(table_name: str, file_path: str, client=None):
    """
    Uploads a file to a table
    """
    if not client:
        client = kaskada.KASKADA_DEFAULT_CLIENT
    f = open(file_path, 'rb')
    file_name = os.path.basename(f.name)
    return upload_data(client, table_name, f, file_name,)

def upload_dataframe(table_name: str, df: pd.DataFrame, client=None):
    """
    Uploads a dataframe to a table (converts to parquet then uploads)
    """
    if not client:
        client = kaskada.KASKADA_DEFAULT_CLIENT
    with tempfile.TemporaryDirectory() as tmpdirname:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        base_name = "{}_{}.parquet".format(current_time, random.randint(0, 1000))
        file_name = os.path.join(tmpdirname, base_name)
        # write to tempfile in `tmpdirname`
        df.to_parquet(file_name, version="2.0")
        # upload tempfile from `tmpdirname`
        return upload_data(client, table_name, open(file_name, "rb"), base_name)
