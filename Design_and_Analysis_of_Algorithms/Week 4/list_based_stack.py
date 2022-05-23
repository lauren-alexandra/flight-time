"""
Compares the performance of a list based stack and a queue with linked list implementation.
"""

import time

def main():

    class Stack:
        def __init__(self):
            self.list = []

        def push(self, data):
            self.list.append(data)

        def pop(self): 
            return self.list.pop()

        def peek(self):
            return self.list[-1]

    class Node:
        def __init__ (self, data=None):
            self.data = data 
            self.next = None

    class Queue:
        def __init__(self):
            self.tail = None

        def enqueue(self, data):
            node = Node(data)
            if self.tail == None:
                self.tail = node 
            else:
                current = self.tail 
                while current.next:
                    current = current.next 
                current.next = node

        def dequeue(self): 
            current = self.tail
            removed_item = current.data
            self.tail = current.next
            return removed_item

        def peek(self):
            return self.tail.data


    t1_start = time.perf_counter()
    q = Queue()
    print('\nEnqueue melon')
    q.enqueue('melon')
    print('Enqueue grapes')
    q.enqueue('grapes')
    print('Enqueue oranges')
    q.enqueue('oranges')
    print('Enqueue pineapples')
    q.enqueue('pineapples')
    print('Dequeue')
    q.dequeue()
    print(f'Peek: {q.peek()}')
    t1_stop = time.perf_counter()
    print(f"Queue operations total: {t1_stop - t1_start:.6f} seconds\n")

    t2_start = time.perf_counter()
    stack = Stack()
    print('\nPush melon')
    stack.push('melon')
    print('Push grapes')
    stack.push('grapes')
    print('Push oranges')
    stack.push('oranges')
    print('Push pineapples')
    stack.push('pineapples')
    print('Pop')
    stack.pop()
    print(f'Peek: {stack.peek()}')
    t2_stop = time.perf_counter()
    print(f"Stack operations total: {t2_stop - t2_start:.6f} seconds")

if __name__ == "__main__":
    main()
