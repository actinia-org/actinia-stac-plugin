from flask_restful_swagger_2 import Schema


class AddCollectionModel(Schema):
    type = "object"
    properties = {
        "stac_instance_id": {"type": "string"},
        "stac_url": {"type": "string"},
    }


class AddInstaceModel(Schema):
    type = "object"
    properties = {"stac_instance_id": {"type": "string"}}
