import boto3

#session = boto3.Session()

ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type, instance.key_name, instance.private_ip_address, instance.public_dns_name)
