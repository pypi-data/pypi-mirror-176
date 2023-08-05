from platform import system
from getpass import getuser

def get_app_folder():
    folders = {
        'Windows': f'C:\\Users\\{getuser()}\\AppData\\Local\\aqua-cli\\',
        'Darwin': f'/Users/{getuser()}/Library/Application Support/aqua-cli/',
        'Linux': f'/home/{getuser()}/.local/share/aqua-cli/'
    }

    return folders[system()]