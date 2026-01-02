import os
import time
import json
import psutil
from pypresence import Presence
import ctypes
import sys
import subprocess
from datetime import datetime
import threading
import pystray
from PIL import Image
import media_helper

# Win32 API setup for window title detection and singleton check
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(get_base_path(), relative_path)

def log_debug(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(get_base_path(), "debug.log")
    try:
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass
    print(message)

def is_already_running():
    # Simple singleton check using a named mutex
    # This prevents multiple instances from running at the same time
    mutex_name = "Global\\UniversalDiscordRPC_Mutex"
    kernel32.CreateMutexW(None, False, mutex_name)
    if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        return True
    return False

def get_window_title_from_pids(target_pids, fallback_title="Unknown"):
    """ Searches for a window title across a set of PIDs and their children. """
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    found_title = [None]

    # Expand the set of PIDs to include all children
    all_target_pids = set(target_pids)
    for tpid in target_pids:
        try:
            process = psutil.Process(tpid)
            for child in process.children(recursive=True):
                all_target_pids.add(child.pid)
        except:
            pass

    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value in all_target_pids:
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    title = buffer.value.strip()
                    # Skip common filler/generic titles
                    if title and title.lower() not in ["unknown", "default", "window", "overlay"]:
                        found_title[0] = title
                        return False # Stop enumeration
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)

    # If specifically "Unknown" or None, use the fallback_title
    if not found_title[0] or found_title[0].lower() == "unknown":
        return fallback_title

    return found_title[0]

def add_to_startup():
    if not getattr(sys, 'frozen', False):
        log_debug("Install only works with compiled .exe version.")
        return False

    exe_path = sys.executable
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_folder, "UniversalDiscordRPC.lnk")

    # Simple VB script to create a shortcut
    vbs_script = f'''
    Set WShShell = CreateObject("WScript.Shell")
    Set Shortcut = WShShell.CreateShortcut("{shortcut_path}")
    Shortcut.TargetPath = "{exe_path}"
    Shortcut.WorkingDirectory = "{os.path.dirname(exe_path)}"
    Shortcut.Save
    '''
    vbs_file = os.path.join(os.getenv('TEMP'), "create_shortcut.vbs")
    with open(vbs_file, 'w') as f:
        f.write(vbs_script)

    subprocess.call(['cscript', '//nologo', vbs_file])
    os.remove(vbs_file)
    log_debug(f"Successfully added to startup: {shortcut_path}")
    return True

