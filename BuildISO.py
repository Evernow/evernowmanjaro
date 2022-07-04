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

pacmanconf = open('/etc/pacman.conf', 'a')
pacmanconf.write('\n[multilib]\nInclude = /etc/pacman.d/mirrorlist')
pacmanconf.close()


subprocess.run('pacman-key --recv-key FBA220DFC880C036 --keyserver keyserver.ubuntu.com',shell=True)
subprocess.run('pacman-key --lsign-key FBA220DFC880C036',shell=True)
subprocess.run("pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' --noconfirm",shell=True)
subprocess.run('pacman-key --recv-key FBA220DFC880C036 --keyserver keyserver.ubuntu.com',shell=True)

pacmanconf = open('/etc/pacman.conf', 'a')
pacmanconf.write('\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist')
pacmanconf.close()

pacmanconf = open('/etc/pacman.conf', 'a')
pacmanconf.write('\n[online-repo]\nSigLevel = Never\nServer = https://evernow.github.io/evernowmanjaro/online-repo/online-repo/x86_64')
pacmanconf.close()



pacmanconf = open('/iso-profiles/user-repos.conf', 'w+')
pacmanconf.write('\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist')
pacmanconf.close()

pacmanconf = open('/iso-profiles/user-repos.conf', 'a')
pacmanconf.write('\n[multilib]\nInclude = /etc/pacman.d/mirrorlist')
pacmanconf.close()





pacmanconf = open('/iso-profiles/user-repos.conf', 'a')
pacmanconf.write('\n[online-repo]\nSigLevel = Never\nServer = https://evernow.github.io/evernowmanjaro/online-repo/online-repo/x86_64')
pacmanconf.close()


# Pacman cannot handle git lfs files unfortunately, and from what I've read Pacman author is actively hostile about supporting anything Github specific, so in future will likely move this to Gitlab or ftp
subprocess.run('pacman -Syyu git-lfs --noconfirm',shell=True,check=True)

subprocess.run('git lfs install',shell=True,check=True)

subprocess.run('git-lfs clone https://github.com/Evernow/evernowmanjaro.git /evernowmanjaropack',shell=True,check=True)

subprocess.run('pacman -U /evernowmanjaropack/online-repo/online-repo/x86_64/*.pkg.tar.zst --noconfirm',shell=True,check=True)

cleanuppackages()
AddPackages()
SetupDesktop()
Startup()
subprocess.run('rm -r /usr/share/manjaro-tools/iso-profiles/',shell=True,check=True)
subprocess.run('mv iso-profiles/  /usr/share/manjaro-tools/',shell=True,check=True)

subprocess.run('buildiso -f -p kde -b stable -k {kernel}'.format(kernel=data["LinuxKernel"]),shell=True,check=True)

