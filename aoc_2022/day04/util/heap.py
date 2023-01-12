import copy


def left_index(index):
    return 2 * index + 1


def right_index(index):
    return 2 * index + 2


def parent_index(index):
    return (index - 1)//2


class MaxHeap:
    def __init__(self, input: list = None, record=False):
        if input == None:
            input = []
        self._values = input
        self._record = record
        self._history = []
        self.record()

    def sorted(self):
        original_values = copy.copy(self._values)
        sorted = []
        while len(self) > 0:
            sorted.append(self.remove_max())
        self._values = original_values
        return sorted

    def insert(self, node):
        self._values.append(node)
        self._sort_up(self.last_node())

    def remove_max(self):
        if len(self) == 0:
            return None
        self.swap_nodes(0, self.last_node())
        self.record()
        node = self._values.pop()
        self.record()
        self._sort_down(0)
        return node

    def heapify(self):
        n = len(self)//2 - 1
        for i in range(n, -1, -1):
            self._sort_down(i)

    # Heap Helpers

    def _sort_down(self, index):

        largest = index

        # If the left child is greater than the parent
        if self.has_left_child(index) and self.left_child(index) > self.value(largest):
            largest = left_index(index)
        # If the left child is greater than the the left child or parent
        if self.has_right_child(index) and self.right_child(index) > self.value(largest):
            largest = right_index(index)

        # If the parent is not the largest swap with the largest
        if largest != index:
            self.swap_nodes(index, largest)
            self.record()
            self._sort_down(largest)

    def _sort_up(self, start_index):
        index = start_index
        while (self.has_parent(index) and self.parent(index) < self.value(index)):
            self.swap_nodes(index, parent_index(index))
            self.record()
            index = parent_index(index)

    # Node Helpers
    def swap_nodes(self, index1, index2):
        self[index1], self[index2] = self[index2], self[index1]

    def has_left_child(self, index):
        return left_index(index) < len(self)

    def has_right_child(self, index):
        return right_index(index) < len(self)

    def has_parent(self, index):
        return parent_index(index) >= 0

    def left_child(self, index):
        return self[left_index(index)]

    def right_child(self, index):
        return self[right_index(index)]

    def parent(self, index):
        return self[parent_index(index)]

    def value(self, index):
        return self[index]
    
    def last_node(self):
        return len(self) - 1

    # Record Helpers

    def record(self):
        if self._record:
            self._history.append(copy.copy(self._values))

    def clear_history(self):
        self._history = []

    def history(self):
        return self._history

    # Dunders

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value):
        self._values[index] = value

    def __len__(self):
        return len(self._values)

    @property
    def array(self):
        return [*self._values]


def print_heap(array):
    NODE_WIDTH = 4
    NODE_PADDING = 2
    NODE_SPACING = 2

    row_width = 1
    item_counter = 0
    output_array = []
    row = []
    for node in array:
        row.append(node)
        item_counter += 1
        if item_counter == row_width:
            output_array.append(row)
            row = []
            item_counter = 0
            row_width *= 2
    output_array.append(row)

    max_nodes = 2 ** (len(output_array)-1)
    node_width = NODE_WIDTH + (2 * NODE_PADDING)
    screen_width = (node_width*max_nodes)
    
    for y, row in enumerate(output_array):
        cols = (2**y)
        col_width = screen_width // cols
        for x, node in enumerate(row):
            if y == 0:
                print(f"{node}".center(col_width), end='')
            else:
                print(f"{node}".center(col_width), end='')
        print()
    return output_array


if __name__ == '__main__':
    max_heap = MaxHeap([0], True)
    max_heap.heapify()
    
    history = max_heap.history()
    
    for iteration in history:
        print_heap(iteration)
        input('Enter to continue')
    
    
