# noinspection PyMethodMayBeStatic
class ConsoleInterface:
    def __init__(self):
        pass

    def print_menu(self):
        print("------------------------------------------\n"
              "1. list instance     2. available zones\n"
              "3. start instance    4. available regions\n"
              "5. stop instance     6. create instance\n"
              "7. reboot instance   8. list images\n"
              "                     99. quit\n"
              "------------------------------------------\n"
              ">> ", end='')

    def print_list(self, data):
        print(data)

    def print_available_zones(self, data):
        pass

    def print_start(self):
        pass

    """
        입력 데이터 예시:
        ['ap-south-1', 'eu-north-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-3', 'ap-northeast-2',
         'ap-northeast-1', 'ca-central-1', 'sa-east-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1',
         'us-east-2', 'us-west-1', 'us-west-2']
    """
    def print_available_regions(self, data):
        print(data)

    def print_stop_instance(self):
        pass

    def print_create_instance(self):
        pass

    def print_reboot_instance(self):
        pass

    def print_list_images(self):
        pass

    def print_quit(self):
        print("Bye.")

    def print_error(self):
        print("Invalid Command. Try Again.")
