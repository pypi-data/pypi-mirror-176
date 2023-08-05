#
# Copyright (c) 2021 Nitric Technologies Pty Ltd.
#
# This file is part of Nitric Python 3 SDK.
# See https://github.com/nitrictech/python-sdk for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import asyncio
from nitric.faas import FunctionServer
# from nitric.resources.base import BaseResource
from typing import Dict, List, Type, Any, TypeVar


BT = TypeVar('BT')

class Nitric:
    _workers: List[FunctionServer] = []
    _cache: Dict[str, Dict[str, Any]] = {
        "api": {},
        "bucket": {},
        "topic": {},
        "secret": {},
        "queue": {},
        "collection": {}
    }

    @classmethod
    def _register_worker(cls, srv: FunctionServer):
        """
        Register a worker for this
        """
        cls._workers.append(srv)

    @classmethod 
    def _create_resource(cls, resource: Type[BT], name: str) -> BT:
        resource_type = resource.__name__.lower()
        if cls._cache.get(resource_type).get(name) is None:
            cls._cache[resource_type][name] = resource.make(name)

        return cls._cache[resource_type][name]

    @classmethod    
    def run(cls):
        """
        Start the nitric application, this will execute in an existing event loop if there is one, otherwise it will
        attempt to create its own
        """
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()

            loop.run_until_complete(asyncio.gather(*[wkr.start() for wkr in cls._workers]))
        except KeyboardInterrupt:
            print("\nexiting")
