#!/bin/sh
 
chmod +x ~/Desktop/Configs/phoronix-test-suite/download-cache/GravityMark_1.53.run
echo "y" | ~/Desktop/Configs/phoronix-test-suite/download-cache/GravityMark_1.53.run --quiet --target gravity-install --nox11 --noexec
 
echo "#!/bin/sh
cd gravity-install/bin
LD_LIBRARY_PATH=.:\$LD_LIBRARY_PATH ./GravityMark.x64 -vsync 0 -fps 1 -benchmark 1 -close 1 -fullscreen 1 -times 100 \$@ > \$LOG_FILE 2>&1" > gravitymark
chmod +x gravitymark
gravitymark 