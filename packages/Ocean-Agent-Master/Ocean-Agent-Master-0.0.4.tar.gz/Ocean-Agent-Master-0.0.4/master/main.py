# TODO: worker의 ws endpoint를 자동으로 마스터 향하게 하기
# boot.sh에서 python3 고려하기
# master에서 NIC 선택할 수 있게 하기
# master setup 실행한 다음 자동으로 서버를 system service로 등록하기
import logging

import click

from master import utils
from master.cmd.setup import setup as master_setup
from master.cmd.serve import serve as master_serve
from master.cmd.serve import PORT

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


@click.group()
def cli():
    pass


@cli.command()
def setup():
    if not utils.check_kubeadm_initialized():
        master_setup()
        # TODO: master server를 system service로 옮기기 자동화

    logging.info(f"""\n
    Run below command in all worker servers.
    > agent-worker join --master-endpoint={utils.get_api_server_address()}:{PORT}
    """)


@cli.command()
def serve():
    master_serve()


if __name__ == "__main__":
    cli()