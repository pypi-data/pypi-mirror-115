#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Asynchronous HTTP API Server

import importlib.util
import json
import os
import sys
import traceback

import aiohttp.web
import typing

from . import formdata

__version__ = '0.1.0'


class Endpoint:
    """API end-point function"""

    exec: typing.Callable

    def __init__(self, executor):
        self.exec = executor


class Server:
    """Basic HTTP API Server"""

    def load_api_dir(self, dirname):
        dir_relative = dirname.replace(self.api_root, "", 1)
        for endpoint_file in os.listdir(dirname):
            endpoint_path = os.path.join(dirname, endpoint_file)
            if endpoint_file.endswith(".py"):
                endpoint = endpoint_file[:-3]
                modname = ".".join(dir_relative.split("/"))
                spec = importlib.util.spec_from_file_location(f"{modname}.{endpoint}", endpoint_path)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                endpoint_url = os.path.join(dir_relative, endpoint).strip("/")
                if hasattr(m, "register"):
                    self.handlers[endpoint_url] = m.__getattribute__("register")(self)
                    print(f"Registered endpoint /{endpoint_url}")
                else:
                    print(f"Could not find entry point 'register()' in {endpoint_path}, skipping!")
            elif os.path.isdir(endpoint_path) and not endpoint_file.startswith("__"):
                print(f"Traversing {endpoint_path}")
                self.load_api_dir(endpoint_path)

    def __init__(self, api_dir: str = "endpoints", bind_ip: str = "127.0.0.1", bind_port: int = 8080, state: typing.Any = None):
        print("==== Starting HTTP API server... ====")
        self.state = state
        self.handlers = {}
        self.server = None
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.api_root = api_dir

        # Load each URL endpoint
        self.load_api_dir(api_dir)


    async def handle_request(self, request: aiohttp.web.BaseRequest) -> aiohttp.web.Response:
        """Generic handler for all incoming HTTP requests"""
        resp: aiohttp.web.Response

        # Define response headers first...
        headers = {"Server": "ahapi v/%s" % __version__}

        # Figure out who is going to handle this request, if any, while allowing path info.
        handler = '__404'
        segments = request.path.strip("/").split("/")
        for i in range(0, len(segments)):
            partial_url = "/".join(segments)
            if partial_url in self.handlers:
                handler = partial_url
                break
            segments.pop()

        body_type = "form"
        cct = request.headers.get('content-type', 'foobar')
        if cct.lower() == 'application/json':
            body_type = "json"

        # Parse form/json data if any
        try:
            indata = await formdata.parse_formdata(body_type, request)
        except ValueError as e:
            return aiohttp.web.Response(headers=headers, status=400, text=str(e))

        # Find a handler, or 404
        if handler in self.handlers:
            try:
                # Wait for endpoint response. This is typically JSON in case of success,
                # but could be an exception (that needs a traceback) OR
                # it could be a custom response, which we just pass along to the client.
                output = await self.handlers[handler].exec(self.state, request, indata)
                headers["content-type"] = "application/json"
                if output and not isinstance(output, aiohttp.web.Response):
                    jsout = json.dumps(output, indent=2)
                    headers["Content-Length"] = str(len(jsout))
                    return aiohttp.web.Response(headers=headers, status=200, text=jsout)
                elif isinstance(output, aiohttp.web.Response):
                    return output
                else:
                    return aiohttp.web.Response(headers=headers, status=404, text="Content not found")
            # If a handler hit an exception, we need to print that exception somewhere,
            # either to the web client or stderr:
            except:  # This is a broad exception on purpose!
                exc_type, exc_value, exc_traceback = sys.exc_info()
                err = "\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                return aiohttp.web.Response(headers=headers, status=500, text="API error occurred: \n" + err)
        else:
            return aiohttp.web.Response(headers=headers, status=404, text="API Endpoint not found!")

    async def loop(self):
        self.server = aiohttp.web.Server(self.handle_request)
        runner = aiohttp.web.ServerRunner(self.server)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, self.bind_ip, self.bind_port)
        await site.start()
        print("==== HTTP API Server running on %s:%s ====" % (self.bind_ip, self.bind_port))
