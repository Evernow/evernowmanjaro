# Just simplifies building locally

import subprocess
try:
  subprocess.run('rm -r /evernowmanjaropack',shell=True)
except:
  Pass

subprocess.run('git clone https://github.com/Evernow/evernowmanjaro.git /evernowmanjaropack',shell=True,check=True)

subprocess.run('docker stop $(docker ps -a -q)',shell=True,check=True)

subprocess.run('docker rm $(docker ps -a -q)',shell=True,check=True)

subprocess.run('sudo cp /evernowmanjaropack/daemon.json /etc/docker/daemon.json',shell=True,check=True)

subprocess.run('sudo rm -rf /var/lib/docker',shell=True,check=True)

subprocess.run('sudo systemctl start docker',shell=True,check=True)

subprocess.run('docker create --name=new_container -it --cap-add=ALL --privileged manjarolinux/base:latest',shell=True,check=True)

subprocess.run('docker start new_container',shell=True,check=True)

subprocess.run('docker cp /evernowmanjaropack/ISO-Components new_container:/',shell=True,check=True)

subprocess.run('docker cp /evernowmanjaropack/BuildISO.py new_container:/',shell=True,check=True)

subprocess.run('docker exec --user root --privileged new_container python BuildISO.py',shell=True,check=True)

subprocess.run('mkdir /iso',shell=True)


subprocess.run('docker cp new_container:/var/vache/manjaro-tools /iso',shell=True,check=True)
