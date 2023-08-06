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

import click

from unify.apimanager import ApiManager

from source.common.commands import org_cluster_options


@click.group()
def user():
    """Group for the user related commands"""
    pass


@user.command('list')
def user_list():
    click.echo(click.style("Command under development", blink=False, bold=True, fg='blue'))


@user.command('add')
@org_cluster_options
@click.option('--email', prompt="User Email", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--name', prompt="Person Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
def user_add(org, remote, email, name, role):
    try:
        response = ApiManager(cluster=remote).orgs.invite_user(
            org_id=org,
            email=email,
            name=name,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('addserviceaccount')
@org_cluster_options
@click.option('--service_account_name', prompt="Service Account Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--service_account_id', prompt="Service Account ID (UUID format)", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--service_account_password', prompt="Service Account Password (UUIC format)", hide_input=True, default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
def user_add(org, remote, service_account_name, service_account_id, service_account_password, role):
    try:
        response = ApiManager(cluster=remote).orgs.invite_machine_user(
            org_id=org,
            fullname=service_account_name,
            id=service_account_id,
            password=service_account_password,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))

