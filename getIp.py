import socket
import psutil
def get_network_info():
    interfaces = {}
    for iface, addrs in psutil.net_if_addrs().items():
        if iface.lower() in {"lo", "loopback"}:
            continue

        ip_info = []
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_info.append({
                    "type": "IPv4",
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            elif addr.family == socket.AF_INET6:
                ip_info.append({
                    "type": "IPv6",
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            elif addr.family == psutil.AF_LINK:
                ip_info.append({
                    "type": "MAC",
                    "address": addr.address
                })

        if ip_info:
            interfaces[iface] = ip_info
    return interfaces

if __name__ == "__main__":

    print(psutil.net_if_addrs())


