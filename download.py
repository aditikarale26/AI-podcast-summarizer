import yt_dlp

def download_audio(url, output_path="audio/podcast"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Downloaded audio to {output_path}.wav")
    return output_path + ".wav"

if __name__ == "__main__":
    url = input("Paste YouTube URL: ")
    download_audio(url)