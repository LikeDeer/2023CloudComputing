import csv
import boto3
import subprocess
import paramiko

from modules.data_preprocessor import process_list_instances
from modules.finder import find_instance_id_from_instance_name


MASTER_PUBLIC_IP = "ec2-50-17-104-113.compute-1.amazonaws.com"
KEY_PEM_PATH = "resources/credentials/CloudComputingProjectKey.pem"


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

            self._next_slave_no = len(process_list_instances(self.list_instances()))

            print("연결 성공! Default Region: ", self._region,
                  "User: ", self._sts_client.get_caller_identity().get('Account'))
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
    def create_instance(self, count):
        info_path = "resources/"
        info_csv_name = "instance_creation_info.csv"
        f = open(info_path + info_csv_name, 'r', encoding='utf-8')
        rdr = csv.DictReader(f)

        creation_info = next(rdr, None)
        instance_params = {}
        if creation_info is not None:
            # BOM 문자 제거
            creation_info = {key.strip('\ufeff'): value for key, value in creation_info.items()}
            instance_params["ImageId"] = creation_info.get("Slave AMI")
            instance_params["InstanceType"] = "t2.micro"
            instance_params["SecurityGroupIds"] = [creation_info.get("Security Group Id")]
            instance_params["SecurityGroups"] = ["CloudSecurityGroup"]
            instance_params["KeyName"] = creation_info.get("Key Name")
            instance_params["MinCount"] = 1
            instance_params["MaxCount"] = 1

        # EC2 인스턴스 생성
        try:
            for i in range(count):
                response = self._ec2_client.run_instances(**instance_params)
                instance_id = response['Instances'][0]['InstanceId']
                self._ec2_client.create_tags(
                    Resources=[instance_id],
                    Tags=[
                        {'Key': 'Name', 'Value': f'Cloud_Slave{self._next_slave_no}'}
                    ]
                )
                self._next_slave_no += 1
            return 0
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
    def condor_status(self):
        cmd = f'ssh -i \"resources/credentials/CloudComputingProjectKey.pem\" ec2-user@{MASTER_PUBLIC_IP} condor_status'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result

    def ssh_to_master(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(MASTER_PUBLIC_IP,
                           username='ec2-user',
                           key_filename=KEY_PEM_PATH)
            print("Connection Complete. Type 'exit' to close the connection.")
            while True:
                print("$ ", end='')
                command = input()

                if command == 'exit':
                    break
                else:
                    stdin, stdout, stderr = client.exec_command(command)

                    output = stdout.read().decode('utf-8')
                    print(output)

        finally:
            client.close()

    def test_job_submit(self):
        count_sh_path = "resources/example/count.sh"
        multiple_jds_path = "resources/example/multiple.jds"
        destination = "test/"

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        transport = paramiko.Transport((MASTER_PUBLIC_IP, 22))

        try:
            client.connect(MASTER_PUBLIC_IP,
                           username='ec2-user',
                           key_filename=KEY_PEM_PATH)
            transport.connect(username='ec2-user', pkey=paramiko.RSAKey(filename=KEY_PEM_PATH))

            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(count_sh_path, destination + "count.sh")
            sftp.put(multiple_jds_path, destination + "multiple.jds")

            command = f"condor_submit ./test/multiple.jds"
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')

            print("Submitted an example program. Try '15. condor queue' to check it.")
            return output

        except Exception as e:
            print(f"작업 제출 중 오류 발생: {e}")

        finally:
            client.close()
            transport.close()

    def condor_queue(self):
        cmd = f'ssh -i \"resources/credentials/CloudComputingProjectKey.pem\" ec2-user@{MASTER_PUBLIC_IP} condor_q'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result

    def fetch_results(self):
        pass

    def condor_rm_all(self):
        cmd = f'ssh -i \"resources/credentials/CloudComputingProjectKey.pem\" ec2-user@{MASTER_PUBLIC_IP} condor_rm -all'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result
