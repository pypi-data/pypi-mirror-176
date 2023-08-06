import sys
import resotolib.logger
from resotolib.args import get_arg_parser, ArgumentParser
from resoto_plugin_aws import get_org_accounts


resotolib.logger.getLogger("resoto").setLevel(resotolib.logger.ERROR)
log = resotolib.logger.getLogger(__name__)

argv = sys.argv[1:]
if "-v" in argv or "--verbose" in argv:
    resotolib.logger.getLogger("resoto").setLevel(resotolib.logger.DEBUG)


def main() -> None:
    # Add cli args
    arg_parser = get_arg_parser()
    add_args(arg_parser)
    arg_parser.parse_args()
    accounts = get_org_accounts()
    for account in accounts:
        print(account)


def add_args(arg_parser: ArgumentParser) -> None:
    arg_parser.add_argument("--aws-access-key-id", help="AWS Access Key ID", dest="aws_access_key_id")
    arg_parser.add_argument(
        "--aws-secret-access-key",
        help="AWS Secret Access Key",
        dest="aws_secret_access_key",
    )
    arg_parser.add_argument("--aws-role", help="AWS IAM Role", dest="aws_role")
    arg_parser.add_argument(
        "--aws-role-override",
        help="Override any stored roles (e.g. from remote graphs) (default: False)",
        dest="aws_role_override",
        action="store_true",
        default=False,
    )


if __name__ == "__main__":
    main()
