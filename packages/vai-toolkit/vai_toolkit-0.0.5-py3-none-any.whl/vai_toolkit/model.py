import requests
import json
from os.path import exists
import sys
# base_url = "http://localhost:1333/api/v1"
# base_url = "https://dev-cloud-api.virtuousai.com/api/v1"
base_url = "https://cloud-api.virtuousai.com/api/v1"

def explain(conn, datasetData, modelId, dataset):
    connCheck = conn.split(":")
    if (len(connCheck) == 2) :
        request_url = base_url + "/explain"
        headers = {"pipeline": conn.split(":")[1], "user-secret" : conn.split(":")[0]}

        payload = json.dumps({ 
            "datasetData": datasetData,
            "modelId": modelId,
            "dataset" : dataset
        })
        response = requests.post(request_url, data=payload, headers=headers)
        res = json.loads(response.text)
        if ('message' in res):
            return sys.stderr.write(res['message'])
        else :
            return res
    else :
        return sys.stderr.write("Invalid connection")

def train_model(conn,modelName, fromDate, toDate):
    connCheck = conn.split(":")
    if (len(connCheck) == 2) :
        request_url = base_url + "/train-model"
        headers = {"pipeline": conn.split(":")[1], "user-secret" : conn.split(":")[0]}
        payload = json.dumps({ 
                "title": modelName,
                "fromDate": fromDate,
                "toDate": toDate,
            })
        response = requests.post(request_url, data =payload ,headers=headers)
        res = json.loads(response.text)
        if ('message' in res):
            return sys.stderr.write(res['message'])
        else :
            return res
    else:
        return sys.stderr.write("Invalid connection")
