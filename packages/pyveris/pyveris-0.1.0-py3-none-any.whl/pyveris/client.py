import json
import os
import requests

import pyveris.constants as const


class Client:
    """
    Loads configuration from environment variable "CONVERIS_API_CONFIG", which is
    a JSON string containing:
        url (str): the URL of Converis API
        username (str): username for basic authentication
        password (str): password for basic authentication
    """

    def __init__(self):
        try:
            api_config = json.loads(os.environ[const.api_config_name])
        except KeyError:
            raise KeyError(f"Environment variable {const.api_config_name} not set")
        except json.decoder.JSONDecodeError:
            raise ValueError(
                f"Environment variable {const.api_config_name} should be set to a JSON string"
            )

        try:
            self.base_url = api_config[const.api_config_url_name]
            user = api_config[const.api_config_user_name]
            password = api_config[const.api_config_pass_name]
        except KeyError as exc:
            raise KeyError(
                f"{exc.args[0]} must be present in {const.api_config_name}; not found"
            )

        self.session = requests.Session()
        self.session.auth = (
            user,
            password,
        )

    def query_data_entities(self, **kwargs):
        """
        Get all data of an entity by type name and query.
        See https://api.clarivate.com/swagger-ui/?apikey=none&url=https%3A%2F%2Fdeveloper.clarivate.com%2Fapis%2Fconverisreadapi%2Fswagger

        Args:
            **kwargs:
                query (required; str): the filter query
                attribute_definition (str): attributes to be returned. Possible values BASIC, ALL, comma-separated
                    string listing attributes
                count (int): maximum number of records to return (default: 10)
                language (str): return only labels or attribute data of specific configured language. Display all
                    configured languages if null. Example: en_GB
                linkentity (str):
                sort (str): sort by attributes of the link entity. Currently only BASIC attributes are supported.
                sortOrder (str): sort order. ASC (default) for ascending; DESC for descending
                startRecord (int): record to start for pagination (default: 1)
                type (str): the entity type name (default: Publication)

        Returns:
        """
        endpoint = (
            f"{self.base_url}data/entities/{kwargs.pop('type', 'Publication')}/query"
        )

        headers = {
            "Content-Type": "application/vnd.converis.ql+plain",
            "Converis-attribute-definition": kwargs.pop("attribute_definition", "ALL"),
            "Converis-linkentity-references": kwargs.pop("linkentity", "TRUE"),
        }

        try:
            body = kwargs.pop("query")
        except KeyError:
            raise KeyError(
                "You must include a 'query' parameter when calling this method"
            )

        return self.session.post(endpoint, data=body, headers=headers, params=kwargs)
