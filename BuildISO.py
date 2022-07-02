import json
import urllib.request
import subprocess
with urllib.request.urlopen("https://github.com/Evernow/evernowmanjaro/raw/main/ISOConfig.json") as url:
    data = json.loads(url.read().decode())


subprocess.run('pacman -Syyu --no-confirm',shell=True)
subprocess.run('pacman -S manjaro-tools-iso git --no-confirm',shell=True)


subprocess.run('git clone https://gitlab.manjaro.org/profiles-and-settings/iso-profiles.git /iso-profiles')
def cleanuppackages():
    listofpackagefiles = ['Packages-Desktop', 'Packages-Live']
    for packagefile in listofpackagefiles:
        a_file = open('/iso-profiles/manjaro/kde/{packagefile}'.format(packagefile=packagefile), "r")
        lines = a_file.readlines()
        a_file.close()


        for x in lines:
            if any(ext in x for ext in data["PackagesToRemove"]):
                lines[x] = '\n#Removed\n'

        new_file = open('/iso-profiles/manjaro/kde/{packagefile}'.format(packagefile=packagefile), "w+")
        for line in lines:
            new_file.write(line)

        new_file.close()

def AddPackages():
    PackagesDesktop = open('/iso-profiles/manjaro/kde/Packages-Desktop', 'a')
    for package in data["PackagesToInstall"]:
        PackagesDesktop.write('\n{package}\n'.format(package=package))
    PackagesDesktop.close()


