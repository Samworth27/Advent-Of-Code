def sliding_window(iterable, window_size, window_func = lambda x: x, item_func = lambda x: x):
    for i in range(0,len(iterable),window_size):
        yield window_func([item_func(x) for x in iterable[i:i+window_size]])