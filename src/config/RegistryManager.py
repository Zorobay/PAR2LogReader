import winreg
from pathlib import Path

DEFAULT_FILE_PATH = 'DefaultFilePath'


class RegistryManager:

    def __init__(self):
        self.key_path = r'Software\PAR2LogReader'

    def get_default_file_path(self) -> Path | None:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
        try:
            value, _ = winreg.QueryValueEx(key, DEFAULT_FILE_PATH)
            return Path(value)
        except FileNotFoundError:
            return None

    def update_default_file_path(self, path: Path):
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
        try:
            winreg.SetValueEx(key, DEFAULT_FILE_PATH, 0, winreg.REG_SZ, str(path))
        except FileNotFoundError:
            raise Exception(f'Could not set value of key: {key}, string: {DEFAULT_FILE_PATH}')
