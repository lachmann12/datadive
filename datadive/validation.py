import json
import jsonschema


def validate(instance, schema_path):
    
    with open(schema_path) as f:
        schema = json.load(f)

    # Validate the instance against the schema
    try:
        jsonschema.validate(instance, schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False

