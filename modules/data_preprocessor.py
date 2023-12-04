from datetime import datetime
import pytz


def process_list_instances(data):
    pre_instances = data.get('Reservations', [])

    processed_instances = []

    for reservation in pre_instances:
        for instance in reservation.get('Instances', []):
            post_instance = {
                'Name': instance['Tags'][0]['Value'],
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'PublicIpAddress': instance.get('PublicIpAddress', '-'),
                'PrivateIpAddress': instance.get('PrivateIpAddress', '-'),
                'LaunchTime': instance['LaunchTime'].astimezone(pytz.timezone('Etc/GMT')).strftime('%Y/%m/%d %H:%M %Z'),
                'SecurityGroups': ', '.join([group['GroupName'] for group in instance['SecurityGroups']]),
                'KeyName': instance.get('KeyName', '-'),
                'ImageId': instance['ImageId'],
                'Architecture': instance['Architecture'],
                'PlatformDetails': instance.get('PlatformDetails', 'N/A'),
            }
            processed_instances.append(post_instance)

    return processed_instances


def process_list_images(data):
    post_images = []

    for ami in data:
        info = {
            'Name': ami.get('Tags', '')[0]['Value'],
            'AMI name': ami.get('Name', ''),
            'AMI ID': ami.get('ImageId', ''),
            'Source': ami.get('SourceInstanceId', ''),
            'Platform': ami.get('PlatformDetails'),
            'Owner': ami.get('OwnerId', ''),
            'Visibility': 'Public' if ami.get('Public', False) else 'Private',
            'Status': ami.get('State', ''),
            'CreationDate': datetime.strptime(ami.get('CreationDate', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
                .astimezone(pytz.timezone('Etc/GMT'))
                .strftime('%Y/%m/%d %H:%M %Z')
        }
        post_images.append(info)

    return post_images


def process_available_zones(data):
    post_zones = []
    for zone in data:
        info = {
            'ZoneId': zone['ZoneId'],
            'ZoneName': zone['ZoneName'],
            'RegionName': zone['RegionName'],
            'State': zone['State'],
            'ZoneType': zone['ZoneType'],
            'NetworkBorderGroup': zone['NetworkBorderGroup']
        }
        post_zones.append(info)

    return post_zones


def process_available_regions(data):
    post_zones = []
    for zone in data:
        info = {
            'Endpoint': zone['Endpoint'],
            'RegionName': zone['RegionName']
        }
        post_zones.append(info)

    return post_zones



