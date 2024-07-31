import platform
import os
import psutil
import socket
import json


def get_os_info():
    os_info = {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    return os_info


def get_disk_usage():
    partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.device] = {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        }
    return disk_usage


def get_memory_info():
    memory = psutil.virtual_memory()
    memory_info = {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }
    return memory_info


def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    net_info = {
        "hostname": hostname,
        "ip_address": ip_address
    }
    return net_info


def baseline_scan():
    baseline_info = {
        "os_info": get_os_info(),
        "disk_usage": get_disk_usage(),
        "memory_info": get_memory_info(),
        "network_info": get_network_info()
    }
    return baseline_info


if __name__ == "__main__":
    scan_result = baseline_scan()
    # Print the scan result as a JSON formatted string for readability
    print(json.dumps(scan_result, indent=4))
