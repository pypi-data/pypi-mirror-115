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

# NOTE! THIS FILE IS AUTOMATICALLY GENERATED AND WILL BE
# OVERWRITTEN WHEN PREPARING PACKAGES.
#
# IF YOU WANT TO MODIFY IT, YOU SHOULD MODIFY THE TEMPLATE
# `get_provider_info_TEMPLATE.py.jinja2` IN the `provider_packages` DIRECTORY


def get_provider_info():
    return {
        'package-name': 'apache-airflow-providers-ssh',
        'name': 'SSH',
        'description': '`Secure Shell (SSH) <https://tools.ietf.org/html/rfc4251>`__\n',
        'versions': ['2.1.0', '2.0.0', '1.3.0', '1.2.0', '1.1.0', '1.0.0'],
        'additional-dependencies': ['apache-airflow>=2.1.0'],
        'integrations': [
            {
                'integration-name': 'Secure Shell (SSH)',
                'external-doc-url': 'https://tools.ietf.org/html/rfc4251',
                'logo': '/integration-logos/ssh/SSH.png',
                'tags': ['protocol'],
            }
        ],
        'operators': [
            {
                'integration-name': 'Secure Shell (SSH)',
                'python-modules': ['airflow.providers.ssh.operators.ssh'],
            }
        ],
        'hooks': [
            {'integration-name': 'Secure Shell (SSH)', 'python-modules': ['airflow.providers.ssh.hooks.ssh']}
        ],
        'hook-class-names': ['airflow.providers.ssh.hooks.ssh.SSHHook'],
    }
