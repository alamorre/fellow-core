from games.models import Block


class BlockQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Sweeper:
    def breadth_first_sweep(self, block):
        print('breadth first sweep!')
        print('start with ' + str(block))


sweeper = Sweeper()
