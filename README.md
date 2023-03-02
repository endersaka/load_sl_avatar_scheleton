# Second Life skeleton definition file loader script for Blender 3.4

This script loads the file `avatar_skeleton.xml`, also known as the **skeleton definition file** (see [Avatar Appearance - Linden skeleton definition file](https://wiki.secondlife.com/wiki/Avatar_Appearance#Linden_skeleton_definition_file)).

> **NOTE**: before to use it remember to modify the file path accordingly to the location of the file on your disk. Usually, on Windows, it is `C:\\Program Files\\SecondLifeViewer\\character\\avatar_skeleton.xml`. Double slashes are required in Python for Windows style paths.

## Usage

To use the script create a new Blender document (menu _File -> New -> General_), open a Text Editor view, _SHIFT F11_, open the script (menu _Text -> Open_ or keyboard combination _ALT O_) and lauch it with _ALT P_ (or menu _Text -> Run Script_).

It will open the skeleton definition file, parse it with Python module `xml.etree` (included in the Blender Python interpreter) and create the entire Bento skeleton hierarchy with all the skeleton extensions (both Fitted Mesh and Bento), bone groups and collision bones (also called collision volumes).

The script is not meant to load multiple skeletons.

Further features (like Blender add-on functionalities) will be added in the future. Hopefully: near future!
