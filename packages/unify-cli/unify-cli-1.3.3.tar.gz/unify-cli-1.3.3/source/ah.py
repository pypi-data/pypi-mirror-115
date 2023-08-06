#!/usr/bin/env python

# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import click

from source.cluster.commands import cluster as cluster_group
from source.user.commands import user as user_group
from source.pipeline.commands import pipeline as pipeline_group
from source.workflow.commands import wf as workflow_group
from source.template.commands import template as template_group
from source.dataset.commands import dataset as dataset_group
from source.org.commands import org as org_group
from source.access.commands import access as access_group
from source.graph.commands import graph as graph_group

sys.dont_write_bytecode = True
PYTHONDONTWRITEBYTECODE = 1


@click.group()
def cli():
    """
    Unify Command Line Interface
    :return:
    """


cli.add_command(cluster_group)
cli.add_command(user_group)
cli.add_command(pipeline_group)
cli.add_command(workflow_group)
cli.add_command(template_group)
cli.add_command(dataset_group)
cli.add_command(org_group)
cli.add_command(access_group)
cli.add_command(graph_group)

if __name__ == '__main__':
    cli()
