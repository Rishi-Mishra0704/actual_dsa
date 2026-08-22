from linked_list.linked_list import LinkedList

class ReverseLinkedList(LinkedList):
    def __init__(self):
        super().__init__()


    def reverse(self):
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
    

ll = ReverseLinkedList()
ll.append(1)
ll.append(2)
ll.append(3)

ll.print()
count = ll.count()
ll.reverse()
ll.print()
