# Import packages
import paramiko
import argparse
import boto.ec2
import json


def test_get_credentials():
    '''
    =================================================================
    Need AWS key and secret key. 
    These are stored in secrets.json. 
    This function loads this .json file and stores these credentials.
    =================================================================
    '''
    pass


def test_get_ec2_urls(name):
    '''
    =================================================================
    Get EC2 URLs.
    =================================================================
    '''
    pass
    

def test_get_ec2_connection(key, secret_key):
    '''
    =================================================================
    Get a connection to the EC2 dashboard given the key and
    secret key.
    =================================================================
    '''
    pass


def test_get_instance_info(key, secret_key):
    '''
    =================================================================
    Get dictionary with keys [instance name]: value [instance ID].
    =================================================================
    '''
    pass


def test_get_instance_ids(key, secret_key, names, target_names):
    '''
    =================================================================
    Get instance names.
    =================================================================
    '''
    pass


def test_launch_instance(key, secret_key):
    '''
    =================================================================
    Launch a new t2.small instance using the paydash-hh-pull AMI
    and security group.
    =================================================================
    '''
    pass


def test_restart_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Restart a stopped instance.
    =================================================================
    '''
    pass


def test_reboot_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Reboot instances.
    =================================================================
    '''
    pass

def test_stop_instance(key, secret_key, target_instance_ids):
    '''
    =================================================================
    Stop an instance with a given name.
    =================================================================
    '''
    pass


def test_ssh_connect(url, key_file, username):
    '''
    =================================================================
    Connect to server using ssh.
    =================================================================
    '''
    pass
    

def test_delete_cron(ssh):
    '''
    =================================================================
    Delete all existing cron jobs from server.
    =================================================================
    '''
    pass



def test_set_cron(ssh, job):
    '''
    =================================================================
    Set new cron-tab on specified instance given an ssh
    client object and job details.
    =================================================================
    '''
    pass




def main(): 
    '''
    =================================================================
    Execute tests
    =================================================================
    '''


if __name__ == '__main__':

    main()