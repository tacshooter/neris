import yaml
import json
import sys

def convert_neris_yaml(yaml_text):
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return {"error": str(exc)}

    form_schema = []
    
    for field_name, attributes in data.items():
        # Map YAML string booleans to actual booleans
        db_required = attributes.get('db_required', 'FALSE').upper() == 'TRUE'
        neris_core = attributes.get('neris_core', 'FALSE').upper() == 'TRUE'
        computed = attributes.get('computed', 'FALSE').upper() == 'TRUE'
        
        # We skip computed fields for the form engine
        if computed:
            continue
            
        field_def = {
            "id": field_name,
            "label": attributes.get('definition', field_name),
            "group": attributes.get('group', 'general'),
            "type": attributes.get('type', 'Text'),
            "required": db_required,
            "core": neris_core,
            "possible_if": attributes.get('possible_if', ''),
            "example": attributes.get('example', ''),
            "cardinality": attributes.get('cardinality', 'Single'),
            "value_set": attributes.get('value_set', 'FALSE').upper() == 'TRUE'
        }
        
        form_schema.append(field_def)
        
    return form_schema

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python neris_to_json.py <path_to_yaml>")
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        schema = convert_neris_yaml(f.read())
        print(json.dumps(schema, indent=2))