class UniversalRPC:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()
        self.config_last_modified = os.path.getmtime(config_path) if os.path.exists(config_path) else 0
        self.active_rpc = None
        self.current_app_id = None
        self.start_time = None
        self.running = True

        # Sticky Presence logic
        self.last_detected_app = None
        self.last_detected_pids = None
        self.lost_focus_at = 0

        log_debug("RPC Service Initialized.")

    def stop(self):
        log_debug("Stopping RPC Service...")
        self.running = False
        if self.active_rpc:
            try:
                self.active_rpc.close()
            except:
                pass
            self.active_rpc = None

    def load_config(self):
        # Try primary path first
        paths_to_try = [self.config_path]

        # Fallback: if we are in a folder named 'dist', try the parent folder
        if "dist" in os.path.normpath(self.config_path).split(os.sep):
            parent_config = os.path.join(os.path.dirname(os.path.dirname(self.config_path)), 'config.json')
            paths_to_try.append(parent_config)

        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        config = json.load(f)
                        log_debug(f"Config loaded from: {path}")
                        self.config_path = path # Update to the found path
                        return config
                except Exception as e:
                    log_debug(f"Error reading {path}: {e}")

        log_debug(f"Error: No config.json found in {paths_to_try}")
        return {"polling_interval": 15, "apps": []}


    def check_config_reload(self):
        # Automatically reload config if file has changed
        if os.path.exists(self.config_path):
            mtime = os.path.getmtime(self.config_path)
            if mtime > self.config_last_modified:
                log_debug("Config file change detected! Reloading...")
                self.config = self.load_config()
                self.config_last_modified = mtime
                # Reset RPC to apply new settings if needed
                if self.active_rpc:
                    self.active_rpc.close()
                    self.active_rpc = None
                    self.current_app_id = None

    def find_target_process(self):
        self.check_config_reload()

        # Build a lookup map for faster matching
        app_map = {}
        for app in self.config.get('apps', []):
            target_names = app.get('process_name', [])
            if isinstance(target_names, str):
                target_names = [target_names]
            for name in target_names:
                app_map[name.lower()] = app

        # First pass: see if any target app is running
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info.get('name')
                if pname and pname.lower() in app_map:
                    target_app = app_map[pname.lower()]

                    # Collect ALL PIDs matching this app's process names
                    target_names = target_app.get('process_name', [])
                    if isinstance(target_names, str): target_names = [target_names]
                    target_names_lower = [n.lower() for n in target_names]

                    all_pids = []
                    for p in psutil.process_iter(['name']):
                        try:
                            if p.info['name'] and p.info['name'].lower() in target_names_lower:
                                all_pids.append(p.pid)
                        except: continue

                    if all_pids:
                        # NEW: Check if this app has at least one visible window (active in taskbar)
                        visibility_marker = "---HIDDEN---"
                        if get_window_title_from_pids(all_pids, visibility_marker) != visibility_marker:
                            return target_app, all_pids
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        # Second pass: Generic Fallback (if enabled)
        master = self.config.get('master_config', {})
        if master.get('enabled'):
            try:
                hwnd = user32.GetForegroundWindow()
                if hwnd:
                    pid = ctypes.c_ulong()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value:
                        proc = psutil.Process(pid.value)
                        pname = proc.name()

                        # Check exclusion list
                        exclusions = [e.lower() for e in master.get('exclude_processes', [])]
                        if pname.lower() not in exclusions:
                            # Dynamic image & format selection
                            image_map = master.get('image_map', {})
                            details_map = master.get('details_map', {})
                            state_map = master.get('state_map', {})

                            large_image = image_map.get(pname, image_map.get(pname.lower(), master.get('large_image')))
                            details_format = details_map.get(pname, details_map.get(pname.lower(), master.get('details_format', 'Working on: {app_name}')))
                            state_format = state_map.get(pname, state_map.get(pname.lower(), master.get('state_format', '{window_title}')))

                            # Create a virtual app entry
                            virtual_app = {
                                'name': pname.replace('.exe', '').capitalize(),
                                'client_id': master.get('client_id'),
                                'large_image': large_image,
                                'details_format': details_format,
                                'state_format': state_format,
                                'is_generic': True
                            }
                            return virtual_app, [pid.value]
            except Exception as e:
                # log_debug(f"Generic detection error: {e}")
                pass

        return None, None

    def run(self):
        log_debug("Universal Discord RPC is running in background...")
        while self.running:
            try:
                app, pids = self.find_target_process()

                # Smart Sticky logic:
                # If no app found (e.g., on Desktop/Explorer), keep the LAST app
                # UNTIL that app's window is closed or minimized to tray.
                if not app:
                    if self.active_rpc and self.last_detected_app and self.last_detected_pids:
                        visibility_marker = "---HIDDEN---"
                        if get_window_title_from_pids(self.last_detected_pids, visibility_marker) != visibility_marker:
                            app = self.last_detected_app
                            pids = self.last_detected_pids
                        else:
                            self.last_detected_app = None
                            self.last_detected_pids = None
                else:
                    self.last_detected_app = app
                    self.last_detected_pids = pids

                if app:
                    client_id = app['client_id']
                    if self.current_app_id != client_id:
                        if self.active_rpc:
                            try: self.active_rpc.close()
                            except: pass

                        log_debug(f"Target found: {app['name']}. Connecting RPC...")

                        discord_running = any(p.info['name'].lower() == "discord.exe" for p in psutil.process_iter(['name']))
                        if not discord_running:
                            log_debug("Discord is not running. Waiting...")
                            time.sleep(10)
                            continue

                        try:
                            self.active_rpc = Presence(client_id)
                            self.active_rpc.connect()
                            self.current_app_id = client_id
                            self.start_time = time.time()
                            log_debug(f"Connected to Discord for {app['name']}")
                        except Exception as e:
                            log_debug(f"Connection failed for {app['name']}: {e}")
                            time.sleep(10)
                            continue

                    window_title = get_window_title_from_pids(pids, fallback_title=app.get('name', 'Unknown App'))

                    # Prepare formatting variables
                    fmt_vars = {
                        'window_title': window_title,
                        'app_name': app.get('name', 'Unknown App'),
                        'process_name': psutil.Process(pids[0]).name() if pids and psutil.pid_exists(pids[0]) else 'Unknown',
                        'artist': '-',
                        'title': window_title,
                        'file_ext': '-'
                    }

                    # Media Metadata Support (No Upload)
                    # Search for media file metadata if this app is a media player
                    media_file = media_helper.get_playing_file(pids)
                    if media_file:
                        m_info = media_helper.get_media_info(media_file)
                        if m_info.get('artist'): fmt_vars['artist'] = m_info['artist']
                        if m_info.get('title'): fmt_vars['title'] = m_info['title']
                        if m_info.get('file_ext'): fmt_vars['file_ext'] = m_info['file_ext']

                    details = app.get('details_format', '{window_title}')
                    state = app.get('state_format', 'Running')
                    large_image = app.get('large_image')

                    # Safely format using our custom list of variables
                    for key, val in fmt_vars.items():
                        details = details.replace(f'{{{key}}}', str(val))
                        state = state.replace(f'{{{key}}}', str(val))

                    try:
                        self.active_rpc.update(
                            details=details[:128],
                            state=state[:128],
                            start=self.start_time,
                            large_image=large_image
                        )
                    except Exception as e:
                        log_debug(f"Update failed: {e}")
                        self.active_rpc = None
                        self.current_app_id = None
                else:
                    if self.active_rpc:
                        log_debug("Target software closed. Stopping RPC...")
                        try: self.active_rpc.close()
                        except: pass
                        self.active_rpc = None
                        self.current_app_id = None
                        self.start_time = None

            except Exception as e:
                log_debug(f"Main loop error: {e}")

            # Optimized polling: wait longer if no target app is running
            interval = self.config.get('polling_interval', 15)
            time.sleep(interval if self.current_app_id else interval * 2)

