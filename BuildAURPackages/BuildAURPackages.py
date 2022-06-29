import subprocess,shutil,glob,os

# {'Package name': ['Package location if AUR, if not then doesn't matter', 'command to launch']}
packages_to_add = {
                    'mprime-bin': ['AUR', 'mprime'],
                    'gputest': ['AUR', None],
                    'nvflash': ['AUR', None],
                    'ddrescue' : ['extra', None], # Dependency of ddrescue-gui
                    'lshw' : ['extra', None], # Dependency of ddrescue-gui
                    'python-beautifulsoup4' : ['extra', None], # Dependency of ddrescue-gui
                    'parted' : ['extra', None], # Dependency of ddrescue-gui
                    'python-getdevinfo': ['AUR', None], # Dependency of ddrescue-gui
                    'python-wxpython': ['AUR', None], # Dependency of ddrescue-gui
                    'ddrescue-gui' : ['AUR','python3 /usr/share/ddrescue-gui/DDRescue_GUI.py']}

def buildAURPackages(AURPACKAGES):
    print(AURPACKAGES)
    subprocess.run('sudo pacman -S makepkg --noconfirm',shell=True)
    subprocess.run('mkdir online-repo',shell=True)
    subprocess.run('mkdir online-repo/x86_64',shell=True)
    os.makedirs('/AURPackagesToRepo')
    for package in AURPACKAGES:
        print("Handling this in AUR loop")
        print( package)
        subprocess.run('git clone https://aur.archlinux.org/{package}.git'.format(package=package),shell=True)
        subprocess.run('chmod 777 /{package}'.format(package=package),shell=True)
        subprocess.run('sudo -u nobody ls',shell=True,cwd='/{package}'.format(package=package))
        subprocess.run('sudo -u nobody makepkg -i --skipinteg --skipchecksums --skippgpcheck',shell=True,cwd='/{package}'.format(package=package))
        shutil.copy(glob.glob('/{package}/*.zst')[0].format(package=package), '/AURPackagesToRepo{nameofbuild}'.format(nameofbuild=glob.glob('/{package}/*.zst'.format(package=package))[0][glob.glob('/{package}/*.zst'.format(package=package))[0].rfind('/'):]))
    allfiles = os.listdir('/AURPackagesToRepo')
  
    for f in allfiles:
        shutil.move('/AURPackagesToRepo' + f, 'online-repo/x86_64' + f)
    subprocess.run('repo-add online-repo.db.tar.gz *.pkg.tar.*',cwd='/{repoaddress}'.format(repoaddress='online-repo/x86_64'))


subprocess.run('sudo pacman -Syyu --noconfirm',shell=True)

subprocess.run('pacman -S manjaro-tools-iso manjaro-tools-base manjaro-tools-pkg git --noconfirm',shell=True)
subprocess.run('mkdir iso-profiles',shell=True)
subprocess.run('git clone https://gitlab.manjaro.org/profiles-and-settings/iso-profiles.git iso-profiles', shell=True)


AURPACKAGES = []
repopackages = []
for package in packages_to_add:
    if packages_to_add[package][0] == 'AUR':
        AURPACKAGES.append(package)
    else:
        repopackages.append(package)
print(" Packages")
print(AURPACKAGES)
print("AUR Packages")
print(repopackages)

for package in repopackages:
    subprocess.run('pacman -S {package} --noconfirm'.format(package=package),shell=True)
buildAURPackages(AURPACKAGES)