import socket
import select
import time

class socket_env:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("your_choice.ctf.fifthdoma.in", 8657))
        self.sock.settimeout(2)

    def send(self, msg) -> int:
        totalsent = 0
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        print(msg)
        return sent
    def receive(self) -> str:

        data=b''
        ready = select.select([self.sock], [], [], 2)
        if ready[0]:
            d= self.sock.recv(4096)

            data+=(d)

        return str(data.decode('ascii'))

def run(s: socket_env):
    r = (s.receive()).splitlines()
    print(f"received \n{r}\n")

    ret = r[-2]

    #time.sleep(0.5)
    print(f"last line is \n{ret}")

    s.send(bytes(ret[0]+"\n", 'ascii'))

    output=""
    while True:
        r = (s.receive()).splitlines()
        #print(f"received \n{r}\n")

        ret = r[-2]
        output+=r[-3]
        #time.sleep(0.5)
        #print(f"last line is \n{ret}")

        s.send(bytes(ret[0]+"\n", 'ascii'))
        print(f"output is \n {output}")





if __name__=="__main__":
    s = socket_env()
    #s.send(b'1\n')
    run(s)