import platform

from prettytable import PrettyTable


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
        print("============================================\n"
              "1.  list instance     2.  available zones\n"
              "3.  start instance    4.  available regions\n"
              "5.  stop instance     6.  create instance\n"
              "7.  reboot instance   8.  list images\n"
              "11. condor status    12.  send direct command\n"
              "13. test job submit  14.  fetch results\n"
              "15. condor queue     16.  condor flush\n"
              "                     99. quit\n"
              "============================================\n"
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
    def print_create_instance(self, result):
        print(result)

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
    def get_instance_name(self):
        print(" * Give instance name > ", end='')
        input_instance_name = input()
        return input_instance_name

    def get_instance_count(self):
        print(" * How many do you want to create? > ", end='')
        input_count = input()
        return input_count

    def print_pretty(self, data):
        headers = list(data[0].keys())
        table = PrettyTable()
        table.field_names = headers

        for row in data:
            table.add_row([row[header] for header in headers])

        print(table)

    def print_condor_status(self, result):
        print(f"{result.stdout}")

    def print_condor_q(self, result):
        print(f"{result.stdout}")
