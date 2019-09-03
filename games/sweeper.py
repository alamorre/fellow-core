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


def get_top_left(block):
    return Block.objects.get(game=block.game,
                             index=block.index - 11) if block.index > 9 and block.index % 10 is not 0 else None


def get_top(block):
    return Block.objects.get(game=block.game, index=block.index - 10) if block.index > 9 else None


def get_top_right(block):
    return Block.objects.get(game=block.game,
                             index=block.index - 9) if block.index > 9 and block.index % 10 is not 9 else None


def get_left(block):
    return Block.objects.get(game=block.game, index=block.index - 1) if block.index % 10 is not 0 else None


def get_right(block):
    return Block.objects.get(game=block.game, index=block.index + 1) if block.index % 10 is not 9 else None


def get_bottom_left(block):
    return Block.objects.get(game=block.game,
                             index=block.index + 9) if block.index < 90 and block.index % 10 is not 0 else None


def get_bottom(block):
    return Block.objects.get(game=block.game, index=block.index + 10) if block.index < 90 else None


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
        visited = BlockQueue()
        q.enqueue(first_block)

        # Keep filling the queue with 0 blocks
        while not q.is_empty():
            block = q.dequeue()
            visited.enqueue(block)
            print(str(block))

            # Check if the block has no nearby mines
            if check_no_mines(block):
                block.is_flipped = True
                block.save()

                # Try flipping then adding the top block to queue
                temp = get_top(block)
                if temp is not None:
                    if check_no_mines(temp) and temp not in visited.items:
                        q.enqueue(temp)
                    temp.is_flipped = True
                    temp.save()

                # Try flipping then adding the bottom block to queue
                temp = get_bottom(block)
                if temp is not None:
                    if check_no_mines(temp) and temp not in visited.items:
                        q.enqueue(temp)
                    temp.is_flipped = True
                    temp.save()

                # Try flipping then adding the left block to queue
                temp = get_left(block)
                if temp is not None:
                    if check_no_mines(temp) and temp not in visited.items:
                        q.enqueue(temp)
                    temp.is_flipped = True
                    temp.save()

                # Try flipping then adding the right block to queue
                temp = get_right(block)
                if temp is not None:
                    if check_no_mines(temp) and temp not in visited.items:
                        q.enqueue(temp)
                    temp.is_flipped = True
                    temp.save()

                # Simply flip the corners
                temp = get_top_left(block)
                if temp is not None:
                    temp.is_flipped = True
                    temp.save()

                temp = get_top_right(block)
                if temp is not None:
                    temp.is_flipped = True
                    temp.save()

                temp = get_bottom_left(block)
                if temp is not None:
                    temp.is_flipped = True
                    temp.save()

                temp = get_bottom_right(block)
                if temp is not None:
                    temp.is_flipped = True
                    temp.save()

sweeper = Sweeper()
