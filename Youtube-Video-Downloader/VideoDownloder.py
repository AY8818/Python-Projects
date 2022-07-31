from pytube import YouTube
from pytube import Playlist
import re
import os
import Graphics


def urlValidator(url):
    # print('\nValidating URL')
    re_exp = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
              "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
    exp = re.compile(re_exp)
    if url == 'Enter Link':
        return(0)  # return 0 coz its normal text
    if(re.search(exp, url)):
        return(1)  # return 1 coz url is valid
    else:
        return(-1)  # return -1 coz not a valid url


def SearchVideo(link):
    error_code = urlValidator(link)
    # print('URL Validation Complete')
    if error_code == 0:
        # print('Not a URL')
        return(0)
    elif error_code == -1:
        # print('Error in URL')
        return(-1)
    elif error_code == 1:
        try:
            # print('\nUrl Found')
            yt = YouTube(link)
            # print('Title: ', yt.title)
            return(yt.title)
        except:
            # print('\nUrl Not Found')
            return(-1)


previousprogress = 0


def on_progress(stream, chunk, bytes_remaining):
    # print('Inside on_progress')
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        # print(liveprogress)
        Graphics.progress_bar_status(liveprogress)


def prepareToDownload(link):
    # print('Inside prepareToDownload')
    if link == '':
        quit()
    else:
        yt = YouTube(link)
    return(yt)


def getdesktoppath():  # gives desktop path to download video at that location
    return os.path.join(os.path.expanduser("~"), "desktop")


def startDownloding(yt):
    # print('Inside startDownloding')
    ys = yt.streams.get_highest_resolution()
    # print('Downloding Going to start...')
    # print('\nDownloding Begins....')
    location = getdesktoppath()
    yt.register_on_progress_callback(on_progress)
    yt.streams.first().download(location)
    # print('Downloding Ends....')
    # print('\n*******Download Completed******')
    return('DC')
