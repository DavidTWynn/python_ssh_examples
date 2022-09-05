from pssh.clients import ParallelSSHClient

from secrets import Secrets
import utils


@utils.timer
def parallel_ssh_example(ips: str, username: str, password: str):
    """Runs show ip int b against all IPs passed in parallel."""    
    client = ParallelSSHClient(ips)

    # Set parallel SSH settings
    client.user = username
    client.password = password

    # Run commands against all IPs
    output = client.run_command("show ip int b | e una")
    for host_output in output:
        for line in host_output.stdout:
            print(line)


def main():
    # Import username and password from secrets.py class
    username = Secrets.username
    password = Secrets.password

    # Get ips from file
    ips = utils.import_inventory("inventory.txt")

    # Run parallel ssh
    parallel_ssh_example(ips, username, password)


if __name__ == '__main__':
    main()
