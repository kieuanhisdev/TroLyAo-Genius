import yt_dlp
import vlc  
import time

def play_music_by_name(song_name):
    # Tìm kiếm video trên YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f'ytsearch1:{song_name}', download=False)

    if 'entries' in search_results:
        # Lấy thông tin của video đầu tiên trong kết quả tìm kiếm
        video_info = search_results['entries'][0]

        # Phát nhạc bằng VLC
        media = vlc.MediaPlayer(video_info['url'])
        media.play()

        # Chờ đến khi nhạc kết thúc
        duration = int(video_info['duration'])
        time.sleep(duration)

        # Trả về đối tượng MediaPlayer để có thể tắt nhạc từ file khác
        return media
    else:
        print("Không tìm thấy kết quả nào.")
        return None



def stop_music(media_player):
    if media_player:
        # Dừng nhạc
        media_player.stop()






