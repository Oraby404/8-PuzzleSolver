class Queue:

    def __init__(self):
        self.queue = []

    # Add an element
    def enqueue(self, newElement):
        self.queue.append(newElement)

    # Remove an element
    #initialize queue with front and rear at -1
    def dequeue(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    # Display  the queue
    def display(self):
        print(self.queue)

    def size(self):
        return len(self.queue)
    def isEmpty(self):
        return len(self.queue) == -1
