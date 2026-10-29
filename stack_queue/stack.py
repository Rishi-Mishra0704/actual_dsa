class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        if len(self.stack) == 0:
            return -1
        return self.stack.pop()

    def top(self):
        if len(self.stack) == 0:
            return -1
        return self.stack[-1]

    def size(self):
        return len(self.stack)
