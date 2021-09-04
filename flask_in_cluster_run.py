from flask import Flask, request, jsonify
from kubernetes import client,config
import json
from bson import json_util
import os

#config.load_kube_config()
config.load_incluster_config()
apis_api = client.AppsV1Api()

app = Flask(__name__)

def drop_nones(d: dict) -> dict:
    """Recursively drop Nones in dict d and return a new dict"""
    dd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            dd[k] = drop_nones(v)
        elif isinstance(v, (list, set, tuple)):
            # note: Nones in lists are not dropped
            # simply add "if vv is not None" at the end if required
            dd[k] = type(v)(drop_nones(vv) if isinstance(vv, dict) else vv 
                            for vv in v) 
        elif v is not None:
            dd[k] = v
    return dd

@app.route('/configs', methods=['POST'])
def createConfigs():
    deployment=[]
    my_dict = {}
    request_data = request.get_json()
    namespace=request_data["metadata"]["namespace"]
    api_response =apis_api.create_namespaced_deployment(namespace, request_data)
    x=api_response.to_dict()
    json_object =json.dumps(drop_nones(x),default=json_util.default)
    loaded_r = json.loads(json_object)
    deployment.append(loaded_r)
    my_dict['deployment']=deployment
    return (my_dict)

@app.route("/configs/<namespace>/<config>", methods=["DELETE"])
def deleteConfig(namespace, config):
    deployment=[]
    my_dict = {}
    request_data = request.get_json()
    namespace=request_data["metadata"]["namespace"]
    api_response = apis_api.delete_namespaced_deployment(config, namespace)
    x=api_response.to_dict()
    json_object =json.dumps(drop_nones(x),default=json_util.default)
    loaded_r = json.loads(json_object)
    deployment.append(loaded_r)
    my_dict['deployment']=deployment
    return (my_dict)

@app.route('/configs', methods=['GET'])
def getConfigs():
    deployment=[]
    my_dict = {}
    api_response = apis_api.list_deployment_for_all_namespaces()
    for i in api_response.items:
        x=i.to_dict()
        json_object =json.dumps(drop_nones(x), default=json_util.default)
        loaded_r = json.loads(json_object)
        deployment.append(loaded_r)
        my_dict['deployment']=deployment
    return (my_dict)


@app.route('/search', methods=['GET'])
def getFieldSelectorConfigs():
    deployment=[]
    my_dict = {}
    #field_selector='metadata.name=hello'
    field_selector=request.query_string
    api_response = apis_api.list_deployment_for_all_namespaces(field_selector=field_selector,_preload_content='false',pretty = 'true')
    for i in api_response.items:
        x=i.to_dict()
        json_object =json.dumps(drop_nones(x), default=json_util.default)
        loaded_r = json.loads(json_object)
        deployment.append(loaded_r)
        my_dict['deployment']=deployment
    return (my_dict)

@app.route('/configs/<deploymentName>', methods=['GET'])
def getDeploymentConfigs(deploymentName):
    deployment=[]
    my_dict = {}
    field_selector='metadata.name={}'.format(deploymentName)
    #field_selector=request.query_string
    api_response = apis_api.list_deployment_for_all_namespaces(field_selector=field_selector,_preload_content='false',pretty = 'true')
    for i in api_response.items:
        x=i.to_dict()
        json_object =json.dumps(drop_nones(x), default=json_util.default)
        loaded_r = json.loads(json_object)
        deployment.append(loaded_r)
        my_dict['deployment']=deployment
    return (my_dict)


if __name__ == '__main__':
    PORT=os.environ.get('SERVE_PORT')
    if PORT is not None:
        app.run(host= '0.0.0.0',debug=True, port=PORT)
