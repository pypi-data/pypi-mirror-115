from jsonschema import validate


feature_schema = {
    "type" : "object",
    "properties" : {
        "enable" : {"type" : "boolean"},
        "default" : {"type" : "boolean"},
        "clusters" : {
            "type" : "array", 
            "items": {
            "type": "string"
            }
        },
     },
     "required": ["enable", "default", "clusters"]
}

cluster_schema = {
    "type" : "object",
    "properties" : {
        "ids" : {
            "type" : "array", 
            "items": {
            "type": "number"
            }
        },
     },
    "required": ["ids"],
}

global_schema = {
    "type": "object"
}

def validate_feature(data):
    validate(data, feature_schema)

def validate_cluster(data):
    validate(data, cluster_schema)

def validate_global(data):
    validate(data, global_schema)