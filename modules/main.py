from enum import Enum
import csv

from modules.console_interface import ConsoleInterface
from modules.ec2_driver import EC2Driver
import modules.data_preprocessor as dpp


class Command(Enum):
    LIST_INSTANCES = '1'
    AVAILABLE_ZONES = '2'
    START_INSTANCE = '3'
    AVAILABLE_REGIONS = '4'
    STOP_INSTANCE = '5'
    CREATE_INSTANCE = '6'
    REBOOT_INSTANCE = '7'
    LIST_IMAGES = '8'
    QUIT = '99'


def init():
    credential_path = "resources/credentials/"
    access_key_csv_name = "credentials.csv"
    f = open(credential_path + access_key_csv_name, 'r', encoding='utf-8')
    rdr = csv.DictReader(f)

    credential_info = next(rdr, None)
    ec2 = object()
    if credential_info is not None:
        # BOM 문자 제거
        credential_info = {key.strip('\ufeff'): value for key, value in credential_info.items()}

        aws_access_key = credential_info.get("Access key ID")
        secret_access_key = credential_info.get("Secret access key")
        ec2 = EC2Driver(aws_access_key, secret_access_key)

    else:
        print("Credential file is empty or header only.")

    f.close()

    main(ec2)       # END of init()


def main(ec2):
    cli = ConsoleInterface(ec2)
    command = ""
    while command != Command.QUIT.value:
        cli.print_menu()
        command = input()
        if command == Command.LIST_INSTANCES.value:
            result = dpp.process_list_instances(ec2.list_instances())
            cli.print_list(result)

        elif command == Command.AVAILABLE_ZONES.value:
            result = dpp.process_available_zones(ec2.available_zones())
            cli.print_available_zones(result)

        elif command == Command.START_INSTANCE.value:
            param = cli.get_instance_name()
            result = ec2.start_instance(param)
            cli.print_start_instance(result)

        elif command == Command.STOP_INSTANCE.value:
            param = cli.get_instance_name()
            result = ec2.stop_instance(param)
            cli.print_stop_instance(result)

        elif command == Command.AVAILABLE_REGIONS.value:
            result = dpp.process_available_regions(ec2.available_regions())
            cli.print_available_regions(result)

        elif command == Command.CREATE_INSTANCE.value:
            params = cli.get_params_create_instance()
            ec2.create_instance(params)

        elif command == Command.REBOOT_INSTANCE.value:
            param = cli.get_instance_name()
            result = ec2.reboot_instance(param)
            cli.print_reboot_instance(result)

        elif command == Command.LIST_IMAGES.value:
            result = dpp.process_list_images(ec2.list_images())
            cli.print_list_images(result)

        elif command == Command.QUIT.value:
            cli.print_quit()

        else:
            cli.print_error()
