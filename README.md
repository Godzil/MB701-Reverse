MB701 Reverse engineering effort
================================

This git repository include all the file related to the reverse engineering of the MinBay 
MB701 Pixel Art Board.

The goal is to document as much as possible the file format used by the Pixel Art Board, both 
the [.PIX](PIXB.md) and [.DAT](PTCR.md) file, reverse on them is near complete, there are 
still unknown part, but they are decipherable as is.

The second goal is to understand the update format and potentially allowing to use the board for 
executing your own code.

An effort to find how the Bluetooth is workind is also underway but too early to document it. Up so far 
all I can say is that it use BLE.

The [update_files](update_files) folder include all the known update file released by MinBay. 

The [sample_tools](sample_tools) folder include sample application in python handling the different 
type of file related to the MB701.

### Quick note about updating your MB701
About update, **DO NOT** try to update the MB701 using anything else than a PC under windows, and 
potentially linux. The way they handle FAT is weird and Mac OS seems to have issues with saving 
the update file properly leading the board to crash in weird way. 

### TODO
 - [ ] Documenting the update file format
 - [ ] Creating a sample tool to create animated an gif from a .dat file
 - [ ] Finish the the pixb2img to crop image if wanted (it only show imaged in their full 32x32 format)
 - [ ] Hardware documentation, there is definitely a serial port and other port on the board.
 - [ ] Maybe add datasheet of the components used on the board.

## Note
This repository is obviously not related in anyway with MinBay the creators of the MB701.

For more information about the MB701 and MinBay go do their website: https://minbay.com

If you have any information missing in this repository, feel free to contact me, especially if you have firmware that 
I did not manage to save from their website and saved here.