"""
JSON Tools Module

Provides simple JSON validation and transformation.
"""

import json

class ValidateJsonTool:
    @staticmethod
    def function(*, json_str: str) -> dict:
        try:
            json.loads(json_str)
            return {"valid": True}
        except Exception:
            return {"valid": False}

class TransformJsonTool:
    @staticmethod
    def function(*, json_str: str, transformation: str) -> dict:
        try:
            data = json.loads(json_str)
            if transformation == "uppercase_keys":
                transformed = {k.upper(): v for k, v in data.items()}
                return transformed
            return data
        except Exception as e:
            return {"error": str(e)}

# Expose tool instances.
validate_json = ValidateJsonTool()
transform_json = TransformJsonTool()
