import boto3
from botocore.exceptions import NoCredentialsError

from modules.data_preprocessor import process_list_instances
from modules.finder import find_instance_id_from_instance_name


# noinspection PyMethodMayBeStatic
class EC2Driver:
    def __init__(self, access_key_id, secret_access_key):
        try:
            self._region = 'us-east-1'    # default region
            self._ec2 = boto3.resource('ec2', aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key,
                                       region_name=self._region)
            self._ec2_client = self._ec2.meta.client
            self._sts_client = boto3.client('sts', aws_access_key_id=access_key_id,
                                            aws_secret_access_key=secret_access_key,
                                            region_name=self._region)
            print("연결 성공! Default Region: ", self._region)
        except Exception as e:
            print(f"연결 중 오류 발생: {e}")

    # 1.
    def list_instances(self):
        try:
            instances = self._ec2_client.describe_instances()
            return instances
        except Exception as e:
            print(f"리스트 조회 중 오류 발생: {e}")

    # 2.
    def available_zones(self):
        try:
            zones = self._ec2_client.describe_availability_zones()['AvailabilityZones']
            return zones
        except Exception as e:
            print(f"가용 zone 조회 중 오류 발생: {e}")

    # 3.
    def start_instance(self, instance_name):
        instance_id = find_instance_id_from_instance_name(
            process_list_instances(self.list_instances()), instance_name
        )
        if instance_id is None:
            print(" ** Name not found.. Try Instance ID instead > ", end='')
            instance_id = input()

        try:
            result = self._ec2_client.start_instances(
                InstanceIds=[
                    instance_id
                ]
            )
            return result
        except Exception as e:
            print(f"인스턴스 시작 중 오류 발생: {e}")

    # 4.
    def available_regions(self):
        try:
            regions = self._ec2_client.describe_regions()['Regions']
            return regions
        except Exception as e:
            print(f"가용 region 조회 중 오류 발생: {e}")

    # 5.
    def stop_instance(self, instance_name):

        if instance_name == "Cloud_Master":
            print(" *** WARNING ***\n Are you really want to stop MASTER node?[y/N] > ", end='')
            answer = input()
            if answer != 'y':
                return -1

        instance_id = find_instance_id_from_instance_name(
            process_list_instances(self.list_instances()), instance_name
        )
        if instance_id is None:
            print(" ** Name not found.. Try Instance ID instead > ", end='')
            instance_id = input()

        try:
            result = self._ec2_client.stop_instances(
                InstanceIds=[
                    instance_id
                ]
            )
            return result
        except Exception as e:
            print(f"인스턴스 중지 중 오류 발생: {e}")

    # 6.
    def create_instance(self, instance_params):
        # 매개변수 설정


        # EC2 인스턴스 생성
        try:
            instances = self._ec2_client.run_instances(**instance_params)
            return instances
        except Exception as e:
            print(f"인스턴스 생성 중 오류 발생: {e}")

    # 7.
    def reboot_instance(self, instance_name):
        if instance_name == "Cloud_Master":
            print(" *** WARNING ***\n Are you really want to reboot MASTER node?[y/N] > ", end='')
            answer = input()
            if answer != 'y':
                return -1

        instance_id = find_instance_id_from_instance_name(
            process_list_instances(self.list_instances()), instance_name
        )
        if instance_id is None:
            print(" ** Name not found.. Try Instance ID instead > ", end='')
            instance_id = input()

        try:
            result = self._ec2_client.reboot_instances(
                InstanceIds=[
                    instance_id
                ]
            )
            return result
        except Exception as e:
            print(f"인스턴스 중지 중 오류 발생: {e}")

    # 8.
    def list_images(self):
        user_id = self._sts_client.get_caller_identity().get('Account')
        try:
            images = self._ec2_client.describe_images(
                Owners=[
                    user_id     # 자신이 생성한 AMI 만 호출
                ],
                Filters=[
                    {'Name': 'state',
                     'Values': ['available']
                     }
                ],
                IncludeDeprecated=False,
                IncludeDisabled=False,
                MaxResults=10
            )['Images']
            return images
        except Exception as e:
            print(f"가용 image 조회 중 오류 발생: {e}")

    """ Additional functions """
