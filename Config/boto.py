import boto
from boto.ec2.regioninfo import RegionInfo
from pprint import pprint
import time 
import argparse
from boto.ec2.connection import EC2Connection


region=RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ACCESS_KEY = "a0af414faac1407d8e15f3ed41fd73f4"
SECRET_KEY = "9a3f5e1e7528454b9f98cbb1047958da"


conn = boto.connect_ec2(aws_access_key_id= ACCESS_KEY, 
aws_secret_access_key= SECRET_KEY, is_secure=True,
region=region, 
port=8773, 
path='/services/Cloud', 
validate_certs=False)

#get all the images
#images = conn.get_all_images()


# set the image for instance
#img = conn.get_image('ami-c163b887')

#print("Image name :"+img.name)

#get security groups
#sec = conn.get_all_security_groups()

#sec_group = []

#create an instance
def createInstance():
	new_instance = conn.run_instances('ami-c163b887',
		key_name='cloud',
		instance_type='m2.small',
		security_groups=['ssh','http','icmp','default'],
		placement='melbourne-np')
	instance = new_instance.instances[0]
	# wait for running 
	while instance.update() != 'running':
		time.sleep(5)

	print (instance.private_ip_address)
	return instance.private_ip_address



# teerminate the instance
def terminate_instance(new_instance_id):
	return get_instance(new_instance_id).terminate()



if __name__ == '__main__':
	keyboard = argparse.ArgumentParser()
	keyboard.add_argument('-operation', type=str, help='launch or terminate')
	keyboard.add_argument('-n',type=int,help='number of instance to create')
	keyboard.add_argument('-id',type=str,help='terminate instance id')
	args = keyboard.parse_args()

  	address = []
  	if args.operation == 'launch':
  		for i in range(args.n):
  			address.append(createInstance())
  	print(address)

  	if args.operation == 'terminate':
  		terminate_instance(args.id)

  	else:
  		keyboard.print_help()
    





