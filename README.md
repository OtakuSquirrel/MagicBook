# MagicBook


## Tutorial


English
```
https://vimeo.com/manage/videos/915469397
```
```
https://youtu.be/_ABUKFHq3Kg
```

Chinese
```
https://www.bilibili.com/video/BV1ja4y127Fm/
```


This is a useful tool which helps you create a full function book rig.


It is necessary to inform you that a ***numpy*** and ***scipy*** module is required!

The plug-in is written in Python3 so please use Maya2020-py3 / Maya2022+.

I code and test it in Maya2023.


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
```
If you are using Maya on Macintosh or Linux, it should be:


Mac: `~<userName>/Library/Preferences/Autodesk/Maya/modules`


Linux: `~<userName>/Maya/modules`


2. ***Reopen*** Maya, then drag and drop the file `dropToInstall.mel` to Maya's viewport, you should see a yuumi on your shelf, installation is done.

## How to install numpy and scipy


The MagicBook plugin is developed with ***numpy1.26.3*** and ***scipy1.11.4***, but higher/latest version should work fine as well.


For Windows user, press `Win` + `R`, type in `cmd`, press `Enter`.


`cd` to your Maya installation directory. If Maya is installed in `D:\...`, type in `D:` first, then `cd` to where Maya locates.


Then `cd bin`


Generally, it is:


`D:`


`cd Program Files\Autodesk\Maya2023\bin`


Then execute:


```mayapy -m pip install numpy```


```mayapy -m pip install scipy```


