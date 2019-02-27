# Autoload
Autoload module for FreeCAD

![Screenshot](https://user-images.githubusercontent.com/4140247/27751514-adf7b748-5daa-11e7-9a02-98b34897b3b2.PNG)

Provides ability to load more workbenches on FreeCAD start. Such ability can be useful for workbench customization purposes and in combination with modules such as PieMenu, ShortCuts, CommandPanel ...

### Features
*  
*  
*  

### Installation
**Note:** Installation path for FreeCAD modules depends on the operating system:  

Linux:
`/home/user/.FreeCAD/Mod/Autoload/InitGui.py`

macOS:
`/Users/user_name/Library/Preferences/FreeCAD/Mod/Autoload/InitGui.py`

Windows:
`C:\Users\user_name\AppData\Roaming\FreeCAD\Mod\Autoload\InitGui.py`
##### Automatically via Addon Manager (Recommended)
As of FreeCAD v0.17.9944 the new Addon Manager has been merged. Install this addon by:   
- Opening **Tools** > **Addon Manager** 
- Locating **Autoload** and installing.  
- Relaunching FreeCAD.   

##### Manually install using git
Instructions for Ubuntu & Mint specifically but can be adapted to other distros. 
- Open the command prompt (terminal) with the keys **ctrl+alt+t**   
- Install git:  ***sudo apt-get install git***   
- Clone repository:  ***git clone https://github.com/triplus/Autoload ~/.FreeCAD/Mod/Autoload***   
- Relaunch FreeCAD (workbench should be incorporated automagically).  

##### Manually install via ZIP
- Download https://github.com/triplus/Autoload as a ZIP (click 'Clone or Download' button)   
- For Ubuntu, Mint and similar OS's, extract it inside */home/username/.FreeCAD/Mod*   
- For Windows, extract it inside *drive: \Users\your_user_name\AppData\Roaming\FreeCAD\Mod*   
Then  
- Relaunch FreeCAD (workbench should be incorporated automagically).
### Usage
Autoload preferences dialog can be accessed from the menu bar -> Accessories -> Autoload. Select workbenches that should be loaded on FreeCAD start.

### Documentation
  
### Feedback 
For bugs please open a ticket in the [issue queue](https://github.com/triplus/Autoload/issues). For discussion please use the [dedicated Autoload thread](https://forum.freecadweb.org/viewtopic.php?f=34&t=22976&p=180395#p178306) in the FreeCAD forums.

#### License 

#### Author
@triplus
