import os
import time
import json
import psutil
from pypresence import Presence
import ctypes
import sys
import subprocess
from datetime import datetime

# Win32 API setup for window title detection and singleton check
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

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

def get_window_title_from_pid(target_pid):
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    found_title = [None]

    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd) and user32.IsWindowEnabled(hwnd):
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value == target_pid:
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    found_title[0] = buffer.value
                    return False  # Stop enumeration
        return True

    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return found_title[0] if found_title[0] else "Unknown"

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
        log_debug("RPC Service Initialized.")

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

        # Single pass through all active processes
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info.get('name')
                if pname and pname.lower() in app_map:
                    return app_map[pname.lower()], proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None, None

    def run(self):
        log_debug("Universal Discord RPC is running in background...")
        while True:
            try:
                app, pid = self.find_target_process()

                if app:
                    client_id = app['client_id']
                    if self.current_app_id != client_id:
                        if self.active_rpc:
                            try: self.active_rpc.close()
                            except: pass

                        log_debug(f"Target found: {app['name']} (PID: {pid}). Connecting RPC...")

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

                    window_title = get_window_title_from_pid(pid)
                    details = app.get('details_format', '{window_title}').replace('{window_title}', window_title)
                    state = app.get('state_format', 'Running')
                    large_image = app.get('large_image')

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

if __name__ == "__main__":
    if is_already_running():
        sys.exit(0)

    if "--install" in sys.argv:
        add_to_startup()
        sys.exit(0)

    config_file = os.path.join(get_base_path(), 'config.json')
    rpc = UniversalRPC(config_file)
    rpc.run()
