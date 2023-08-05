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
        'package-name': 'apache-airflow-providers-mysql',
        'name': 'MySQL',
        'description': '`MySQL <https://www.mysql.com/products/>`__\n',
        'versions': ['2.1.0', '2.0.0', '1.1.0', '1.0.2', '1.0.1', '1.0.0'],
        'additional-dependencies': ['apache-airflow>=2.1.0'],
        'integrations': [
            {
                'integration-name': 'MySQL',
                'external-doc-url': 'https://www.mysql.com/',
                'how-to-guide': ['/docs/apache-airflow-providers-mysql/operators.rst'],
                'logo': '/integration-logos/mysql/MySQL.png',
                'tags': ['software'],
            }
        ],
        'operators': [
            {'integration-name': 'MySQL', 'python-modules': ['airflow.providers.mysql.operators.mysql']}
        ],
        'hooks': [{'integration-name': 'MySQL', 'python-modules': ['airflow.providers.mysql.hooks.mysql']}],
        'transfers': [
            {
                'source-integration-name': 'Vertica',
                'target-integration-name': 'MySQL',
                'python-module': 'airflow.providers.mysql.transfers.vertica_to_mysql',
            },
            {
                'source-integration-name': 'Amazon Simple Storage Service (S3)',
                'target-integration-name': 'MySQL',
                'python-module': 'airflow.providers.mysql.transfers.s3_to_mysql',
            },
            {
                'source-integration-name': 'Presto',
                'target-integration-name': 'MySQL',
                'python-module': 'airflow.providers.mysql.transfers.presto_to_mysql',
            },
            {
                'source-integration-name': 'Trino',
                'target-integration-name': 'MySQL',
                'python-module': 'airflow.providers.mysql.transfers.trino_to_mysql',
            },
        ],
        'hook-class-names': ['airflow.providers.mysql.hooks.mysql.MySqlHook'],
    }
