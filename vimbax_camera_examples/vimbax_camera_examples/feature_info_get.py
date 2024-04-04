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
import argparse
from .helper import single_service_call, feature_type_dict
from .helper import print_feature_info, get_module_from_string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("node_name")
    parser.add_argument("feature_type", choices=['Int', 'Float', 'String', 'Raw', 'Bool', 'Enum'])
    parser.add_argument("feature_name")
    parser.add_argument("-m", "--module", choices=[
        "remote_device",
        "system",
        "interface",
        "local_device",
        "stream"
    ], default="remote_device", dest="module")

    (args, rosargs) = parser.parse_known_args()

    rclpy.init(args=rosargs)

    node = Node("_feature_get")

    feature_type = feature_type_dict[args.feature_type]
    feature_service_type = feature_type.info_service_type

    if feature_service_type is None:
        print(f"Feature type {args.feature_type} does not support info query")
        exit(1)

    request = feature_service_type.Request()
    request.feature_name = args.feature_name
    request.feature_module = get_module_from_string(args.module)
    response = single_service_call(
        node, feature_service_type,
        f"{args.node_name}/{feature_type.service_base_path}_info_get", request)

    if response.error.code == 0:
        print_feature_info(response)
    else:
        print(f"Getting feature {args.feature_name} info failed with {response.error}")
