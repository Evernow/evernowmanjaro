sleNouveau_ok = ["NV", "GF", "C", "G8", "GT", "ION", "G9"] # Prematurely considering Fermi EOL.
NVIDIA_EOL = False
import subprocess
import time
time.sleep(3)
s = subprocess.check_output("inxi -G", shell=True).decode('utf-8')
def RunGood():
    subprocess.run("/home/manjaro/Desktop/Configs/ksetwallpaper.py /home/manjaro/Desktop/Configs/thumb-1920-1002134.png", shell=True)
for GPU in s:
    if "NVIDIA" in GPU:
        for EOL_Option in Nouveau_ok:
            if "NVIDIA " + EOL_Option in GPU:
                RunGood()
                NVIDIA_EOL = True
        if NVIDIA_EOL == False:
            if "loaded: nouveau" in GPU:
                print("BAD")
                subprocess.run("/home/manjaro/Desktop/Configs/ksetwallpaper.py /home/manjaro/Desktop/Configs/WrongDriverRee.png", shell=True)
            else:
                RunGood()
    else:
        RunGood()
try:
    #Turn off VSync...
    subprocess.run("nvidia-settings -a 'SyncToVBlank=0'", shell=True)
    subprocess.run("nvidia-settings -a 'SyncToVBlank=0'", shell=True)
except:
    pass
 