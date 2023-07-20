import socket
import time


def check_connection_status(host, port):
  s = socket.socket()
  ip_address = socket.gethostbyname(host)
  try:
    print(f"Checking {host}:{port} at {ip_address} connection status")
    s.connect((host, port))
  except Exception as e:
    s.close()
    print(f"No, {host}:{port} connection is not yet open. Retry in 5sec.")
    time.sleep(5)
    return check_connection_status(host, port)
  print(f"Ok, {host} connection is open!")
  s.close()