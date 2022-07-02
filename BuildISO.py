import json
import urllib.request
subprocess
with urllib.request.urlopen("https://github.com/Evernow/evernowmanjaro/raw/main/ISOConfig.json") as url:
    data = json.loads(url.read().decode())


subprocess.run('pacman -Syyu --no-confirm',shell=True)
subprocess.run('pacman -S manjaro-tools-iso git --no-confirm',shell=True)


subprocess.run('git clone https://gitlab.manjaro.org/profiles-and-settings/iso-profiles.git /iso-profiles')

