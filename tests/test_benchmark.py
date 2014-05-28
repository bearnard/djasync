import subprocess
import os
import time
import re


def do_benchmark(concurrency=10, number=100):
    client_out = subprocess.check_output(['ab',
                                          '-c', str(concurrency),
                                          '-n', str(number),
                                          'http://localhost:8000/'])
    return float(
        re.search(r'^Requests per second:[ ]*([0-9\.]+)', client_out.decode(),
                  re.MULTILINE).group(1))


def benchmark_runserver():
    '''Normal runserver.'''
    with subprocess.Popen(['python', 'manage.py', 'runserver', '-v', '0',
                           '--noreload'],
                          cwd=os.path.dirname(__file__),
                          stderr=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL) as proc:
        time.sleep(2)  # XXX
        out = do_benchmark()
        proc.kill()
    return out


def benchmark_djasync():
    '''DjAsync '''
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    wsgi_app = subprocess.check_output(
        ['python', '-c', 'from zootest import settings; print(settings.WSGI_APPLICATION)'],
        cwd=os.path.dirname(__file__)
    ).strip()
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([base_dir, os.path.dirname(__file__)])
    with subprocess.Popen(
            ['python', '-m', 'djasync.webserver', wsgi_app],
            cwd=base_dir,
            env=env) as proc:
        time.sleep(2)  # XXX
        out = do_benchmark()
        proc.kill()
    return out


def test_djasync_vs_runserver():
    assert benchmark_djasync() > benchmark_runserver()
