import os
import random
import string
import subprocess
from functools import lru_cache
import time
import urllib3

import netifaces as ni
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_default_iface():
    default_iface = [iface for iface in os.listdir('/sys/class/net/') if iface != 'lo' and iface != 'docker0'][0]
    return default_iface


@lru_cache()
def get_join_token(ttl_hash=None):
    if check_kubeadm_initialized():
        return str(subprocess.check_output(['kubeadm', 'token', 'create']).decode("utf-8").strip())
    else:
        return f'{get_random_string(6)}.{get_random_string(16)}'


def get_ttl_hash(seconds=1800):
    return round(time.time() / seconds)


# 바꾸지 않아도 문제는 없으니 일단 이대로 놔둔다.
def get_compatible_versions():
    kube_version = "1.20.8-00"
    cni_version = "0.8.7-00"
    docker_version = "5:19.03.15~3-0~ubuntu-bionic"

    return kube_version, cni_version, docker_version


# default iface의 1번째 IP만을 반환한다. NIC에 IP가 여러개 붙어있는 경우는 고려하지 않음.
def get_api_server_address(nic):
    if nic:
        return ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
    else:
        return ni.ifaddresses(get_default_iface())[ni.AF_INET][0]['addr']


def get_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def check_kubeadm_initialized():
    try:
        response = requests.get('https://localhost:6443', verify=False)
        if response.status_code == 403: # If api server is running, 403 should be returned
            return True
    except requests.exceptions.ConnectionError:
        return False
