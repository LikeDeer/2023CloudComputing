import os
import platform

from prettytable import PrettyTable

from modules.constants import INSTRUCTIONS_CREATE_INSTANCES
from modules.ec2_driver import EC2Driver


# noinspection PyMethodMayBeStatic
class ConsoleInterface:
    def __init__(self, ec2):
        self._ec2 = ec2
        self._system = platform.system()
        print("------------------------------------------\n"
              "         Amazon AWS Control Panel         \n"
              "\n"
              "Jeong, Junho\n"
              "               School of Computer Science\n"
              "          at Chungbuk National University")

    def print_menu(self):
        print("==========================================\n"
              "1. list instance     2. available zones\n"
              "3. start instance    4. available regions\n"
              "5. stop instance     6. create instance\n"
              "7. reboot instance   8. list images\n"
              "                     99. quit\n"
              "==========================================\n"
              ">> ", end='')

    # 1.
    def print_list(self, data):
        self.print_pretty(data)

    # 2.
    def print_available_zones(self, data):
        self.print_pretty(data)

    # 3.
    def print_start_instance(self, result):
        print(result)

    # 4.
    def print_available_regions(self, data):
        self.print_pretty(data)

    # 5.
    def print_stop_instance(self, result):
        print(result)

    # 6.
    def print_create_instance(self):
        pass

    # 7.
    def print_reboot_instance(self, result):
        print(result)

    # 8.
    def print_list_images(self, data):
        self.print_pretty(data)

    # 99.
    def print_quit(self):
        print("Bye.")

    def print_error(self):
        print("Invalid Command. Try Again.")

    # Methods which require inputs by the user
    # 6-1.

    def get_instance_name(self):
        print(" * Give instance name > ", end='')
        input_instance_name = input()
        return input_instance_name

    def get_params_create_instance(self):
        params = {}
        print(" * Give parameters following questions\n"
              " *  Some questions are marked '*-', which means required.\n"
              " *  Otherwise, you can remain it blank, which will be applied by default values\n")
        for item in INSTRUCTIONS_CREATE_INSTANCES:
            print(item[0], end='')
            input_param = input()

            if input_param != "":
                params[item[1]] = input_param

            """
            elif input_param == 'help':
                self.print_help_create_instance(item[1])
            """

        return params

    def print_pretty(self, data):
        headers = list(data[0].keys())
        table = PrettyTable()
        table.field_names = headers

        for row in data:
            table.add_row([row[header] for header in headers])

        print(table)


"""
    def print_help_create_instance(self, for_what):
        if for_what == "ImageId":
            images = self._ec2.list_images()
            self.print_list_images(images)
        elif for_what == "InstanceType":
            instance_types = self._ec2.list
        elif for_what == "MinCount":

        elif for_what == "KeyName":

        elif for_what == "SecurityGroups":
"""