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

### Output example

![P0002_18.png](samples/P0002_18.png) ![P0002_18.gif](samples/P0002_18.gif)  
P0002_18 - Artist: Unknown (Minbay?)

### TODO
 - [ ] Documenting the update file format
 - [ ] Documenting the BLE protocol
 - [X] Creating a sample tool to create animated an gif from a .dat file
 - [ ] Finish the pixb2img to crop image if wanted (it only shows imaged in their full 32x32 format)
 - [ ] Hardware documentation, there is definitely a serial port and other port on the board.
 - [ ] Maybe add datasheet of the components used on the board.
 - [ ] Find how they draw straigh lines and circle to have an exact match.

## Note
This repository is obviously not related in any way with MinBay the creators of the MB701.

For more information about the MB701 and MinBay go do their website: https://minbay.com

If you have any information missing in this repository, feel free to contact me, especially if you have firmware that 
I did not manage to save from their website and saved here.

## MB701 known bugs

 ### 1 - Pixel tool overflow

#### Explanation

Using the normal pixel drawing tool, drawing too many pixels in a single stroke can lead to at least two possible outcome
1. the artboard will crash and force you to power cycle it
2. the history will not work properly, and you will not be able to properly undo/redo the stroke.

#### Reason

Considering how is made the current version of the PTCR format, it can only store 255 pixel per stroke, so having more 
pixel than this number may generate a buffer overflow at some point, this need to be confirmed with the reverse 
engineering of the main software, but with really long stroke crash has been consistent.
Smaller but more than ~200 pixels stroke do lead to problem with the history.

Also considering that some history files provided with the artboard do have error in the pixel count on some long 
stroke, it is likely they also store this number with a non 8bit cap and the value do roll-over and create counting issues.

| Discoverd  | Affected firmware | Fixed on Version |
|------------|-------------------|------------------|
| 17/11/2022 | All known         | N/A              |

 ### 2 - Update not working properly with Mac OS

#### Explanation

Copying an update file to the MB701 from a Mac OS based system will not work, properly the file copy finish without any error
but the artboard will crash when it is ejected.
Doing the same thing from a windows system do not crash the board.

#### Reason

Unclear at the moment, but probably linked with the way show a FAT filesystem to the USB as I think it does not use a
native FAT internally.

| Discoverd  | Affected firmware | Fixed on Version |
|------------|-------------------|------------------|
| 01/11/2022 | All known         | N/A              |