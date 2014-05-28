
def _parser():
    '''Splits the HTTP messages into lines
    '''
    idx_g, idx = 0, 0
    cr_found = False
    data = yield
    
    while True:
        # CR was found in the previous chunk
        if cr_found and data[idx] == b'\n'[0]:
            yield idx_g + idx - 1
            cr_found = False

        # find cr
        cr = data.find(b'\r', idx)
        if cr >= 0:
            cr_found = True
            idx = cr + 1
        else:
            idx = len(data)

        # check if more data is needed
        if idx >= len(data):
            idx_g += len(data)
            idx = 0
            data = yield


def create_parser():
    '''Start an HTTP parser.

    Feed the parser by calling `.send`

    It yields:
       - `None` if it needs more data
       - an pinteger representing the index of the current chunk.

    Feed the parser *only* when he asks so: when he returns `None`
    
    Returns:
        a generator

    '''
    p = _parser()
    next(p)
    return p
