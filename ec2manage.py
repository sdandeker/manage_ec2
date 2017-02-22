#!/usr/bin/env python
"""
Required:
   boto
   IAM account credentials with EC2 instances describe,start,stop privileges
"""
import boto3.ec2
import sys

#### Configuration section ####
IAM_ID = '<AWS IAM ID info>'  # or use env variables
IAM_SECRET ='<AWS IAM Secret info>' # or use env variables
REGION = '<your_region>'  #  e.g. us-east-1

instances_list = ['i-0a733fb92d56f144a']

### End Configuration section ###

conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=IAM_ID, aws_secret_access_key=IAM_SECRET)
USAGE = "Usage: %s (start|stop|status)" % sys.argv[0]
try:
    cmdarg = sys.argv[1]
    if cmdarg not in ['start','stop','status']:
        print "Unknown arg: %s" % cmdarg
        print USAGE
        sys.exit(1)
except IndexError:
    print "Missing option(s)"
    print USAGE
    sys.exit(1)

for i in instances_list:
    instance = conn.get_all_instances(instance_ids=[i])
    inst_state = instance[0].instances[0].state   
    inst_priv_ip = instance[0].instances[0].private_ip_address
    inst_nametag = instance[0].instances[0].tags['Name']
    if cmdarg == 'status':
        print "instance: %s  %s  %s   %s" % (i,inst_nametag, inst_priv_ip, inst_state)
        continue
    if cmdarg == 'start':
        if inst_state == 'stopped':
            print "starting instance %s  %s" % (i,inst_nametag)
            instance[0].instances[0].start()
        else:
            print "skipped: %s %s state is %s" % (i, inst_nametag, inst_state) 
        continue
    if cmdarg == 'stop':
        if inst_state == 'running':
            print "stopping instance %s %s" % (i, inst_nametag)
            instance[0].instances[0].stop()
        else:
            print "skipped: %s %s state is %s" % (i, inst_nametag, inst_state)
        continue
