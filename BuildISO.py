import json
import urllib.request
import subprocess,shutil,os
with urllib.request.urlopen("https://github.com/Evernow/evernowmanjaro/raw/main/ISOConfig.json") as url:
    data = json.loads(url.read().decode())


subprocess.run('pacman -Syyu --noconfirm',shell=True,check=True)
subprocess.run('pacman -S manjaro-tools-iso git --noconfirm',shell=True,check=True)


subprocess.run('git clone https://gitlab.manjaro.org/profiles-and-settings/iso-profiles.git /iso-profiles',shell=True,check=True)

def cleanuppackages():
    listofpackagefiles = ['Packages-Desktop', 'Packages-Live']
    for packagefile in listofpackagefiles:
        a_file = open('/iso-profiles/manjaro/kde/{packagefile}'.format(packagefile=packagefile), "r")
        lines = a_file.readlines()
        a_file.close()


        for x in lines:
            if any(ext in x for ext in data["PackagesToRemove"]):
                lines[lines.index(x)] = '\n#Removed\n'

        new_file = open('/iso-profiles/manjaro/kde/{packagefile}'.format(packagefile=packagefile), "w+")
        for line in lines:
            new_file.write(line)

        new_file.close()

def AddPackages():
    PackagesDesktop = open('/iso-profiles/manjaro/kde/Packages-Desktop', 'a')
    for package in data["PackagesToInstall"]:
        PackagesDesktop.write('\n{package}\n'.format(package=package))
    PackagesDesktop.close()


def SetupDesktop():
    localdesktop = '/ISO-Components/etc/Desktop/'
    files = os.listdir(localdesktop)
    if not os.path.exists('/iso-profiles/manjaro/kde/live-overlay/etc/skel/Desktop/'):
        os.makedirs('/iso-profiles/manjaro/kde/live-overlay/etc/skel/Desktop/')
    for f in files:
        shutil.move(localdesktop + f, '/iso-profiles/manjaro/kde/live-overlay/etc/skel/Desktop/' + f)


def Startup():
    # Does things like make Chika wallpaper and warnings
    localconfig = '/ISO-Components/etc/.config/'
    files = os.listdir(localconfig)
    if not os.path.exists('/iso-profiles/manjaro/kde/live-overlay/etc/skel/.config/'):
        os.makedirs('/iso-profiles/manjaro/kde/live-overlay/etc/skel/.config/')
    for f in files:
        shutil.move(localconfig + f, '/iso-profiles/manjaro/kde/live-overlay/etc/skel/.config/' + f)


cleanuppackages()
AddPackages()
SetupDesktop()
Startup()

subprocess.run('buildiso -f -p kde -b stable',shell=True,check=True)

