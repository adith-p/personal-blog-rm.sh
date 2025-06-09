from pathlib import Path, PosixPath
import json

import logging


class JsonSerializer:

    def __init__(self, file_list):
        self.file_list: list[PosixPath] | PosixPath = file_list
        self.json_dict = {}

    def serialize(self) -> dict[str, dict]:

        if isinstance(self.file_list, PosixPath):
            self.file_list = [self.file_list]

        for i, file in enumerate(self.file_list):
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                self.json_dict[f"file{i}"] = data
            except FileNotFoundError:
                logging.warning(f"File not found: '{file.name}'. Skipping.")
            except json.JSONDecodeError:
                logging.warning(
                    f"json file could not be parsed '{file.name}'. Skipping."
                )
            except TypeError:
                logging.critical(
                    f"passing in the single PosixPath change the safe to false"
                )
        return self.json_dict
        # try:
        #     print([self.file_list])
        #     with open(self.file_list, "r") as f:
        #         data = json.load(f)

        #     self.json_dict[f"result"] = data
        # except (FileNotFoundError, json.JSONDecodeError) as e:
        #     logging.warning(f"exection have occured {e}")

        # return self.json_dict
