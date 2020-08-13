# Import packages
import paramiko
import argparse
import boto.ec2
import json


def get_credentials():
    '''
    =================================================================
    Need AWS key and secret key. 
    These are stored in secrets.json. 
    This function loads this .json file and stores these credentials.
    =================================================================
    '''
    with open('./secrets.json') as data_file: 
        secrets = json.load(data_file)
    
    key = secrets['aws']['access_key_id']
    secret_key = secrets['aws']['secret_access_key']
    
    return secret_key, key


def get_ec2_urls(name):
    '''
    =================================================================
    Get EC2 URLs.
    =================================================================
    '''
    with open('./secrets.json') as data_file: 
        secrets = json.load(data_file)
    
    key_pair = secrets['ec2']['key_pair_file']
    username = secrets['ec2']['username']
    url = secrets['ec2'][name]
    
    return key_pair, username, url
    

def get_ec2_connection(key, secret_key):
    '''
    =================================================================
    Get a connection to the EC2 dashboard given the key and
    secret key.
    =================================================================
    '''
    conn = boto.ec2.connect_to_region("ap-south-1",
                                      aws_access_key_id=key,
                                      aws_secret_access_key=secret_key)
    
    return conn


def get_instance_info(key, secret_key):
    '''
    =================================================================
    Get dictionary with keys [instance name]: value [instance ID].
    =================================================================
    '''
    conn = get_ec2_connection(key, secret_key)
    reservations = conn.get_all_instances()
    
    instances = [i for r in reservations for i in r.instances]
    instance_info = {i.__dict__['tags']['Name']:i.__dict__['id'] for i in instances}
    
    names = instance_info.keys()
    return instance_info, names


def get_instance_ids(key, secret_key, names, target_names):
    '''
    =================================================================
    Get instance names.
    =================================================================
    '''
    conn = get_ec2_connection(key, secret_key)
    reservations = conn.get_all_instances()
    instance_ids = [names[name] for name in target_names]
    
    return(instance_ids)


def check_names(names, name):
    '''
    =================================================================
    Check whether a given name on which user 
    wants to perform action is indeed a valid EC2 
    instance. Return an AssertionError if not.
    =================================================================
    '''
    assert name in names
    
    return


def launch_instance(key, secret_key):
    '''
    =================================================================
    Launch a new t2.small instance using the paydash-hh-pull AMI
    and security group.
    =================================================================
    '''
    
    conn = get_ec2_connection(key, secret_key)
    conn.run_instances('ami-09b370c460434b12c', 
                       key_name='paydash-etl', 
                       instance_type='t2.small', 
                       security_groups=['launch-wizard-5'])


def restart_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Restart a stopped instance.
    =================================================================
    '''
    
    conn = get_ec2_connection(key, secret_key)
    conn.start_instances(instance_ids = target_instance_ids)


def reboot_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Reboot instances.
    =================================================================
    '''
    
    conn = get_ec2_connection(key, secret_key)
    conn.reboot_instances(instance_ids=target_instance_ids)


def stop_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Stop an instance with a given name.
    =================================================================
    '''
    
    conn = get_ec2_connection(key, secret_key)
    conn.stop_instances(instance_ids=target_instance_ids)


def ssh_connect(url, key_file, username):
    '''
    =================================================================
    Connect to server using ssh.
    =================================================================
    '''
    
    # Print 
    print 'Here is the key pair: {}'.format(key_file)
    print 'Here is the username: {}'.format(username)
    print 'Here is the URL: {}'.format(url)
    
    # Connect using ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(url,key_filename=key_file,username=username)
    
    return ssh
    

def delete_cron(ssh):
    '''
    =================================================================
    Delete all existing cron jobs from server.
    =================================================================
    '''
    
    # Execute command to remove all cronjobs
    cmd = "crontab -r"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    
    # Read data line by line
    data = stdout.read().splitlines()
    for line in data: print line
    ssh.close()


def set_cron(ssh, job):
    '''
    =================================================================
    Set new cron-tab on specified instance given an ssh
    client object and job details.
    =================================================================
    '''
    
    # Print 
    print 'Here is the job: {}'.format(job)
    
    # Execute command to set cron job
    cmd = '''(crontab -l 2>/dev/null; echo "{}") | crontab -'''.format(job) 
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    
    # Read data line by line
    data = stdout.read().splitlines()
    for line in data: print line
    ssh.close()


def main():
    '''
    =================================================================
    Excute the complete code.
    =================================================================
    '''
    # Get credentials
    secret_key, key = get_credentials()
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help = "Add the state code here...", type = str)
    parser.add_argument("name", help = "Add the financial year here...", type = str)
    parser.add_argument("--job", help = "Add the financial year here...", type = str)
    
    # Store the action and name you want to take here
    args = parser.parse_args()
    action = args.action
    name = args.name
    job = args.job
    
    # Make sure that there is an EC2 instance with the given name
    instance_info, names = get_instance_info(key, secret_key)
    
    # Check whether the name is valid and get the IDs
    check_names(names, name)
    target_instance_ids = [instance_info[name]]
    
    # Execute
    if action == 'restart': 
        restart_instance(key, secret_key, target_instance_ids)
    
    if action == 'reboot': 
        reboot_instance(key, secret_key, target_instance_ids)
    
    if action == 'stop': 
        stop_instance(key, secret_key, target_instance_ids)
    
    if action == 'launch': 
        launch_instance(key, secret_key)
    
    if action == 'del':
        key_pair, username, url = get_ec2_urls(name)
        ssh = ssh_connect(url, key_pair, username)
        delete_cron(ssh)
        
    if action == 'set':
        key_pair, username, url = get_ec2_urls(name)
        ssh = ssh_connect(url, key_pair, username)
        set_cron(ssh, job)
    

# Execute the code    
if __name__ == '__main__':
    main()