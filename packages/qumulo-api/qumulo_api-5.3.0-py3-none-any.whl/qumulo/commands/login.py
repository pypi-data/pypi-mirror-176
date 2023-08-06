# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


import argparse
import textwrap
import time

from typing import Any, Callable, Dict, Tuple

import qumulo.lib.opts
import qumulo.rest.auth as auth

from qumulo.commands import auth as auth_commands
from qumulo.lib.auth import (
    credential_store_filename,
    Credentials,
    remove_credentials_store,
    set_credentials,
)
from qumulo.lib.opts import str_decode
from qumulo.lib.request import RequestError
from qumulo.rest_client import RestClient


class LoginCommand(qumulo.lib.opts.Subcommand):
    NAME = 'login'
    SYNOPSIS = 'Log in to qfsd to get REST credentials'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-u', '--username', type=str_decode, default=None, required=True, help='User name'
        )
        parser.add_argument(
            '-p',
            '--password',
            type=str_decode,
            default=None,
            help='Password (insecure, visible via ps)',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.password is None:
            password = qumulo.lib.opts.read_password(prompt='Password: ')
        else:
            password = args.password

        if args.credentials_store is None:
            credentials_store_path = credential_store_filename()
        else:
            credentials_store_path = args.credentials_store

        login_resp, _ = auth.login(
            rest_client.conninfo, rest_client.credentials, args.username, password
        )
        set_credentials(login_resp, credentials_store_path)


class LogoutCommand(qumulo.lib.opts.Subcommand):
    NAME = 'logout'
    SYNOPSIS = 'Remove qfsd REST credentials'

    @staticmethod
    def main(_rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.credentials_store is None:
            credentials_store_path = credential_store_filename()
        else:
            credentials_store_path = args.credentials_store

        remove_credentials_store(credentials_store_path)


class SSOCommand(qumulo.lib.opts.Subcommand):
    NAME = 'sso_login'
    SYNOPSIS = 'Log in to the cluster using the configured Single Sign-On service'

    DESCRIPTION = SYNOPSIS + textwrap.dedent(
        """

        Cluster administrators can enable SAML single sign-on (SSO) with qq saml_modify_settings
        """
    )

    @staticmethod
    def main(
        rest_client: RestClient,
        args: argparse.Namespace,
        auth_mod: Any = auth,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        if args.credentials_store is None:
            credentials_store_path = credential_store_filename()
        else:
            credentials_store_path = args.credentials_store

        pending_login, _ = auth_mod.start_saml_login(rest_client.conninfo, None)
        login_id = pending_login['login_id']

        print('Waiting for authentication. Please open the following link in the browser:')
        print()
        print(pending_login['login_url'])
        print()

        login_resp = poll_for_creds(rest_client, login_id, auth_mod, sleep_fn)
        rest_client.credentials = Credentials.from_login_response(login_resp)

        me, _ = auth_mod.who_am_i(rest_client.conninfo, rest_client.credentials)
        set_credentials(login_resp, credentials_store_path)
        print('Logged in as', me['name'])


def poll_for_creds(
    rest_client: RestClient, login_id: str, auth_mod: Any, sleep_fn: Callable[[float], None]
) -> Dict[str, str]:
    while True:
        response, _ = auth_mod.retrieve_saml_login(rest_client.conninfo, None, login_id)
        if response['bearer_token']:
            return response
        sleep_fn(2)


class WhoAmICommand(qumulo.lib.opts.Subcommand):
    NAME = 'who_am_i'
    SYNOPSIS = 'Get information on the current user'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        me = auth.who_am_i(rest_client.conninfo, rest_client.credentials)
        print(str(me))

        # Get user's Role assignments
        print('This user is granted the following roles:')
        my_roles = auth.my_roles(rest_client.conninfo, rest_client.credentials)
        print(str(my_roles))

        try:
            group_info_msg, related_info_msg = WhoAmICommand.get_related_info(
                rest_client, str(me.lookup('id'))
            )
            print(str(group_info_msg))
            print(str(related_info_msg))
        except RequestError as ex:
            # Users without the ability to expand identities can't get their
            # related info. Since that information was never really core to
            # `who_am_i`, and erroring would be weird, we swallow the exception.
            if ex.status_code != 403:
                raise

    @staticmethod
    def get_related_info(rest_client: RestClient, user_id: str) -> Tuple[str, str]:
        # Get all related group info
        try:
            group_info_msg = auth_commands.get_user_group_info_msg(
                rest_client.conninfo, rest_client.credentials, user_id
            )
        except RequestError as ex:
            if ex.status_code == 404:
                # Expected for an AD user, for example.
                group_info_msg = 'Not a local user.'
            else:
                raise

        # Get all related IDs
        try:
            related_info_msg = auth_commands.get_expanded_identity_information_for_user(
                rest_client.conninfo, rest_client.credentials, user_id
            )
        except RequestError as ex:
            if ex.status_code == 404:
                # Expected for operators, for example.
                related_info_msg = 'No related IDs found.'
            else:
                raise

        return group_info_msg, related_info_msg
