import uuid
from django.conf import settings
import pathlib
import json

import logging


class FileSystem:
    base_dir = settings.BASE_DIR

    @classmethod
    def does_exist(cls) -> bool:

        return pathlib.Path(f"{cls.base_dir}/posts").exists()

    @classmethod
    def create_folder(cls, folder_name: str):
        return pathlib.Path(f"{cls.base_dir}/{folder_name}").mkdir()
        # return os.mkdir(f"{cls.base_dir}/{folder_name}")

    @classmethod
    def add(cls, data_json: dict):
        try:
            file_id = f"file-{str(uuid.uuid4())[:15]}-{data_json["title"].strip().replace(" ","-",-1)[:5]}"
            data_json["id"] = file_id
            with open(f"{cls.base_dir}/posts/{file_id}.json", "x") as jsonfile:

                json_object = json.dumps(data_json, indent=4)
                jsonfile.write(json_object)
            return file_id
        except FileExistsError:
            logging.critical("FILE name already exist")

    @classmethod
    def remove(cls, file_id: str):
        try:

            pathlib.Path(f"{cls.base_dir}/posts/{file_id}.json").unlink()
        except FileNotFoundError:
            logging.critical("post does not exist")
            return False
        return True

    @classmethod
    def update(cls, data_json: dict, file_id: str):
        try:

            with open(f"{cls.base_dir}/posts/{file_id}.json", "w") as json_file:
                json_object = json.dumps(data_json)
                json_file.write(json_object)

        except FileNotFoundError:
            logging.critical("post does not exist")

    @classmethod
    def read(cls, file_id: str):

        for file in pathlib.Path(f"{cls.base_dir}/posts").iterdir():

            if file.is_file() and file.name == f"{file_id}.json":
                return file

        return None
