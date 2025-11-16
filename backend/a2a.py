# a2a.py - simple agent-to-agent bus
import queue, threading, time

class A2ABus:
    def __init__(self):
        self.queues = {}
        self.lock = threading.Lock()

    def create_agent_queue(self, agent_name):
        with self.lock:
            if agent_name not in self.queues:
                self.queues[agent_name] = queue.Queue()
        return self.queues[agent_name]

    def send(self, agent_name, message):
        q = self.create_agent_queue(agent_name)
        q.put(message)

    def receive(self, agent_name, timeout=0.1):
        q = self.create_agent_queue(agent_name)
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            return None
