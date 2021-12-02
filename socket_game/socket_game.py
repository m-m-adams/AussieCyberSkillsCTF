import socket
import select
import time
from agent import TDAgent


class socket_env:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("your_choice.ctf.fifthdoma.in", 8657))
        self.sock.settimeout(2)

    def reset(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("your_choice.ctf.fifthdoma.in", 8657))
        self.sock.settimeout(2)

    def send(self, msg) -> int:
        totalsent = 0
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        # print(msg)
        return sent

    def receive(self) -> str:

        data = b''
        ready = select.select([self.sock], [], [], 2)
        if ready[0]:
            d = self.sock.recv(4096)

            data += (d)

        return str(data.decode('ascii'))


def main():
    s = socket_env()
    agent = TDAgent()
    r = (s.receive()).splitlines()
    text = (r[-2]).split()
    a = str(agent.start(text))

    # time.sleep(0.5)
    print(f"last line is \n{r[-2]}")
    s.send(bytes(a+"\n", 'ascii'))
    output = ""
    while True:
        r = (s.receive()).splitlines()

        if len(r) > 2:
            text = (r[-2]).split()
            a = str(agent.step(1, text))

            output += r[-3]
            # time.sleep(0.5)
            # print(f"last line is \n{ret}")
            print(
                f'\rlast line is {text}, taking action {a}, output is {output}')
            s.send(bytes(a+"\n", 'ascii'))

        else:
            output = ''
            agent.end(-1)
            s.reset()
            r = (s.receive()).splitlines()
            text = (r[-2]).split()

            a = str(agent.start(text))
            print(f'\rLOST. last line is {text}, taking action {a}')
            s.send(bytes(a+"\n", 'ascii'))


if __name__ == "__main__":
    main()
