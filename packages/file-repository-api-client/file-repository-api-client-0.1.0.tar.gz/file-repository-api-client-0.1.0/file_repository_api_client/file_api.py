import logging
import logging.config
import mimetypes
from pathlib import Path
from typing import Any

import requests


class MimeTypeUnknown(Exception):
    pass


class FileApi(object):
    """
    Store and Retrieve files store in a file repository api.
    used with a custom based aws file repository api.

    :param api_url: the custom api end point
    :type api_url: str
    """

    def __init__(self, api_url: str):
        self.api_url = api_url

    def store_file(self, absolute_file_path: str) -> dict:
        """
        Stole file name
        :param absolute_file_path:
        :return:
        """
        file_name = Path(absolute_file_path).name
        file_mime_type, encoding = mimetypes.guess_type(absolute_file_path)

        if file_mime_type is None:
            raise MimeTypeUnknown("Unknown file mimetype")

        results_dict: dict = {}
        headers = {"NAME": file_name, "Content-Type": file_mime_type}

        # read file
        with open(absolute_file_path, mode="rb") as file_resource:
            payload = file_resource.read()

        try:
            response: Any = requests.post(self.api_url, headers=headers, data=payload)
            response.raise_for_status()
            results_dict = response.json()
        except requests.exceptions.HTTPError as err:
            logging.exception(
                f"Exception occurred whilst attempting to store file using api:{self.api_url}"
            )
            raise Exception(err) from err

        return results_dict

    def retrieve_file(self, guid: str) -> dict:
        """
        Retrieve file name
        :param guid:
        :return:
        """

        results_dict: dict = {}
        headers = {"Accept": "application/json"}

        formatted_url: str = f"{self.api_url}/{guid}"
        try:
            response: Any = requests.get(formatted_url, headers=headers)
            response.raise_for_status()
            results_dict = response.json()
        except requests.exceptions.HTTPError as err:
            logging.exception(
                f"Exception occurred whilst attempting to retrieve file using api:{formatted_url}"
            )
            raise Exception(err) from err

        return results_dict
