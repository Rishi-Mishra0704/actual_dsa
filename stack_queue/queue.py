from collections import deque


class Queue:
    def __init__(self):
        self.queue = deque()

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        if len(self.queue) == 0:
            return -1
        return self.queue.popleft()

    def front(self):
        if len(self.queue) == 0:
            return -1
        return self.queue[0]

    def size(self):
        return len(self.queue)
