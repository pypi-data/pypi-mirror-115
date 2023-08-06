import os
import logging
import subprocess

import requests

from master import utils
from master.k8s import k8s

CALICO_YAML_URL = 'https://docs.projectcalico.org/v3.8/manifests/calico.yaml'


def setup():
    logging.info("[Setup]\n")

    # get configuration
    iface = utils.get_default_iface()
    token = utils.get_join_token()
    kube_version, cni_version, docker_version = utils.get_compatible_versions()

    # Run install-master script from internet
    env = os.environ
    env = dict({
        "ADVERTISE_NET_DEV": iface,
        "JOIN_TOKEN": token,
        "KUBERNETES_VERSION": kube_version,
        "KUBERNETES_CNI_VERSION": cni_version,
        "DOCKER_VERSION": docker_version
    }, **env)
    command = "cd /tmp && curl -s https://raw.githubusercontent.com/AI-Ocean/kubernetes-install-scripts/main/install-master.sh | bash"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    # print progress
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode())

    return True


def setup_calico(pod_cidr):
    logging.info('Installing calico...')
    response = requests.get(url=CALICO_YAML_URL)

    # 별도의 pod cidr을 명시한 경우에 replace 해준다.
    manifest = response.text.replace('192.168.0.0/16', pod_cidr) if pod_cidr else response.text
    k8s.create_resources_from_yaml(manifest)

    logging.info('Completed install calico.')


def setup_system_service():
    response = requests.get(url='https://raw.githubusercontent.com/AI-Ocean/kubernetes-install-scripts/main/ocean-agent.service')
    with open("/lib/systemd/system/ocean-agent.service", "w") as f:
        f.write(response.text)

    subprocess.check_output(['systemctl', 'daemon-reload'])
    subprocess.check_output(['systemctl', 'restart', 'ocean-agent'])