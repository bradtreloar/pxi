from paramiko import AutoAddPolicy, SSHClient
from scp import SCPClient  # type: ignore
import sys


def get_scp_client(hostname: str, username: str, password: str):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(hostname, username=username, password=password)
    scp_client = SCPClient(ssh_client.get_transport())
    return scp_client
