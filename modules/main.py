from enum import Enum
import csv

from modules.console_interface import ConsoleInterface
from modules.ec2_driver import EC2Driver


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
    access_key_csv_name = "IAMLikeDeer_accessKeys.csv"
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
    cli = ConsoleInterface()
    command = ""
    while command != Command.QUIT.value:
        cli.print_menu()
        command = input()
        if command == Command.LIST_INSTANCES.value:
            result = ec2.list_instances()
            cli.print_list(result)
        elif command == Command.AVAILABLE_ZONES.value:
            result = ec2.available_zones()
            cli.print_available_zones(result)
        elif command == Command.START_INSTANCE.value:
            cli.print_start()
        elif command == Command.AVAILABLE_REGIONS.value:
            result = ec2.available_regions()
            cli.print_available_regions(result)
        elif command == Command.CREATE_INSTANCE.value:
            cli.print_create_instance()
        elif command == Command.REBOOT_INSTANCE.value:
            cli.print_reboot_instance()
        elif command == Command.LIST_IMAGES.value:
            cli.print_list_images()
        elif command == Command.QUIT.value:
            cli.print_quit()
        else:
            cli.print_error()
