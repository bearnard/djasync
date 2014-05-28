import subprocess


def do_benchmark(cmdline, concurrency=1, number=100):
    server = subprocess.Popen(cmdline)
    client = subprocess.check_output(['ab', 'http://localhost:8000', '-c',
                                      concurrency, '-n', number])
    print client_out


def test_runserver():
    '''Normal runserver.'''
    print 'ciao'
