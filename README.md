# Custom Manjaro ISO for troubleshooting hardware issues

## Goal

This custom build Manjaro ISO aims to be make it easier for a user to be able to determine if an issue is hardware or software based by making it as simple as possible to test it in Manjaro.

## Benefits

Main benefits to this is that a user will not need to interact with the command line to install these tools, nor will they require an internet connection past downloading the ISO (which can be troublesome if a user does not have access to an ethernet connection and has an unsupported wifi card) 

## Drawbacks

1. This ISO is much bigger than the original, size is yet to be detemrined.
2. This ISO is not an easy maintainance task, and adds additional hurdles, due to this all modifications will be minimal, no changes to how Manjaro behaves will be made.


## Modifications

### Added

1. Unigine-Valley*
2. Furmark*
3. GPU Monitoring tools (GWE* for Nvidia, RadeonTop for AMD)
4. Kernel Panic monitoring
5. Prime95*
6. Nvidia LTS drivers for the 390 series. 
7. Discord
8. Nvidia Optimus packages 
9. xdotool

*These packages are maintained by me here to be able to control what they do and how they do it. Sources for them is in the repository.

### Removed
This is removed as an effort to reduce the size of the ISO.

1. VLC
2. qBittorrent
3. Printer drivers
4. Office
5. Steam
6. Snaps
7. HPLIP
8. Wallpapers
9. Extra themes
10. TimeShift
11. Java
12. DVD/CD reading/burning packages.

## Optimus notes

I do not have an Optimus laptop to test this with. 

You can run `glxinfo | grep "server glx vendor string"`. If you see 
`SGI`, you are running on the Intel GPU. If you see `NVIDIA 
Corporation`, you are running on the Nvidia GPU.

## To do list

- [x] Add .desktop files on the desktop to make it easier for a person to initiate stress tests
- [ ] Find a way to add the Phoronix Test Suite (main issue is for offline use, and the fact we can't have this image be bigger than 4gb due to ram limitations)
- [ ] Find an additional good GPU stress test 
- [ ] Add more Wifi drivers
- [ ] Look into viability of switching to the Minimal ISO style of Manjaro

## Reproducability

All pkgbuild files and iso-profiles files will be provided in this repo. 

ISO itself will not be provided here due to bandwidth limitations on this hosted repo, ISO downloads will be provided through Google Drive.

## Credits

Manjaro for providing documentation on how to make your own ISO: https://wiki.manjaro.org/index.php/Build_Manjaro_ISOs_with_buildiso

Disconnected Systems for providing a guide on how to host a Manjaro repo on GitHub: https://disconnected.systems/blog/archlinux-repo-in-a-git-repo/

