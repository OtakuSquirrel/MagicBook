# MagicBook


This is a useful tool which helps you create a full function book rig.


It is necessary to inform you that a ***numpy*** and ***scipy*** module is required!


After you download the .zip file from the release page, you can install the plug-in by following the steps below:


## How to install MagicBook


1. Decompression the files to your `MAYA_APP_DIR\modules`, for me (on Windows) it is:
```
C:\Users\Otaku\Documents\maya\modules
```
If you didn't find such a folder, create it by yourself!
Things should be like:
```
maya\modules\MagicBook
maya\modules\MagicBook.mod
maya\modules\dropToInstall.mel
```
  If you are using Maya on Macintosh or Linux, it should be:
```
~<userName>/Library/Preferences/Autodesk/Maya/modules
```
```
~<userName>/Maya/modules
```


2. ***Reopen*** Maya, then drag and drop the file `dropToInstall.mel` to Maya's viewport, you should see a yuumi on your shelf, installation is done.

## How to install numpy and scipy


For Windows user, press ```Win``` + ```R```, type in ```cmd```, press ```Enter```.


```cd``` to your Maya installation directory. If Maya is installed in ```D:\...```, type in ```D:```, then ```cd``` to where Maya locates.


Execute


```mayapy -m pip install numpy```


```mayapy -m pip install scipy```


