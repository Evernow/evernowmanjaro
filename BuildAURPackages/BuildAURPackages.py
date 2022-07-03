import subprocess,shutil,glob,os

# {'Package name': ['Package location if AUR, if not then doesn't matter', 'command to launch']}

subprocess.run('exec 1>&2',shell=True) #https://stackoverflow.com/questions/58662065/docker-run-output-appears-out-of-order




packages_to_add = {
                    'mprime-bin': ['AUR', 'mprime'],
                    'gputest': ['AUR', None],
                    'basemark': ['AUR', None],
                    'nvflash': ['AUR', None],
                   'gwe': ['Chaotic AUR', None],
                    'corectrl': ['Chaotic AUR', None],
                    'python-getdevinfo': ['AUR', None], # Dependency of ddrescue-gui
                    'ddrescue-gui' : ['AUR','python3 /usr/share/ddrescue-gui/DDRescue_GUI.py']}

def buildAURPackages(AURPACKAGES):
    print(AURPACKAGES)
    os.makedirs('/AURPackagesToRepo')
    for package in AURPACKAGES:
        print("Handling this in AUR loop")
        print( package)
        subprocess.run('git clone https://aur.archlinux.org/{package}.git'.format(package=package),shell=True)
      #  
      # subprocess.run('chmod 777 /{package}'.format(package=package),shell=True)
      #  subprocess.run('sudo -u nobody ls',shell=True,cwd='/{package}'.format(package=package))
        subprocess.run('makepkg -si --syncdeps --cleanbuild  --noconfirm ',shell=True,cwd='/{package}'.format(package=package))
      #  subprocess.run('pacman -U {package} --noconfirm'.format(package=glob.glob('/{package}/*.zst'.format(package=package))[0]),shell=True)
        print('Command that is maybe failing here')
        shutil.copy(glob.glob('/{package}/*.zst'.format(package=package))[0], '/AURPackagesToRepo{nameofbuild}'.format(nameofbuild=glob.glob('/{package}/*.zst'.format(package=package))[0][glob.glob('/{package}/*.zst'.format(package=package))[0].rfind('/'):]))
    allfiles = os.listdir('/AURPackagesToRepo')
  
    for f in allfiles:
        shutil.move('/AURPackagesToRepo/' + f, '/online-repo/x86_64/' + f)
    subprocess.run('repo-add /online-repo/x86_64/online-repo.db *.pkg.tar.zst',shell=True,cwd='/{repoaddress}'.format(repoaddress='/online-repo/x86_64'))


def HandleAURdependenciesFromAUR(package):
    # Handles AUR packages which themselves depend on AUR packages, we need to build those too since makepkg won't grab those.

    # WIP, not currently finished since the need isn't there yet.
    subprocess.run('pacman -Slq community > communityrepo.txt',shell=True)
    subprocess.run('pacman -Slq extra > extrarepo.txt',shell=True)
    subprocess.run('pacman -Slq core > corerepo.txt',shell=True)
    subprocess.run('pacman -Slq multilib > multilibrepo.txt',shell=True)
    allpackages = [line.rstrip() for line in open('communityrepo.txt')] + [line.rstrip() for line in open('extrarepo.txt')] + [line.rstrip() for line in open('corerepo.txt')] + [line.rstrip() for line in open('multilibrepo.txt')] 

    os.makedirs('/throwaway')





def unbullshitifymakepkg():
    # Unfortunately due to this extremely bad practice of package developers trying to be our moms,
    # makepkg completely blocks use of itself when as root, which docker fucking runs under.
    # This hack essentially looks for the first 'fi' before the codeblock that checks for root,
    # then looks for the second 'fi' after it, and deletes everything in between.

    # Fuck. This. Shit. Whoever decided this can go fuck off to hell.
    List = open('/usr/bin/makepkg').readlines()

    #print(List)

    location_of_bullshit = None

    for line in List: 
        if 'Running %s as root is not allowed as it can cause permanent' in line:
            location_of_bullshit =  (List.index(line)-1)

    first_fi = None

    currentlocal = 0

    while currentlocal < location_of_bullshit:
            currentlocal += 1
            if 'fi' in List[currentlocal][0:2]:
                first_fi =  currentlocal + 1

    #print(first_fi)
    #print(location_of_bullshit)

    second_fi = None

    second_local = location_of_bullshit

    while True:
    #  print(List[second_local])
    #  print('fi' in List[second_local][0:3])
        if 'fi' in (List[second_local])[0:2]:
        # second_fi =  List.index(line)
            break
        else:
            second_local += 1
    second_local = second_local + 1
    #print(second_local)


    a_file = open('/usr/bin/makepkg', "r")
    lines = a_file.readlines()
    a_file.close()

    #print (range(first_fi,second_local))

    for x in list(range(first_fi,second_local)):
        lines[x] = '\n'

    new_file = open('/usr/bin/makepkg', "w+")
    for line in lines:
        new_file.write(line)

    new_file.close()

print('running the unbullshitifymakepkg')
unbullshitifymakepkg()
print('finished')

# Enable mulilib, easier to add the lines than uncomment them
pacmanconf = open('/etc/pacman.conf', 'a')
pacmanconf.write('\n[multilib]\nInclude = /etc/pacman.d/mirrorlist')
pacmanconf.close()

#Chaotic AUR has gwe and corectrl, two less packages to build is always a win
subprocess.run('pacman-key --recv-key FBA220DFC880C036 --keyserver keyserver.ubuntu.com',shell=True)
subprocess.run('pacman-key --lsign-key FBA220DFC880C036 ',shell=True)
subprocess.run("pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst' --noconfirm",shell=True)
subprocess.run('pacman-key --recv-key FBA220DFC880C036 --keyserver keyserver.ubuntu.com',shell=True)

pacmanconf = open('/etc/pacman.conf', 'a')
pacmanconf.write('\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist')
pacmanconf.close()






subprocess.run('sudo pacman -Syyu --noconfirm',shell=True)

subprocess.run('pacman -S manjaro-tools-iso manjaro-tools-base manjaro-tools-pkg git --noconfirm',shell=True)



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

os.makedirs('/online-repo/x86_64')
subprocess.run('chmod 777 {directory}'.format(directory='/online-repo'),shell=True)
subprocess.run('chmod 777 {directory}'.format(directory='/online-repo/x86_64'),shell=True)

import time
time.sleep(5)

buildAURPackages(AURPACKAGES)

print(os.listdir('/online-repo/x86_64'))

subprocess.run('chmod -R 777 {directory}'.format(directory='/online-repo/x86_64'),shell=True)
