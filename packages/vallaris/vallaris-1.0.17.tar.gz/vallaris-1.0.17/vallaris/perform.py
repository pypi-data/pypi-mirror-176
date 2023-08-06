################# Vallaris Maps ##################
############## By : sattawat arab ###############
###### GIS Backend Engineer #########
########### i-bitz company limited ##############
##################### 2020 ######################

import time
import tempfile
import os
import json
import requests
from geopandas import GeoSeries
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from vallaris.utils import *
from IPython.display import IFrame
from urllib.request import urlretrieve
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()



def setEnviron(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)

    try:
        msgBody = json.loads(parameter)
    except:
        msgBody = parameter

    try:
        GP_API_FEATURES_HOST = os.environ.get(
            'GP_API_FEATURES_HOST', 'https://v2k-dev.vallarismaps.com/core/api/features')
        url = GP_API_FEATURES_HOST.split("/")[-4]
        Api_Key = msgBody["API-Key"]
        VallarisServer = GP_API_FEATURES_HOST

        if 'APIKey' in os.environ:
            del os.environ['APIKey']

        if 'VallarisServer' in os.environ:
            del os.environ['VallarisServer']

        os.environ["APIKey"] = Api_Key
        os.environ["VallarisServer"] = VallarisServer

    except:
        Api_Key = os.environ["APIKey"]
        VallarisServer = os.environ["VallarisServer"]

    return [Api_Key, VallarisServer]


def InputValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def OverlayValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][1]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][1]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def FileValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        file = str(input) + ".gpkg"
        return file
    except Exception as e:
        print(e)
        file = False
        return file


def FormatValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        return format
    except Exception as e:
        print(e)
        format = False
        return format


def ParamValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        param = msgOption['process']['inputs']['parameter'][0]['input']
        return param
    except Exception as e:
        print(e)
        param = False
        return param


def CollectionValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['process']['inputs']['input'][0]['input']
        dataset_id = collection[0]['value']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataCollection = getData(storage, dataset_id, VallarisServer, Api_Key)

        if dataCollection != "something wrong":
            input = dataCollection
            return input

        else:
            input = False
            return input
    except Exception as e:
        print(e)
        input = False
        return input


def ExportFeatures(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataExport = getExport(dataset_id, VallarisServer, Api_Key)
        return dataExport

    except Exception as e:
        print(e)
        dataExport = False
        return dataExport


def CreateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        data = msgOption['data']
        dirpath = tempfile.mkdtemp()

        dataImport = getImport(dataset_id,
                               data, VallarisServer, Api_Key)
        shutil.rmtree(dirpath)

        if dataImport != "something wrong":
            return dataImport

        else:
            dataImport = False
            return dataImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def UpdateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        data = msgOption['data']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataEdit = editFeatures(dataset_id,
                                features_id, data,  VallarisServer, Api_Key)

        if dataEdit != "something wrong":
            return dataEdit

        else:
            dataEdit = False
            return dataEdit

    except Exception as e:
        print(e)
        dataEdit = False
        return dataEdit


def DeleteFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataDelete = delFeatures(
            dataset_id, features_id,  VallarisServer, Api_Key)

        if dataDelete != "something wrong":
            return dataDelete

        else:
            dataDelete = False
            return dataDelete

    except Exception as e:
        print(e)
        dataDelete = False
        return dataDelete


def CreateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataNew = newCollection(
            title, description, itemType, VallarisServer, Api_Key)

        if dataNew != "something wrong":
            return dataNew

        else:
            dataNew = False
            return dataNew

    except Exception as e:
        print(e)
        dataNew = False
        return dataNew


def UpdateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        editImport = editCollection(
            dataset_id, title, description, itemType, VallarisServer, Api_Key)

        if editImport != "something wrong":
            return editImport

        else:
            editImport = False
            return editImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def DeleteCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        deleteData = delCollection(dataset_id, VallarisServer, Api_Key)

        if deleteData != "something wrong":
            return deleteData

        else:
            deleteData = False
            return deleteData

    except Exception as e:
        print(e)
        deleteData = False
        return deleteData


def CreateTile(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption["data_filter"]['dataset_id']
        dataset_out = msgOption["data_filter"]['dataset_out']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        tile = makeTile(dataset_id, dataset_out,
                        VallarisServer, Api_Key, parameter)

        if tile != "something wrong":
            return tile

        else:
            tile = False
            return tile

    except Exception as e:
        print(e)
        tile = False
        return tile


def ProcessSuccess(storage, parameter, msg, data):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    msgOption = msgBody
    _output = msgOption['process']['outputs'][0]['format']

    try:
        order = msgOption['process']['order']
    except:
        order = 1

    if "GeoJSON" in _output:
        _output = 'json'

    data.to_file(storage + '/' + str(_output) +
                 str(order) + ".gpkg", driver="GPKG")

    file_final_up = storage + '/' + str(_output) + str(order) + '.gpkg'
    out_msg = {
        "code": 200,
        "message": msg,
        "file": file_final_up
    }
    return json.dumps(out_msg)


def ProcessFail(storage, parameter, msg):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    out_msg = {
        "code": 404,
        "message": msg,
        "file": "no data"
    }

    print("process failed")
    return json.dumps(out_msg)

def RenderFeatures(parameter):
    data_out = parameter['data']
    features = data_out['geometry'].to_json()

    VallarisServer = os.environ["VallarisServer"]
    HOST = VallarisServer

    data_items = {"features":[{
        "id":"Polygon",
        "data":features,
        "layer_type":["polygon"],"paint":{"opacity":0.4}
    }]}
    
    params = json.dumps(data_items)
    
    mydict = {'params': params,'center':[
            ],'z':1,'p':0}

    qstr = urlencode(mydict)   

    mapURL = '/sandbox/render/iframe?'

    url =HOST + mapURL + qstr

    out_iframe = IFrame(url, '100%', '336px')

    return out_iframe
