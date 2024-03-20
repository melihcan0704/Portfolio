import os
from pytube import Playlist
from moviepy.editor import *


def download_playlist(url, save_path):
    try:
        playlist = Playlist(url)
        print("Downloading playlist...")
        for video in playlist.videos:
            audio_stream = video.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download(output_path=save_path)
                print(f"Downloaded: {video.title}")
            else:
                print(f"No audio stream available for {video.title}")
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_to_mp3(source_path, target_path):
    try:
        for filename in os.listdir(source_path):
            if filename.endswith('.mp4'):
                audio_clip = AudioFileClip(os.path.join(source_path, filename))
                audio_clip.write_audiofile(os.path.join(target_path, filename[:-4] + ".mp3"))
                audio_clip.close()
                os.remove(os.path.join(source_path, filename))
    except Exception as e:
        print(f"An error occurred during conversion: {e}")


def main():
    print("Initializing download.")
    playlist_url = input("Enter the YouTube playlist URL: ")
    save_location = input("Enter the path to save the music files: ")

    
    if not os.path.exists(save_location):
        os.makedirs(save_location)

    download_playlist(playlist_url, save_location)
    convert_to_mp3(save_location, save_location)
    print("Download and conversion completed successfully!")


if __name__ == "__main__":
    main()
