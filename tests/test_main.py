import unittest

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


FIND_NODE_BY_TYPE_REQUEST = {
        'url': 'https://www.figma.com/file/GRsmqGlwbQNCn0ESzi9HWx/Delivery-App_UI-Kit-(Community)?node-id=33%3A444',
        'node_name':'',
        'node_kind': 'FRAME'
}

FIND_NODE_BY_NAME_REQUEST = {
        'url': 'https://www.figma.com/file/GRsmqGlwbQNCn0ESzi9HWx/Delivery-App_UI-Kit-(Community)?node-id=33%3A444',
        'node_name':'Splash Screen',
        'node_kind': ''
}

FIND_NODE_INVALID_REQUEST = {
        'url': 'https://www.figma.com/file/GRsmqGlwbQNCn0ESzi9HWx/Delivery-App_UI-Kit-(Community)?node-id=33%3A444',
        'node_kind': ''
}

FIND_NODE_NOTFOUND_REQUEST = {
        'url': 'https://www.figma.com/file/GRsmqGlwbQNCn0ESzi9HWx/Delivery-App_UI-Kit-(Community)?node-id=33%3A444',
        'node_name': 'Not existent name...',
        'node_kind': ''
}


class TestFindNode(unittest.TestCase):

    def test_find_node_by_type(self):
        response = client.post("/findNode", json=FIND_NODE_BY_TYPE_REQUEST)
        print(response.status_code)
        assert response.status_code == 200

    def test_find_node_by_name(self):
        response = client.post("/findNode", json=FIND_NODE_BY_NAME_REQUEST)
        print(response.status_code)
        assert response.status_code == 200

    def test_find_node_invalid_request(self):
        response = client.post("/findNode", json=FIND_NODE_INVALID_REQUEST)
        print(response.status_code)
        assert response.status_code == 422

    def test_find_node_notfound_request(self):
        response = client.post("/findNode", json=FIND_NODE_NOTFOUND_REQUEST)
        print(response.status_code)
        assert response.status_code == 404
