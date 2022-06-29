import subprocess,shutil,glob,os

# {'Package name': ['Package location if AUR, if not then doesn't matter', 'command to launch']}
packages_to_add = {'ddrescue-gui' : ['AUR','python3 /usr/share/ddrescue-gui/DDRescue_GUI.py'],
                    'mprime-bin': ['AUR', 'mprime'],
                    'gputest': ['AUR', None],
                    'nvflash': ['AUR', None],
                    'python-getdevinfo': ['AUR', None]}

def buildAURPackages(AURPACKAGES):
    subprocess.run('sudo pacman -S makepkg --noconfirm',shell=True)
    subprocess.run('mkdir online-repo/x86_64',shell=True)
    os.makedirs('/AURPackagesToRepo')
    for package in AURPACKAGES:
        subprocess.run('git clone https://aur.archlinux.org/{package}.git'.format(package=package),shell=True)
        subprocess.run('chmod 777 /{package}'.format(package=package),shell=True)
        subprocess.run('sudo -u nobody makepkg --skipinteg --skipchecksums --skippgpcheck',shell=True,cwd='/{package}'.format(package=package))
        shutil.copy(glob.glob('/{package}/*.zst')[0].format(package=package), '/AURPackagesToRepo{nameofbuild}'.format(nameofbuild=glob.glob('/{package}/*.zst'.format(package=package))[0][glob.glob('/{package}/*.zst'.format(package=package))[0].rfind('/'):]))
    allfiles = os.listdir('/AURPackagesToRepo')
  
    for f in allfiles:
        shutil.move('/AURPackagesToRepo' + f, 'online-repo/x86_64' + f)
    subprocess.run('repo-add online-repo.db.tar.gz *.pkg.tar.*',cwd='/{repoaddress}'.format(repoaddress='online-repo/x86_64'))


subprocess.run('sudo pacman -Syyu --noconfirm',shell=True)

subprocess.run('pacman -S manjaro-tools-iso manjaro-tools-base manjaro-tools-pkg git --noconfirm',shell=True)

subprocess.run('git clone https://gitlab.manjaro.org/profiles-and-settings/iso-profiles.git iso-profiles', shell=True)


AURPACKAGES = []
for package in packages_to_add:
    if packages_to_add[package][0] == 'AUR':
        AURPACKAGES.append(package)
buildAURPackages(AURPACKAGES)