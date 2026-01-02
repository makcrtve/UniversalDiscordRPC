import os
import psutil
from mutagen import File as MutagenFile

# List of media extensions to monitor
MEDIA_EXTENSIONS = ('.mp3', '.flac', '.wav', '.m4a', '.ogg', '.wma', '.aac', '.alac', '.opus')

def get_playing_file(pids):
    """ Finds a media file currently opened by the given process IDs. """
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            # Get open files and filter by media extensions
            for f in proc.open_files():
                if f.path.lower().endswith(MEDIA_EXTENSIONS):
                    return f.path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

def get_media_info(file_path):
    """ Extracts artist, title, and extension from a media file. """
    info = {
        'artist': None,
        'title': None,
        'file_ext': os.path.splitext(file_path)[1][1:].upper()
    }

    try:
        tag_file = MutagenFile(file_path)
        if tag_file:
            # Common tags across different formats
            if 'artist' in tag_file:
                info['artist'] = tag_file['artist'][0]
            elif 'TPE1' in tag_file: # ID3 artist
                info['artist'] = tag_file['TPE1'].text[0]

            if 'title' in tag_file:
                info['title'] = tag_file['title'][0]
            elif 'TIT2' in tag_file: # ID3 title
                info['title'] = tag_file['TIT2'].text[0]
    except Exception:
        pass # Ignore errors, return what we have

    return info
