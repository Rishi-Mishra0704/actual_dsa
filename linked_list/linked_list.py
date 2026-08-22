class Node:
    def __init__(self, val=0, nextNode=None):
        self.val = val
        self.next = nextNode
        

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self,val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
            
        current.next = new_node

    def count(self):
        count = 0
        current = self.head
        while current:
            count+=1
            current = current.next
        return count

    def print(self):
      
        current = self.head
        while current:
            print(current.val,end="->")
            current = current.next
        print("None")

    def insert_at(self, index, value):
        if index < 0:
            raise IndexError('index cannot be negative')

        new_node = Node(value)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        for _ in range(index - 1):
            if current is None:
                raise IndexError('index out of range')
            current = current.next

        if current is None:
            raise IndexError('index out of range')

        new_node.next = current.next
        current.next = new_node
    
    def remove_at(self,index):
        if index < 0:
            raise IndexError("index cannot be negative")

        if self.head is None:
            raise IndexError("cannot delete from empty list")

        if index == 0:
            self.head = self.head.next
            return
        
        current = self.head
        for _ in range(index-1):
            if current is None:
                raise IndexError("index out of bound")

            current = current.next

        if current is None or current.next is None:
               raise IndexError("index out of bound")

        current.next = current.next.next
ll = LinkedList()

ll.append(1)
ll.append(2)
ll.append(3)

ll.print()
count = ll.count()
print(count)
ll.insert_at(1,99)
ll.print()
count = ll.count()
print(count)
ll.remove_at(1)
ll.print()
count = ll.count()
print(count)
