from requests import get
from os import path
from time import monotonic
from sys import argv


def clear():
    print('\033[2J\x1b[2J\x1b[H')


def update_status(speed: float, pct_done: float, file_size: float, downloaded: float, file_name: str) -> None:
    print(f'{file_name}:')
    print(f'[{'=' * int(pct_done) + (100 - int(pct_done)) * ' '}] {round(pct_done, 2)}%\n')
    print(f'{round(speed / 1000, 2)} mbps')
    print(f'{round(downloaded / 1000000, 2)}/{round(file_size / 1000000, 2)} mb')


def download(url: str, file_name: str, resume: bool = False) -> bool:
    # amount of file downloaded variable
    downloaded = 0
    if not resume:
        request = get(url, stream=True, verify=False, allow_redirects=True)
    else:
        resume_header = {'Range': 'bytes=%d-' % path.getsize(file_name)}
        request = get(url, headers=resume_header, stream=True, verify=False, allow_redirects=True)

    # size of remote file
    file_size = int(request.headers['content-length'])
    start = last_print = monotonic()

    # Write file in chunks
    with open(file_name, 'ab') as d:
        for chunk in request.iter_content(chunk_size=4096):
            if chunk:
                downloaded += d.write(chunk)
                now = monotonic()

                # print speed stats
                if now - last_print > 1:

                    pct_done = round((downloaded / file_size) * 100, 2)

                    speed = round(downloaded / (now - start) / 1024)

                    clear()
                    update_status(speed, pct_done, file_size, downloaded, file_name)
                    last_print = now

    # assert that file was written to disk
    if downloaded == file_size:
        return True
    else:
        return False


try:
    query = argv[1]
    file = argv[2]
    try:
        resume_status = True if argv[3] == 'resume' else False
    except IndexError:
        resume_status = False
except IndexError:
    print('Syntax: [URL] [File Name]')
    exit(0)

# Gets url and file name
clear()


# Checks if file name has a dot
if file is None or file.find('.') == -1:
    print('File name must not be none and file name must have an extension.')
    exit(0)
if path.isfile(file):
    resume_status = True

try:
    assert download(query, file, resume_status) is True
    print('\nDownload Success!')
except AssertionError:
    print('\nDownload Failed!')
