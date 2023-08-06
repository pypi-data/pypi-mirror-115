"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from kaskada.client import Client
import kaskada
import kaskada.api.v1alpha.view_pb2 as view_pb

import grpc

def list_views(**kwargs):
    """
    Lists all the views
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = view_pb.ListViewsRequest(**kwargs)
        return client.viewStub.ListViews(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)


def get_view(**kwargs):
    """
    Get a view by name
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = view_pb.GetViewRequest(**kwargs)
        return client.viewStub.GetView(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def create_view(**kwargs):
    """
    Creates a view
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = view_pb.CreateViewRequest(view = view_pb.View(**kwargs))
        return client.viewStub.CreateView(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)

def delete_view(**kwargs):
    """
    Deletes a view
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        req = view_pb.DeleteViewRequest(**kwargs)
        return client.viewStub.DeleteView(req, metadata=client.metadata)
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)
