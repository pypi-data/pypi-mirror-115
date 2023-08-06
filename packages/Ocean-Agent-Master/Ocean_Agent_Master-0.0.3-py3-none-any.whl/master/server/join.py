import logging

from master import utils


def join():
    logging.info("[Join]")

    # send join info
    token = utils.get_join_token(ttl_hash=utils.get_ttl_hash())
    kube_version, cni_version, docker_version = utils.get_compatible_versions()
    api_addr = utils.get_api_server_address()

    join_info = {
        "API_SERVER_ADDR": api_addr,
        "JOIN_TOKEN": token,
        "KUBERNETES_VERSION": kube_version,
        "KUBERNETES_CNI_VERSION": cni_version,
        "DOCKER_VERSION": docker_version
    }

    return join_info