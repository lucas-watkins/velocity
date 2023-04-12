from requests import get; from os import system, path; from time import monotonic; from threading import Thread;

# method to clear console
def clear():
    system('cls')

# method to update download status
def update_status(speed, pct_done, file_size, downloaded):
    print('_____________________________')
    print("| \033[94mVelocity Download Manager\033[0m |")
    print('-----------------------------')
    print(f'Download is \033[92m{round(pct_done,2)}%\033[0m Done')
    print('-----------------------------')
    print(f'Download Rate is \033[92m{round(speed / 1000, 2)}\033[0m mbps')
    print('-----------------------------')
    print(f'Remote File is \033[92m{round(file_size / 1000000, 2)}\033[0m mb')
    print('-----------------------------')
    print(f'Downloaded \033[92m{round(downloaded / 1000000, 2)}\033[0m mb')
    print('-----------------------------')

# function to download normally
def download(url, file_name):
    # amount of file downloaded variable
    downloaded = 0

    download = get(url, stream=True, verify=False, allow_redirects=True)

    # size of remote file
    file_size = int(download.headers['content-length'])
    start = last_print = monotonic()
        # Write file in chunks 
    with open(file_name, 'wb') as d:
        for chunk in download.iter_content(chunk_size=4096):
            if chunk:
                downloaded += d.write(chunk)
                now = monotonic()

                # print speed stats
                if now - last_print > 1:
                   pct_done = round((downloaded / file_size) * 100, 2)

                   speed = round(downloaded / (now - start) / 1024)

                # restart download if speed is equal to zero
                   if speed == 0:
                       Thread(target = resume_download, args = (url, path.getsize(file_name), file_name)).start()
                       
                       # return statement to stop execution of method 
                       return
                   else:
                    clear()
                    update_status(speed, pct_done, file_size, downloaded)
                    last_print = now

# function to resume downloads
def resume_download(fileurl, resume_byte_pos, file_name):
    # amount of file downloaded variable
    downloaded = path.getsize(file_name)

    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    download = get(fileurl, headers=resume_header, stream=True,  verify=False, allow_redirects=True)
    
    start = last_print = monotonic()

    # size of remote file
    file_size = int(download.headers['content-length']) + downloaded
    
    # Append file in chunks
    with open(file_name, 'ab') as d:
        for chunk in download.iter_content(chunk_size=4096):
            if chunk:
               downloaded += d.write(chunk)
               now = monotonic()

                # print speed stats
               if now - last_print > 1:
                   pct_done = (downloaded / file_size) * 100

                   speed = round(downloaded / (now - start) / 1024)

                   # restart download if speed is equal to zero
                   if speed == 0:
                       Thread(target = resume_download, args = (url, path.getsize(file_name), file_name)).start()

                       # return statement to stop execution of method
                       return
                   else:
                    clear()
                    update_status(speed, pct_done, file_size, downloaded)
                    last_print = now

# Gets url and file name
clear()
print('Welcome To \033[94mVelocity Download Manager\033[0m')
print('------------------------------------\n')
url = input('Enter Url: ')
file_name = input('Enter File Name To Save As: ')

# Checks if file name has a dot
if file_name == None or file_name.find('.') == -1:
    print('\033[91mFile Name Must Not Be None and File Name must have a dot')
    exit(0)

# resume download if path exists
if path.exists(file_name):
    resume_download(url, path.getsize(file_name), file_name)
    
else:
    download(url, file_name)