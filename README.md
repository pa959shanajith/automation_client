![Build Status](https://dev.azure.com/dimensionlabs/Nineteen68/_apis/build/status/Nineteen68?branchName=master)

# Avo Assure Version 2.0

## Technologies Used
* `Avo Assure Executor`
    * Python 3.7.0 - Entire Core Development
    * Plugin Development 
* `UX`
    * HTML5, AngularJS
* `Web Server and Backend`
    * Nodejs
    * ExpressJS
* `Database`
    * Mongo v4.2.0
    * Redis v3.2.1

### Core Development

### Package Changes for 32 bit support
* All the packages used in 64 bit to support Avo Assure have been installed in 32 bit setup.

* Following are the few packages that has been installed in 32 bit which are different in version used in 64 bit :
    * 64 bit packages
        * ftfy==4.4.2
        * lxml==3.6.4
        * requests==2.11.1
        * wxPython==3.0.2.0
        
    * 32 bit packages                                           
        * ftfy==4.4.3                                                  
        * lxml==3.6.0
        * requests==2.5.3
        * wxPython==4.0.0a2.dev3028+40a98da  

* Packages in 32bit that used to serve the same purpose in 64 bit:
    * Pillow==3.4.2 is used for PIL==1.1.7.
    * pypiwin32==219 is used for pywin32==220

