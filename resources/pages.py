
def paginate(l, page_size):
    for start in range(0, len(l), page_size):
        yield l[start:start + page_size]