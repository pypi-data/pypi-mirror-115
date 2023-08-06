import subprocess
import os
import logging

from master import utils


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
