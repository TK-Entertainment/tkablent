import pytube, yt_dlp


ytdl_format_options = {
    'outtmpl': 'music/%(extractor_key)s/%(title)s-%(id)s-.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDL:
    def __init__(self):
        self.api_key: str = None

    def get_info(self, song, url):
        if ("http" not in url) and ("www" not in url):
            searchflag = True
            info = pytube.Search(url).results[0]
        else:
            searchflag = False
            info = pytube.YouTube(url)
        # the value below is for high audio quality
        setattr(song, 'title', info.title)
        setattr(song, 'author', info.author)
        setattr(song, 'channel_url', info.channel_url)
        setattr(song, 'watch_url', info.watch_url)
        setattr(song, 'thumbnail_url', info.thumbnail_url)
        setattr(song, 'length', info.length)
        if song.length != 0:
            infohd = info.streams.get_highest_resolution()
            setattr(song, 'url', infohd.url)
        else:
            if searchflag == True:
                url = info.watch_url
            streaminfo = ytdl.extract_info(url, download=False)
            setattr(song, 'url', streaminfo['url'])

        # Debugging Message
    #     if song.length != 0:
    #         print(f'''
    # Pytube Debug Info
    # Title: {song.title}
    # Author: {song.author}
    # Length: {song.length}sec
    # AudioCodec: {infohd.audio_codec}
    # Bitrate: {infohd.abr}
    #         ''')
    #     else:
    #         print(f'''
    # Pytube Debug Info
    # Title: {song.title}
    # Author: {song.author}
    # Length: It is a stream, how can you tell the length?
    # AudioCodec: Not availible
    # Bitrate: Not availible
    #         ''')