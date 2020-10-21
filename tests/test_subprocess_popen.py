import subprocess
import pexpect

ELLIPSE_PARAM = dict(
    _xc=626,
    _yc=381,
    _a=198,
    _b=40,
    _rad=3.141593,
    _score=0.67299813,
)


def exec_spawn(cmd):
    """Read subprocess output and yield each line ended with expect()
    https://stackoverflow.com/questions/20503671/python-c-program-subprocess-hangs-at-for-line-in-iter
    :param cmd: array of exec & params
    :return: yield process output line
    """
    i = 0
    child = pexpect.spawn(' '.join(cmd))
    print(f"exec_spawn command: {' '.join(cmd)}")
    while True:
        try:
            # 0 - '\n'; 1 - 'ms\$'
            i = child.expect(['\n', 'ms\$'])
        except:
            # two type exception EOF & TIMEOUT
            # in both cases will be done finally & close()
            break
        finally:
            # if i == 0:
            yield child.before

    child.close()


def execute(cmd):
    """RUN one-sub in subprocess with line by line output

    :param cmd: array of command and params
    :return:
    """
    print(f"Execute command: {' '.join(cmd)}")
    popen = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        universal_newlines=False,
        bufsize=1,  # unbuffered
    )
    for stdout_line in iter(popen.stdout.readline, b''):
        yield stdout_line

    popen.stdout.close()
    popen.kill()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == "__main__":
    """	
    -N image Name
    -D DataSet Name
    -S The threshold of ellipse score
    -R The threshold of Reliability
    -C The threshold of CenterDis
    -M The method id
    -P Working Directory
    """
    # command = ['ping', '-c', '4', 'localhost']
    # -N 027_0003.jpg  -S 0.85 -P . -M 9
    command = [
        'serverless/opencv/ellipse_detection/bin/ellipse_detector',
        '-N', '027_0003.jpg',
        '-S', '0.85',
        '-P', '.',
        '-M', '9'
    ]
    ell_keys = list(ELLIPSE_PARAM.keys())

    try:
        # for line in exec_spawn(command):
        ellipses = []
        for line in execute(command):
            ell = line.split(b"\t")
            if ell[0].decode('utf-8') == 'ellipse':
                ellipses.append(
                    # ' '.join([el.decode('utf-8').strip() for el in ell[1:]])
                    {ell_keys[key]: el.decode('utf-8').strip()
                     for key, el in enumerate(ell[1:])}
                )

        for ell in ellipses:
            print(ell)

    except KeyboardInterrupt as e:
        print(f'KeyboardInterrupt !................{e}')
