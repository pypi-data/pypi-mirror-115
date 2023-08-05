# Copyright 2021 Chainopt LLC.
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

import click

from rio.utilities import utils as rio_utils


@click.command()
@click.option("-l", "--local", is_flag=True, type=bool, help="Specify local deployment")
@click.option("-f", "--file", type=str, help="Specify a yaml file with docker credentials")
def cli(local, file):
    """
    Begin RIO Services.

    1) Authenticates to Docker Hub and creates RIO-API container
    2) Lists all packages that have been deployed
    3) Begins all packages that have been deployed
    """
    rio_utils.begin(local, file)
    rio_utils.list_packages(local)
    rio_utils.begin_packages(local)

    return