def on_quit(icon, item, rpc_obj):
    log_debug("Exit selected from tray.")
    rpc_obj.stop()
    icon.stop()

def setup_tray(rpc_obj):
    try:
        # Try to find icon in bundled resources first, then locally
        icon_path = get_resource_path("icon.ico")

        if not os.path.exists(icon_path):
            # Fallback to local path if not in bundle
            icon_path = os.path.join(get_base_path(), "icon.ico")

        log_debug(f"Loading tray icon from: {icon_path}")
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
        else:
            log_debug("Icon not found, using fallback colored square.")
            image = Image.new('RGB', (64, 64), color=(114, 137, 218))

        menu = pystray.Menu(
            pystray.MenuItem("Universal Discord RPC", lambda: None, enabled=False),
            pystray.MenuItem("Exit", lambda icon, item: on_quit(icon, item, rpc_obj))
        )

        icon = pystray.Icon("UniversalDiscordRPC", image, "Universal Discord RPC", menu)
        icon.run()
    except Exception as e:
        log_debug(f"Tray initialization error: {e}")
        # If tray fails, we still want the RPC to run if possible,
        # but since this is the main thread, it might exit anyway.
        # We'll just keep the main thread alive if we can.
        while rpc_obj.running:
            time.sleep(1)

if __name__ == "__main__":
    if is_already_running():
        sys.exit(0)

    if "--install" in sys.argv:
        add_to_startup()
        sys.exit(0)

    config_file = os.path.join(get_base_path(), 'config.json')
    rpc = UniversalRPC(config_file)

    # Run RPC logic in a separate thread
    rpc_thread = threading.Thread(target=rpc.run, daemon=True)
    rpc_thread.start()

    # Run tray icon in the main thread (pystray needs to be in the main thread on some platforms)
    setup_tray(rpc)