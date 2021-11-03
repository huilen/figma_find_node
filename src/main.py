import uvicorn
import requests
import json
import re

from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException


FIGMA_URL = 'https://api.figma.com/v1'
FIGMA_AUTH_TOKEN = '258480-b2f63765-38a3-4755-b282-dda8f191b9c3'

app = FastAPI()


class FindNodeRequestModel(BaseModel):
    url: str
    node_name: str
    node_kind: str


def find_in_node_tree(key, value, node_tree):
    children = node_tree.get('children')

    if node_tree[key] == value:
        return children

    if not children:
        return None

    for child in children:
        exists = find_in_node_tree(key, value, child)
        if exists:
            return child['children']


@app.post('/findNode')
async def find_node(params: FindNodeRequestModel):
    # get node key from url field
    matches = re.search('/file/(.*)/', params.url)
    if not matches:
        raise HTTPException(status_code=400, detail="Invalid URL")
    key = matches[1]

    # get file nodes from figma for that key
    headers = {'X-Figma-Token': FIGMA_AUTH_TOKEN}
    url = FIGMA_URL + '/files/{key}'.format(key=key)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error in Figma API")
    node_tree = json.loads(response.content)['document']

    # find node by name or kind 
    node = None
    if params.node_name:
        node = find_in_node_tree('name', params.node_name, node_tree)
    elif params.node_kind:
        node = find_in_node_tree('type', params.node_kind, node_tree)

    if not node:
        raise HTTPException(status_code=404, detail='Node not found')

    return node


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
