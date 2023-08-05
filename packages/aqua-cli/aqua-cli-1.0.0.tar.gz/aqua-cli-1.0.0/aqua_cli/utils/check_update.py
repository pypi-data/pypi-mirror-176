from aqua_cli import name, __version__
import requests

def check_update():
    url = 'https://api.github.com/repos/nyf9b/aqua-cli/releases/latest'
    latest_version = None

    try:
        latest_version = requests.get(url=url).json()['tag_name']

        if latest_version == __version__:
            print('No update available.')
            return

        print(f'A new release is available: v{latest_version}\nUpdate {name} with pip: pip install --upgrade aqua-cli')
    except:
        print('Couldn\'t check for updates. Are you connected to the Internet?')