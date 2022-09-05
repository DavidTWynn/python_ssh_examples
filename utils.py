from time import perf_counter
import asyncio


def import_inventory(file):
    with open(file, "r") as file:
        ips = [ip.split()[0] for ip in file.readlines()]
        return ips


def timer(func):
    """Async and regular decorator to run a perf_counter over function.
    Looks for args to check number of devices ran against."""
    if asyncio.iscoroutinefunction(func):
        async def wrapper(*args, **qwargs):
            num_devices = len(args[0])
            start = perf_counter()
            await func(*args, **qwargs)
            print(
                f"Finished {num_devices} devices in "
                f"{round(perf_counter() - start, 2)} seconds."
            )
        return wrapper

    else:
        def wrapper(*args, **qwargs):
            num_devices = len(args[0])
            start = perf_counter()
            func(*args, **qwargs)
            print(
                f"Finished {num_devices} devices in "
                f"{round(perf_counter() - start, 2)} seconds."
            )
    return wrapper
