import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

from adtsdk import DataFormat, DataSources, Uploader


def print_output(output: Dict[str, Any]) -> None:
    """Prints to the stdout JSON formatted output dictionary of the response"""
    print(json.dumps(output, indent=4))


def cli_arg_parser() -> argparse.ArgumentParser:
    """Creates common functionality of argument parser

    Returns
    -------
    argparse.ArgumentParser
        Instance of the argument parser
    """
    argp = argparse.ArgumentParser(
        description='ADT Upload and Datasource API CLI'
    )
    argp.add_argument(
        '-a',
        '--api-server',
        help='ADT API server URL',
        required=True,
    )
    argp.add_argument(
        '-d',
        '--datasource',
        help='Data source name',
        required=True,
    )
    argp.add_argument(
        '-j',
        '--jwt-auth-token',
        help=(
            'JWT for authentication to the API. If not set then'
            ' JWT_AUTH_TOKEN environment variable must be set'
        ),
        default=os.getenv('JWT_AUTH_TOKEN'),
    )
    argp.add_argument(
        '--http-proxy', help='HTTP Proxy URL', default=os.getenv('HTTP_PROXY')
    )
    argp.add_argument(
        '--https-proxy',
        help='HTTPS Proxy URL',
        default=os.getenv('HTTPS_PROXY'),
    )
    return argp


def parse_input(argp: argparse.ArgumentParser) -> argparse.Namespace:
    """Parses input arguments

    Parameters
    ----------
    argp : argparse.ArgumentParser
        Argument parser instance

    Returns
    -------
    argparse.Namespace
        Parsed argument namespace

    Raises
    ------
    ValueError
        When neither `--jwt-auth-token` argument nor `JWT_AUTH_TOKEN`
        environment variable is defined.
    """
    args = argp.parse_args()
    if args.jwt_auth_token is None:
        raise ValueError(
            'Neither --jwt-auth-token argument nor JWT_AUTH_TOKEN'
            ' environment variable is defined'
        )
    return args


def upload_data() -> None:
    """Uploads data with CLI"""

    argp = cli_arg_parser()
    argp.add_argument('-f', '--file', help='Path to the file to upload')
    args = parse_input(argp)

    file = Path(args.file)

    with Uploader(
        api_server_url=args.api_server,
        jwt_auth_token=args.jwt_auth_token,
        http_proxy=args.http_proxy,
        https_proxy=args.https_proxy,
    ) as uploader:
        out = uploader.upload_single(
            stream_name=args.datasource, data=file.open('rb')
        )
        print_output(out)


def add_datasource() -> None:
    """Creates new data source with CLI"""
    argp = cli_arg_parser()
    argp.add_argument(
        '-t',
        '--data-format',
        help='Data type of the data source, defaults to CSV',
        choices=[
            str(DataFormat.CSV),
            str(DataFormat.NDJSON),
        ],
        default=str(DataFormat.CSV),
    )
    args = parse_input(argp)

    data_format = DataFormat(args.data_format)

    with DataSources(
        api_server_url=args.api_server,
        jwt_auth_token=args.jwt_auth_token,
        http_proxy=args.http_proxy,
        https_proxy=args.https_proxy,
    ) as datasources:
        out = datasources.add_datasource(
            name=args.datasource, data_format=data_format
        )
        print_output(out)


def delete_datasource() -> None:
    """Deletes existing data source with CLI"""
    argp = cli_arg_parser()
    args = parse_input(argp)

    with DataSources(
        api_server_url=args.api_server,
        jwt_auth_token=args.jwt_auth_token,
        http_proxy=args.http_proxy,
        https_proxy=args.https_proxy,
    ) as datasources:
        out = datasources.delete_datasource(name=args.datasource)
        print_output(out)
