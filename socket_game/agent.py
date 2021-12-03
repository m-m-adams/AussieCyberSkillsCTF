import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import optimizer
import numpy as np
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


class TDAgent():
    class Net(nn.Module):

        def __init__(self):
            super().__init__()
            self.embed = nn.Embedding(7, 2)
            self.fc = nn.Linear(5, 5)
            self.fcout = nn.Linear(5, 1)

        def forward(self, x):

            hidden = F.relu(self.fc(x.to(torch.float)))
            return self.fcout(hidden)

    def __init__(self, seed=0, step_size=0.01, discount_factor=0.8, beta_m=0.9, beta_v=0.1, eps=0.25):

        # Set random seed for weights initialization for each run
        self.rand_generator = np.random.RandomState(seed)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.device = 'cpu'
        self.valuenetwork = self.Net().to(self.device)

        self.optimizer = optim.Adam(
            self.valuenetwork.parameters(), lr=step_size)
        # Set random seed for policy for each run
        self.policy_rand_generator = np.random.RandomState(
            seed)

        self.gamma = discount_factor
        self.beta = beta_v
        self.epsilon = eps
        self.steps = 0
        self.action_space = torch.tensor([0, 1])
        self.meanR = 0
        self.last_state = None
        self.last_action = None
        self.tokens = {}
        self.token_count = 0

    def word2token(self, word: str):
        if word in self.tokens:
            return self.tokens[word]
        else:
            print(f"new word {word}")
            self.token_count += 1
            self.tokens[word] = self.token_count
            return self.token_count

    def state2tensor(self, state):
        #v = self.word2token(state[0])
        return torch.tensor([self.word2token(v) for v in state])

    def policy(self, state):
        state_vec = self.state2tensor(state)
        # Set chosen_action as 0 or 1 with equal probability.
        maxv = -np.Inf
        a = self.action_space[0]
        for action in self.action_space:
            features = torch.cat(
                (action.unsqueeze(0), state_vec), 0).unsqueeze(0)
            v = self.valuenetwork(features.to(self.device))
            if v > maxv:
                maxv = v
                a = action
        r = self.policy_rand_generator.uniform(0, 1)
        if r > self.epsilon:
            return a
        else:
            print("picking randomly")
            chosen_action = torch.tensor(
                self.policy_rand_generator.choice([0, 1]))
            return chosen_action

    def start(self, state):

        self.last_state = self.state2tensor(state)
        self.last_action = self.policy(state)

        return self.last_action.cpu().numpy()

    def step(self, reward, state):
        """A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (Numpy array): the state from the
                environment's step based, where the agent ended up after the
                last step
        Returns:
            The action the agent is taking.
        """

        # Compute TD error (5 lines)
        # delta = None
        self.optimizer.zero_grad()
        ### START CODE HERE ###
        self.steps += 1
        if self.steps > 100:
            self.epsilon = 0.001
        last_state = self.last_state

        # add the last action to the feature vector
        features = torch.cat(
            (self.last_action.unsqueeze(0), last_state), 0).unsqueeze(0)
        v_last = self.valuenetwork(features.to(self.device))

        curr_state = self.state2tensor(state)
        a = self.policy(state)
        features = torch.cat((a.unsqueeze(0), curr_state), 0).unsqueeze(0)
        v = self.valuenetwork(features.to(self.device))

        delta = reward - self.meanR + v - v_last

        self.meanR = self.meanR + self.beta*delta

        # print(v_last, target)
        L = nn.MSELoss()
        loss = L(v_last, delta.detach())

        loss.backward()
        self.optimizer.step()

        # update self.last_state and self.last_action (2 lines)

        ### START CODE HERE ###
        self.last_state = curr_state
        self.last_action = a
        ### END CODE HERE ###

        return self.last_action.cpu().numpy()

    def end(self, reward):
        """Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """

        # compute TD error (3 lines)
        # delta = None

        ### START CODE HERE ###
        last_state = self.last_state

        features = torch.cat(
            (self.last_action.unsqueeze(0), last_state), 0).unsqueeze(0)
        v_last = self.valuenetwork(features.to(self.device))

        delta = reward - self.meanR - v_last

        self.meanR = self.meanR + self.beta*delta

        # print(v_last, target)
        L = nn.MSELoss()
        loss = L(v_last, delta.detach())
        loss.backward()
        self.optimizer.step()


if __name__ == "__main__":
    main()
