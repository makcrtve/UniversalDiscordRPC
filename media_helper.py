import os
import psutil
from mutagen import File as MutagenFile

# List of media extensions to monitor
MEDIA_EXTENSIONS = ('.mp3', '.flac', '.wav', '.m4a', '.ogg', '.wma', '.aac', '.alac', '.opus')

# Cache for media file paths {pid: (path, last_title)}
_file_cache = {}  # {pid: (path, last_title, file_size, mtime)}

def get_playing_file(pids, current_window_title=""):
    if not pids:
        return None
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            for f in proc.open_files():
                if f.path.lower().endswith(MEDIA_EXTENSIONS):
                    # Hitung key unik
                    st = os.stat(f.path)
                    cache_key = (pid, current_window_title, st.st_size, int(st.st_mtime))
                    cached = _file_cache.get(pid)
                    if cached and cached[:4] == cache_key:
                        return cached[4]  # return path
                    # Update cache
                    _file_cache[pid] = cache_key + (f.path,)
                    return f.path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            _file_cache.pop(pid, None)
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