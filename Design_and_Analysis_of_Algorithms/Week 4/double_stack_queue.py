class DoubleStackQueue:
    def __init__(self):
        self.current = [] # stack 
        self.temp = [] # stack
        self.removed = []

    def status(self):
        removed = [f'{elem} removed' for elem in self.removed] 
        elem_history = self.current + removed
        print('Status:\n')
        for elem in elem_history: 
            print(f'• {elem}\n')

    def enqueue(self, elements): 
        for elem in elements: 
            self.current.append(elem)

    def dequeue(self):
        while(len(self.current) > 1):
            self.temp.append(self.current.pop())

        dq_elem = self.current.pop()
        self.removed.append(dq_elem) # for status

        for i in range(len(self.temp)):
            self.current.append(self.temp.pop())


q = DoubleStackQueue()
q.enqueue([{'ID': 249, 'Name': 'Sam'}, {'ID': 903, 'Name': 'Anjali'}, {'ID': 781, 'Name': 'Robin'}])
q.enqueue([{'ID': 311, 'Name': 'Jo'}, {'ID': 684, 'Name': 'Emi'}])
q.dequeue()
q.dequeue()
q.status()

"""
Status:

• {'ID': 781, 'Name': 'Robin'}

• {'ID': 311, 'Name': 'Jo'}

• {'ID': 684, 'Name': 'Emi'}

• {'ID': 249, 'Name': 'Sam'} removed

• {'ID': 903, 'Name': 'Anjali'} removed
"""
