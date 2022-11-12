MB701 Reverse engeneeering effort
=================================

This git repository include all the file related to the reverse engineering of the MinBay MB701 Pixel Art Board.

The goal is to document as much as possible the file format used by the Pixel Art Board, both the [.PIX](PIXB.md) and [.DAT](PTCR.md) file, reverse on them is near complte, there are still unknown part but they are decypherable as is.

The second goal is to understand the update format and potentially allowing to use the board for executing your own code.

An effort to find how the Bluetooth is workind is also underway but too early to document it. Up so far all I can say is that it use BLE.


The [update_file](update_file) folder include all the known update file released by MinBay. 

### Note about update
About update, **DO NOT** try to update the MB701 using anything else than a PC under windows, and potentially linux. The way they handle FAT is weird and Mac OS seems to have issues with saving the update file properly leading the board to crash in weird way. 