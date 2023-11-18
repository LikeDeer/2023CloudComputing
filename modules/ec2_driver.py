import boto3
from botocore.exceptions import NoCredentialsError


# noinspection PyMethodMayBeStatic
class EC2Driver:
    def __init__(self, access_key_id, secret_access_key):
        try:
            self._region = 'us-east-1'    # default region
            self._ec2 = boto3.resource('ec2', aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key,
                                       region_name=self._region)
            print("연결 성공! Default Region: ", self._region)
        except NoCredentialsError:
            print("AWS 자격 증명이 제공되지 않았습니다. 액세스 키 및 시크릿 액세스 키를 확인하세요.")
        except Exception as e:
            print(f"연결 중 오류 발생: {e}")

    # 1.
    def list_instances(self):
        try:
            instances = self._ec2.instances.all()
            return instances
        except Exception as e:
            print(f"리스트 조회 중 오류 발생: {e}")

    # 4.
    def available_regions(self):
        try:
            ec2_client = self._ec2.meta.client
            regions = [region['RegionName']
                       for region in ec2_client.describe_regions()['Regions']]
            return regions
        except Exception as e:
            print(f"가용 region 조회 중 오류 발생: {e}")
