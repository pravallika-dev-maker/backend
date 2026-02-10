import socket

def check_port(host, port):
    print(f"Checking {host}:{port}...")
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("  CONNECTED!")
        s.close()
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False

hosts = [
    "db.yibpjemrwzawgxdcnmsw.supabase.co",
    "aws-0-ap-south-1.pooler.supabase.com",
    "aws-1-ap-south-1.pooler.supabase.com"
]

for h in hosts:
    check_port(h, 5432)
    check_port(h, 6543)
