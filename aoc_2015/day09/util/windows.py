def tumbling_window(iterable, window_size, window_func=lambda x: x, item_func=lambda x: x):
    for i in range(0, len(iterable), window_size):
        yield window_func([item_func(x) for x in iterable[i:i+window_size]])


def sliding_window(iterable, window_size, fixed=True, window_func=lambda x: x, item_func=lambda x: x):
    start = 0 if fixed == True else 0-window_size+1
    finish = len(iterable) - (window_size if fixed else 0)
    for i in range(start, finish + 1):
        yield window_func([item_func(x) for x in iterable[max(0, i):i+window_size]])
