import yt_dlp


class InstaDownloader(object):

    def __init__(self):
        pass

    def dl_video(self, code, output_path="downloader"):
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output template for downloaded file
            'format': 'bestvideo+bestaudio/best',  # Select the best quality
            'merge_output_format': 'mp4'  # Merge video and audio if separate
        }
        url = 'https://www.instagram.com/p/' + code + '/'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video
            ydl.download([url])
