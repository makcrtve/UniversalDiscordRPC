import os
import psutil
from mutagen import File as MutagenFile

# List of media extensions to monitor
MEDIA_EXTENSIONS = ('.mp3', '.flac', '.wav', '.m4a', '.ogg', '.wma', '.aac', '.alac', '.opus')

# Cache for media file paths {pid: (path, last_title)}
_file_cache = {}

def get_playing_file(pids, current_window_title=""):
    """ Finds a media file currently opened by the given process IDs with track-aware caching. """
    if not pids:
        return None

    for pid in pids:
        # Check cache: Only reuse if title hasn't changed (simple heuristic for track change)
        if pid in _file_cache:
            path, last_title = _file_cache[pid]
            # If window title changed significantly, the file might have changed
            # We refresh if the current title doesn't contain the old one or vice-versa
            # Or simpler: if it's a media player, we just re-scan if the title changed at all
            if current_window_title == last_title and os.path.exists(path):
                return path

        try:
            proc = psutil.Process(pid)
            # Expensive call: we only do this when title changes or cache is empty
            for f in proc.open_files():
                if f.path.lower().endswith(MEDIA_EXTENSIONS):
                    _file_cache[pid] = (f.path, current_window_title)
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