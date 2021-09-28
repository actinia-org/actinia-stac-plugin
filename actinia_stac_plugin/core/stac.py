 
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

import json 
import requests
from actinia_core.core.common.redis_base import RedisBaseInterface
from actinia_core.core.common.config import Configuration
from actinia_stac_plugin.core.stac_redis_interface import redis_actinia_interface
from stac_validator import stac_validator
import re

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

def defaultInstance():
    
    redis_actinia = connectRedis()
    exist = redis_actinia_interface.exists("defaultStac")

    defaultStac = {
            "stac.defaultStac.rastercube.landsat-8": { 
                "root": "https://landsat-stac.s3.amazonaws.com/landsat-8-l1/catalog.json",
                "href": "/api/v1/stac/collections/stac.defaultStac.rastercube.landsat-8",
                },
            "stac.defaultStac.rastercube.sentinel-2": { 
                "root": "https://sentinel-stac.s3.amazonaws.com/sentinel-2-l1c/catalog.json",
                "href": "/api/v1/stac/collections/stac.defaultStac.rastercube.sentinel-2"
                }
        }
    
    if(exist):
        return redis_actinia_interface.read("defaultStac") 
    else:
        redis_actinia_interface.create("defaultStac",defaultStac)
        return redis_actinia_interface.read("defaultStac")

def createStacItemList():
    redis_actinia = connectRedis()
    exist = redis_actinia_interface.exists("stac_instances")
    
    if not exist:
        collections = defaultInstance()
        redis_actinia_interface.create("stac_instances",{"defaultStac":{
            "path": "stac.defaultStac.rastercube.<stac_collection_id>"
        }})
    
    instances = redis_actinia_interface.read("stac_instances")

    string_respose = instances
    
    return string_respose

def createStacCollectionsList():
    redis_actinia = connectRedis()
    stac_inventary = {}
    exist = redis_actinia_interface.exists("stac_instances")
    
    if exist:
        instances = redis_actinia_interface.read("stac_instances")
        for k,v in instances.items():
            collections = redis_actinia_interface.read(k)
            stac_inventary[k] = collections
    else:
        collections = defaultInstance()
        stac_inventary["defaultStac"] = collections
        redis_actinia_interface.create("stac_instances",{"defaultStac":{
            "path": "stac.defaultStac.rastercube.<stac_collection_id>"
        }})
    
    instances = redis_actinia_interface.read("stac_instances")

    string_respose = stac_inventary
    
    return string_respose

def resolveCollectionURL(url):
    collection_url = url

    stac = stac_validator.StacValidate(url)
    stac.run()
    type = stac.message[0]['asset_type']
    if type == "COLLECTION":
            collection_url = url
    
    return collection_url

def addStac2User(jsonParameters): 
    """
        Add the STAC Catalog to redis 
            1. Update the catalog to the initial list GET /stac
            2. Store the JSON as a new variable in redis
    """
    # Initializing Redis
    redis_actinia = connectRedis()
    
    #Splitting the inputs
    stac_instance_id = jsonParameters['stac-instance-id']
    stac_collection_id = jsonParameters['stac-collection-id']
    stac_root = resolveCollectionURL(jsonParameters['stac-url'])
    stac_unique_id = "stac."+ stac_instance_id +".rastercube."+ stac_collection_id
    
    # Caching JSON from the STAC collection
    stac_json_collection =  requests.get(stac_root)
    redis_actinia_interface.create(stac_unique_id,stac_json_collection)
    
    # Verifying the existance of the instances - Adding the item to the Default List
    list_instances_exist = redis_actinia_interface.exists("stac_instances")
    if not list_instances_exist:
        defaultInstance() 
    
    stac_instance_exist= redis_actinia_interface.exists(stac_instance_id)

    if not stac_instance_exist:
        redis_actinia_interface.create(stac_instance_id,{})

    defaultJson = redis_actinia_interface.read(stac_instance_id)

    instances_list = redis_actinia_interface.read("stac_instances")

    instances_list[stac_instance_id] = {
       "path": "stac."+ stac_instance_id+".rastercube.<stac_collection_id>"
    }

    defaultJson[stac_unique_id] = {
        'root': stac_root,
        'href': "api/v1/stac/collections/" + stac_unique_id
    }

    list_of_instances_updated = redis_actinia_interface.update("stac_instances",instances_list)
    instance_updated = redis_actinia_interface.update(stac_instance_id,defaultJson)

    if instance_updated and list_of_instances_updated:
        response = {
            "message": "The STAC Collection has been added successfully",
            "StacCatalogs": redis_actinia_interface.read(stac_instance_id)
        }
    else: 
        response = {"message": "Something went wrong, please check the stac-instance-id , stac-url or stac-collection-id given"}
        
    return response

