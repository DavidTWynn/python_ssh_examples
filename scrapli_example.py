import asyncio
from scrapli.driver.core import AsyncIOSXEDriver
from scrapli import response

from secrets import Secrets
import utils


def create_scrapli_inv(ips: list, username: str, password: str) -> list[dict]:
    """Creates list of dicts inventory for scrapli async drivers."""
    devices = []
    for ip in ips:
        device = {
            "host": ip,
            "auth_username": username,
            "auth_password": password,
            "auth_strict_key": False,
            "transport": "asyncssh",
        }
        devices.append(device)
    return devices


async def show_ip(device: dict) -> response:
    """Asynchronously send show ip int b to device.
    Requires scrapli device inventory."""
    async with AsyncIOSXEDriver(**device) as conn:
        version_result = await conn.send_command("show ip int b | e una")
    return version_result


@utils.timer
async def run_scrapli(devices: list[dict]) -> None:
    """Run async scrapli show commands against list of devices.
    Devices are scrapli inventory dicts."""
    coroutines = [show_ip(device) for device in devices]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(result.result)


def main():
    # Import username and password from secrets.py class
    username = Secrets.username
    password = Secrets.password

    # Get ips from file
    ips = utils.import_inventory("inventory.txt")

    # Get scrapli formatted list of dicts to run
    devices = create_scrapli_inv(ips, username, password)
    # Run scrapli async
    asyncio.get_event_loop().run_until_complete(run_scrapli(devices))


if __name__ == "__main__":
    main()
