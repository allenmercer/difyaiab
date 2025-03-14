import json

from app.utils.logger import Logger

logger = Logger("Dify-POC-Agent")


class JsonUtil:
    @staticmethod
    def convert_to_dict(string_dict: str) -> dict:
        """
        Converts a JSON string into a Python dictionary.
        If parsing fails, returns an empty dictionary.
        """
        try:
            data_dict = json.loads(string_dict)
        except Exception as e:
            logger.error("Error parsing JSON to dict: %s", e)
            data_dict = {}
        return data_dict

    @staticmethod
    def convert_to_list_of_dicts(json_str: str) -> list:
        """
        Converts a JSON string into a Python list of dictionaries.
        If the JSON represents a single dictionary, it wraps it in a list.
        If parsing fails or the data is of an unexpected type, returns an empty list.
        """
        try:
            data = json.loads(json_str)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                return []
        except Exception as e:
            logger.error("Error parsing JSON: %s", e)
            return []
