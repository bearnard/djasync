from djasync.webserver import create_parser


def test_parser():
    p = create_parser()
    out = p.send(b'GET / HTTP 1.0\r\n')
    assert out == 14
    out = next(p)
    assert out is None
    out = p.send(b'Accept: text/html\r\n')
    assert out == 33
    out = next(p)
    assert out is None


def test_parser_2():
    p = create_parser()
    out = p.send(b'GET / HTTP')
    assert out is None
    out = p.send(b' 1.0\r\n')
    assert out == 14


def test_parser_3():
    p = create_parser()
    out = p.send(b'GET / HTTP 1.0\r')
    assert out is None
    out = p.send(b'\n')
    assert out == 14

