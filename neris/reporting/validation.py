import json
import os
from django.conf import settings

class NerisValidator:
    def __init__(self):
        # The JSON schemas we generated are in the neris/ folder
        self.schema_dir = os.path.join(settings.BASE_DIR, 'neris')

    def load_schema(self, module_name):
        path = os.path.join(self.schema_dir, f"{module_name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None

    def validate_incident(self, data):
        """
        Validates the raw incident data against NERIS schemas.
        Returns a list of structured errors/warnings.
        """
        errors = []
        
        # 1. Validate against the Core Incident Schema
        core_schema = self.load_schema('core_mod_incident')
        if not core_schema:
            return [{'level': 'error', 'message': 'System Error: Core schema missing from server'}]

        self._validate_recursive(core_schema, data, errors)
        
        return errors

    def _validate_recursive(self, schema, data, errors, prefix=""):
        for field in schema:
            field_id = field['id']
            # If the field is a Module, the data might be nested
            # If the field is a standard type, it's a direct key
            val = data.get(field_id)
            
            is_missing = val is None or val == "" or (isinstance(val, list) and len(val) == 0)
            
            # Visibility Check (Placeholder: In production, we'd evaluate 'possible_if' here)
            
            if is_missing:
                if field.get('required'):
                    errors.append({
                        'field': f"{prefix}{field_id}",
                        'label': field.get('label'),
                        'level': 'error',
                        'message': 'Required for database acceptance.'
                    })
                elif field.get('core'):
                    errors.append({
                        'field': f"{prefix}{field_id}",
                        'label': field.get('label'),
                        'level': 'warning',
                        'message': 'Required for a complete NERIS record.'
                    })
            
            # If it's a Module and has data, validate its sub-fields
            if not is_missing and field['type'] == 'Module':
                # Try to load the module schema (e.g. mod_fire)
                nested_schema_name = f"mod_{field_id}"
                nested_schema = self.load_schema(nested_schema_name)
                if nested_schema:
                    self._validate_recursive(nested_schema, val, errors, f"{prefix}{field_id}.")

            # If it's an Array of Modules (e.g. Medical Patients)
            if not is_missing and field['type'] == 'Array[Module]':
                nested_schema_name = f"mod_{field_id}"
                nested_schema = self.load_schema(nested_schema_name)
                if nested_schema:
                    for i, item in enumerate(val):
                        self._validate_recursive(nested_schema, item, errors, f"{prefix}{field_id}[{i}].")
