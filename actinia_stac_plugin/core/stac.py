 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
GRASS GIS module viewer
* List all modules
* Describe single module
"""

__license__ = "Apache-2.0"
__author__ = "Anika Bettge, Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Anika Bettge, Carmen Tawalika"

from requests.models import Response
from actinia_stac_plugin.api.stac import StacCatalog
import json 
import requests
from actinia_core.core.common.redis_base import RedisBaseInterface
from actinia_core.core.common.config import Configuration
from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface

global DefaultStacConf

def connectRedis():
    """This method initializes the connection with redis.
    """
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        pass

    server = conf.REDIS_SERVER_URL
    port = conf.REDIS_SERVER_PORT
    if conf.REDIS_SERVER_PW:
        redis_password = conf.REDIS_SERVER_PW
    else:
        redis_password = None

    redis_actinia_interface.connect(
        host=server, port=port, password=redis_password)

    return redis_actinia_interface

def globalDefine():
    redis_actinia = connectRedis()

    exist = redis_actinia_interface.exists("defaultStac")

    defaultStac = {
            "element84": { 
                "root": "https://earth-search.aws.element84.com/v0",
                "href": "/api/v1/stac/Sentinel-2A"
                },
            "landsat-8": { 
                "root": "https://landsat-stac.s3.amazonaws.com/landsat-8-l1/catalog.json",
                "href": "/api/v1/stac/landsat-8",
                },
            "sentinel-2": { 
                "root": "https://sentinel-stac.s3.amazonaws.com/catalog.json",
                "href": "/api/v1/stac/sentinel-2a"
                }
        }
    
    if(exist):
        return redis_actinia_interface.read("defaultStac") 
    else:
        redis_actinia_interface.create("defaultStac",defaultStac)

        return redis_actinia_interface.read("defaultStac") 

def createStacList():
    response = globalDefine()
    
    string_respose = response

    return string_respose

def addStac2User(jsonParameters): 

    #Splitting the inputs
    actinia_id = jsonParameters['stac_id']
    actinia_root = jsonParameters['stac_url']
    
    # Caching JSON from the STAC collection
    stac_json_collection =  requests.get(actinia_root)
    redis_actinia_interface.create(actinia_id,actinia_root,stac_json_collection)
    
    # Adding the item to the Default List
    defaultJson = redis_actinia_interface.read("defaultStac")
    defaultJson[actinia_id] = {
        'root': actinia_root,
        'href': 'api/v1/'+ actinia_id
    }
    updated = redis_actinia_interface.update("defaultStac",defaultJson)

    if updated:
        response = {
            "message": "The STAC Catalog has been added successfully",
            "StacCatalogs": redis_actinia_interface.read("defaultStac")
        }
    else: 
        response = {"message": "Something happen, please check the stac_url or stac_id given"}
        
    return response

def callStacCatalog(catalog: str):
    stac_dict = redis_actinia_interface.read("defaultStac")

    try:
        stac_root_url = stac_dict[catalog]['root']
        response = requests.get(stac_root_url)
        stac = response.content
    except:
        stac = {"Error":"Something went wrong, please check the catalog to retrived"}
    
    return stac
