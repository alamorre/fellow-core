from games.models import Block


class BlockQueue:
    def __init__(self):
        self.items = []
        self.visited = set()

    def is_empty(self):
        """
        This method checks if the queue is empty
        :return: boolean on if the queue is empty
        """
        return self.items == []

    def enqueue_unique(self, item):
        """
        This method checks and adds only unique Blocks in O(1)
        :param item: Block obj
        :return: void
        """
        if item not in self.visited:
            self.items.insert(0, item)
            self.visited.add(item)

    def dequeue(self):
        """
        This method removes the oldest item from queue
        :return: Block obj
        """
        return self.items.pop()


# Get the top left neighbour block if it exists
def get_top_left(block):
    return Block.objects.get(game=block.game,
                             index=block.index - 11) if block.index > 9 and block.index % 10 is not 0 else None


# Get the top center neighbour block if it exists
def get_top(block):
    return Block.objects.get(game=block.game, index=block.index - 10) if block.index > 9 else None


# Get the top right neighbour block if it exists
def get_top_right(block):
    return Block.objects.get(game=block.game,
                             index=block.index - 9) if block.index > 9 and block.index % 10 is not 9 else None


# Get the left neighbour block if it exists
def get_left(block):
    return Block.objects.get(game=block.game, index=block.index - 1) if block.index % 10 is not 0 else None


# Get the Right neighbour block if it exists
def get_right(block):
    return Block.objects.get(game=block.game, index=block.index + 1) if block.index % 10 is not 9 else None


# Get the bottom left neighbour block if it exists
def get_bottom_left(block):
    return Block.objects.get(game=block.game,
                             index=block.index + 9) if block.index < 90 and block.index % 10 is not 0 else None


# Get the bottom center neighbour block if it exists
def get_bottom(block):
    return Block.objects.get(game=block.game, index=block.index + 10) if block.index < 90 else None


# Get the bottom right neighbour block if it exists
def get_bottom_right(block):
    return Block.objects.get(game=block.game,
                             index=block.index + 11) if block.index < 90 and block.index % 10 is not 9 else None


def check_no_mines(block):
    """
    This function checks if there are no nearby mines
    :param block: Block obj
    :return: true if no mines are near, false otherwise
    """
    # Make sure this block is not a mine
    if block.is_mine:
        return False

    # Get the top neighbours
    top_left = get_top_left(block)
    top = get_top(block)
    top_right = get_top_right(block)

    # Check if the top neighbours are not mines
    if (hasattr(top_left, 'is_mine') and top_left.is_mine) or (hasattr(top, 'is_mine') and top.is_mine) or (
            hasattr(top_right, 'is_mine') and top_right.is_mine):
        return False

    # Get the side neighbours
    left = get_left(block)
    right = get_right(block)

    # Check if the side neighbours are not mines
    if (hasattr(left, 'is_mine') and left.is_mine) or (hasattr(right, 'is_mine') and right.is_mine):
        return False

    # Get the bottom neighbours
    bottom_left = get_bottom_left(block)
    bottom = get_bottom(block)
    bottom_right = get_bottom_right(block)

    # Check if the bottom neighbours are not mines
    if (hasattr(bottom_left, 'is_mine') and bottom_left.is_mine) or (hasattr(bottom, 'is_mine') and bottom.is_mine) or (
            hasattr(bottom_right, 'is_mine') and bottom_right.is_mine):
        return False

    # If all pass, this tile has no nearby neighbours
    return True


class Sweeper:
    def breadth_first_sweep(self, first_block):
        """
        This function does a breadth first search of (right angle) adjacent blocks with no nearby mines
        :param first_block: Block obj
        :return: void
        """
        # Put the first block into the queue
        q = BlockQueue()
        q.enqueue_unique(first_block)

        # Keep filling the queue with 0 blocks
        while not q.is_empty():
            block = q.dequeue()

            # Check if the block has no nearby mines
            if check_no_mines(block):
                block.is_flipped = True
                block.save()

                # Flip then try enqueueing the top block
                temp = get_top(block)
                if temp is not None:
                    if check_no_mines(temp):
                        q.enqueue_unique(temp)
                    temp.is_flipped = True
                    temp.save()

                # Flip then try enqueueing the bottom block
                temp = get_bottom(block)
                if temp is not None:
                    if check_no_mines(temp):
                        q.enqueue_unique(temp)
                    temp.is_flipped = True
                    temp.save()

                # Flip then try enqueueing the left block
                temp = get_left(block)
                if temp is not None:
                    if check_no_mines(temp):
                        q.enqueue_unique(temp)
                    temp.is_flipped = True
                    temp.save()

                # Flip then try enqueueing the right block
                temp = get_right(block)
                if temp is not None:
                    if check_no_mines(temp):
                        q.enqueue_unique(temp)
                    temp.is_flipped = True
                    temp.save()

                # Simply flip the corners
                for c in [get_top_left(block), get_top_right(block), get_bottom_left(block), get_bottom_right(block)]:
                    if c is not None:
                        c.is_flipped = True
                        c.save()


sweeper = Sweeper()
