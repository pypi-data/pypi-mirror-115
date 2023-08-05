#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from collections import namedtuple
from typing import Dict, List

from polyaxon.utils.date_utils import path_last_modified
from polyaxon.utils.path_utils import get_files_and_dirs_in_path


class PathData(namedtuple("PathData", "base ts op")):
    pass


class FSWatcher:
    PUT = "put"
    RM = "rm"
    NOOP = ""

    def __init__(self):
        self._dir_mapping = {}
        self._file_mapping = {}

    def _sync_path(self, path: str, base_path: str, mapping: Dict):
        current_ts = path_last_modified(path)
        rel_path = os.path.relpath(path, base_path)
        data = mapping.get(rel_path)
        if data:
            if current_ts > data.ts:
                mapping[rel_path] = PathData(base_path, current_ts, self.PUT)
            else:
                mapping[rel_path] = PathData(base_path, data.ts, self.NOOP)
        else:
            mapping[rel_path] = PathData(base_path, current_ts, self.PUT)
        return mapping

    def sync_file(self, path: str, base_path: str):
        self._file_mapping = self._sync_path(path, base_path, self._file_mapping)

    def sync_dir(self, path: str, base_path: str):
        self._dir_mapping = self._sync_path(path, base_path, self._dir_mapping)

    def init(self):
        self._dir_mapping = {
            p: PathData(d.base, d.ts, self.RM) for p, d in self._dir_mapping.items()
        }
        self._file_mapping = {
            p: PathData(d.base, d.ts, self.RM) for p, d in self._file_mapping.items()
        }

    def sync(self, path: str, exclude: List[str] = None):
        files, dirs = get_files_and_dirs_in_path(
            path, exclude=exclude, collect_dirs=True
        )
        for file_path in files:
            self.sync_file(file_path, base_path=path)

        for dir_path in dirs:
            self.sync_dir(dir_path, base_path=path)

    def _get_mapping_by_op(self, mapping: Dict, op: str):
        return {(p.base, k) for k, p in mapping.items() if p.op == op}

    def get_files_to_put(self):
        return self._get_mapping_by_op(self._file_mapping, self.PUT)

    def get_files_to_rm(self):
        return self._get_mapping_by_op(self._file_mapping, self.RM)

    def get_dirs_to_put(self):
        return self._get_mapping_by_op(self._dir_mapping, self.PUT)

    def get_dirs_to_rm(self):
        return self._get_mapping_by_op(self._dir_mapping, self.RM)