def collectionValidation(url: str) -> bool:
    """
        Verify that the URL provided belong to a STAC endpoint
    """
    stac = stac_validator.StacValidate(url)
    stac.run()
    valid = stac.message[0]['valid_stac']
    type = stac.message[0]['asset_type']
    if valid and type == "COLLECTION":
         return True
    else: 
        return False

def addStacValidator(json):
    """
        The function validate the inputs syntax and STAC validity  
        Input:
            - json - JSON array with the Instance ID , Collection ID and STAC URL 
    """
    stac_instance_id = 'stac-instance-id' in json
    stac_collecion_id = 'stac-collection-id' in json
    stac_root = 'stac-url' in json
    msg = {}
    if stac_instance_id and stac_collecion_id and stac_root:
        root_validation = collectionValidation( json['stac-url'])
        collection_validation = (re.match('^[a-zA-Z0-9-_]*$',json['stac-collection-id']))
        instance_validation = (re.match('^[a-zA-Z0-9-_]*$',json['stac-instance-id']))
        
        if root_validation and instance_validation and collection_validation:
            return addStac2User(json)
        elif not root_validation:
            msg["Error-root"] = {"message": "Please check the URL provided (Should be a STAC Catalog) as well as the name given (no spaces or undercore characters)."}
        elif not collection_validation:
            msg["Error-collection"] = {"message": "Please check the URL provided (Should be a STAC Catalog)."}
        elif not instance_validation:
            msg["Error-instance"] = {"message": "Please check the ID given (no spaces or undercore characters)."}
        
        return msg
    else:
        return {"message": "The JSON give does not have either stac-instance-id or stac-collection-id or stac-url . Check the parameters provided"}

def callStacCollection(collection: str):
    try:
        stac = redis_actinia_interface.read(collection)
    except:
        stac = {"Error":"Something went wrong, please check the collection to retrived"}
    
    return stac

def callStacCatalog(collection: str, catalog: str):
    try:
        stac_dict = redis_actinia_interface.read(collection)
        stac_root_url = stac_dict[catalog]['root']
        response = requests.get(stac_root_url)
        stac = response.content
    except:
        stac = {"Error":"Something went wrong, please check the collection and catalog to retrived"}
    
    return stac

def deleteStac(json):
    stac_instance_id = 'stac-instance-id' in json
    stac_collecion_id = 'stac-collection-id' in json

    if stac_instance_id and stac_collecion_id:
        return deleteStacCollection(json['stac-instance-id'],json['stac-collection-id'])
    elif not stac_collecion_id and stac_instance_id:
        return deleteStacInstance(json['stac-instance-id'])
    elif not stac_instance_id and stac_collecion_id:
        return {"Error":"The parameter stac-instance-id is required"}
    else:
        return {"Error":"The parameter does not match stac-instance-id or stac-collection-id"}

def deleteStacCollection(stac_instance_id:str, stac_collection_id : str):
    redis_actinia = connectRedis()
    try:
        stac_instance = redis_actinia_interface.read(stac_instance_id)
        del stac_instance[stac_collection_id]
        redis_actinia_interface.update(stac_instance_id,stac_instance)
    except:
        return {"Error": "Please check that the parameters given are well typed and exist"}

    return redis_actinia_interface.read(stac_instance_id)

def deleteStacInstance(stac_instance_id:str):
    redis_actinia = connectRedis()
    try:
        redis_actinia_interface.delete(stac_instance_id)
        instances = redis_actinia_interface.read("stac_instances")
        del instances[stac_instance_id]
        redis_actinia_interface.update("stac_instances",instances)
    except:
        return {"Error": "Something went wrong please that the element is well typed"}
    return {"message": "The instance --"+ stac_instance_id + "-- was deleted with all the collections stored inside"}