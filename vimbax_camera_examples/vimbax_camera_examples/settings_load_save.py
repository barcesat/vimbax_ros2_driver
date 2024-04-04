# Copyright 2024 Allied Vision Technologies GmbH. All Rights Reserved.
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

import rclpy
from rclpy.node import Node
import vimbax_camera_msgs.srv
import argparse
from .helper import single_service_call


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("node_namespace")
    parser.add_argument("operation", choices=["load", "save"])
    parser.add_argument("filename")

    (args, rosargs) = parser.parse_known_args()

    rclpy.init(args=rosargs)

    node = Node("vimbax_settings_load_save_example")

    service_type = vimbax_camera_msgs.srv.SettingsLoadSave

    namespace = args.node_namespace.strip("/")
    topic: str = f"/settings/{args.operation}"
    if len(namespace) != 0:
        topic = f"/{namespace}/{topic.strip('/')}"

    request = service_type.Request()
    request.filename = args.filename
    response = single_service_call(node, service_type,
                                   topic, request)

    if response.error.code == 0:
        print(f"Settings {args.operation} was successfull")
    else:
        print(f"Settings {args.operation} failed with {response.error}")
