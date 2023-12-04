def find_instance_id_from_instance_name(instances, instance_name):
    for instance in instances:
        if instance.get('Name') == instance_name:
            return instance.get('InstanceId', 'Failed')
