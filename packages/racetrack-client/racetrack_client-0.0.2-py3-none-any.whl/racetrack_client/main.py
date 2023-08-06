import argparse
import sys

from racetrack_client import __version__
from racetrack_client.client.deploy import send_deploy_request
from racetrack_client.client_config.update import set_credentials, set_config_var
from racetrack_client.log.exception import log_exception
from racetrack_client.log.logs import configure_logs
from racetrack_client.manifest.validate import load_validated_manifest


def main():
    parser = argparse.ArgumentParser(description='CLI client tool for deploying workloads to Racetrack')
    subparsers = parser.add_subparsers()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='enable verbose mode')

    subparser = subparsers.add_parser('deploy', help='Send request deploying a new Job to running LC instance')
    subparser.add_argument('workdir', default='.', nargs='?')
    subparser.add_argument('lifecycle_url', default='', nargs='?', help='URL to Lifecycle API server')
    subparser.set_defaults(func=_deploy)

    subparser = subparsers.add_parser('validate', help='Validate Fatman manifest file')
    subparser.add_argument('path', default='.', nargs='?',
                           help='path to a Fatman manifest file or to a directory with it')
    subparser.set_defaults(func=_validate)

    subparser = subparsers.add_parser('version', help='Show the version information')
    subparser.set_defaults(func=_version)

    subparser = subparsers.add_parser('config', help='Set lifecycle global options for a local client')
    config_subparsers = subparser.add_subparsers()

    config_subparser = config_subparsers.add_parser(
        'set-credentials', help='set credentials for reading git repository'
    )
    config_subparser.add_argument('repo_url', help='git remote URL')
    config_subparser.add_argument('username', help='username for git authentication')
    config_subparser.add_argument('token_password', help='password or token for git authentication')
    config_subparser.set_defaults(func=_set_credentials)

    config_subparser = config_subparsers.add_parser('set', help='set variable in local client config')
    config_subparser.add_argument('var_name', help='variable name')
    config_subparser.add_argument('var_value', help='variable value')
    config_subparser.set_defaults(func=_set_config_var)

    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
    else:
        args: argparse.Namespace = parser.parse_args()

        configure_logs(args.verbose)
        args.func(args)


def _deploy(args: argparse.Namespace):
    try:
        send_deploy_request(args.workdir, lifecycle_api_url=args.lifecycle_url)
    except Exception as e:
        log_exception(e)


def _validate(args: argparse.Namespace):
    try:
        load_validated_manifest(args.path)
    except Exception as e:
        log_exception(e)


def _set_credentials(args: argparse.Namespace):
    set_credentials(args.repo_url, args.username, args.token_password)


def _set_config_var(args: argparse.Namespace):
    set_config_var(args.var_name, args.var_value)


def _version(_: argparse.Namespace):
    print(f'racetrack-client version {__version__}')
