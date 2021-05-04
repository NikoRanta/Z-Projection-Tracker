# Z-Projection-Tracker

# Overview:  
  Input: 3D reconstructed image files (tif and tiff are supported)  
    
  Output: Two sets of 2D tif files, the maximum value for each xy column and the first z-slice for which that value was found.  Upon starting the process, a popup will prompt the user to select between saving the output as individual time slice tif files or one hyperstack tif.  
    
  Main Popup Window:   
    ![](Readme_Help_Images/Main_Popup_Appearence.PNG?raw=true "Main Window Appearence")  
  Dropdown shown:  
    ![](Readme_Help_Images/Main_Popup_Appearence_Dropdown.PNG?raw=true "Dropdown Menu")  
  Selection shown:
    ![](Readme_Help_Images/Main_Popup_Appearence_With_Selection.PNG?raw=true "Selection Made")  
  Output Format Prompt:  
  ![](Readme_Help_Images/Output_Format_Selection_Popup.PNG?raw=true "Specify Output Format Popup")


# Requirements:  
  64-bit operating system - this is crucial as 32-bit numpy is only able to hold ~500 z/t slices in a single array.
    
  Python (version 3.7+) - can be downloaded from python.org, choose an AMD64 (x86-64) architecture.
    
  Numpy (64-bit) - Can be downloaded from https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy, select the version which matches what you python version is installed (for example, python3.7 would download "numpy‑1.20.1+mkl‑cp37‑cp37m‑win_amd64.whl").  Next open cmd.exe and run "pip install pip --upgrade" to ensure that you are using the most recent version of pip.  Navigate to the directory (using 'cd [path_to_file]') where the numpy whl file was downloaded to and run 'pip install "numpy‑1.20.1+mkl‑cp37‑cp37m‑win_amd64.whl" ' (in the case of python3.7).  
  
  Download:  
  ![](Readme_Help_Images/64bit_Numpy_Download.PNG?raw=true "Download 64-Bit Numpy")  
  Install:  
  ![](Readme_Help_Images/Install_64bit_Numpy.PNG?raw=true "Install 64-Bit Numpy")  
    
  To verify, type python in cmd.exe and run "import numpy.distutils.sytem_info as sysinfo", "sysinfo.platform_bits" and ensure the printout is "64".  
  ![](Readme_Help_Images/Verify_64bit_Numpy.PNG?raw=true "Confirm 64-Bit Numpy")
    
  Skimage - install with 'pip install scikit-image'

# Operation:  
  ![](Readme_Help_Images/Run_Python_Script.PNG?raw=true "Initiate Python Script")  
  Open cmd.exe and navigate to where ClownBarf_Z_Projection_Finder.py is located, run 'python ClownBarf_Z_Projection_Finder.py'.  A popup should appear with 4 entry spots; an input directory, output directory, projection filename, and location filename.  Proper formating of the input reconstruction files is important.  The folder selected for the input directory should only contain folders that are named with numbers only (example, "0.000" or "2"), and the tif (or tiff) files inside each should also be numbers only.  
    
  Below are the expected print outputs in the command line for a given output format.  
    
  Hyperstack file:  
  ![](Readme_Help_Images/Readout_Hyperstack_File_Format.PNG?raw=true "Expected Hyperstack File Output")  
    
  Individual files:  
  ![](Readme_Help_Images/Readout_Individual_File_Format.PNG?raw=true "Expected Individual Files Output")  
  
# Troubleshooting:  
  All entries come prefilled with '(Required)', none of them can remain as such for the program to run.  Below are most of the errors that will appear should an entry be filled incorrectly.  
  
    
  The entries can be preset by editing the script text, instructions can be seen in the image below taken from the script.  
  ![](Readme_Help_Images/Pre_Set_Entries.PNG?raw=true "Edit Preset Entries")
  
# Possible input errors:  
  "Reconstruction Directory Is Not A Valid Directory" - The folderpath does not exist as typed, could be a typo or directing to a non-existent folder.  
  "Reconstruction Directory Does Not Contain Valid Folders" - Only folders with numbers are allowed, also no other files allowed.  If the folders are all named properly, check for a hidden file by navigating to the folder in cmd.exe and printing out the contents with "dir" in windows and "ls" in mac/linux.  
  "Reconstruction Directory Contains Invalid Files" - One or more files are present that are not a normal formatted file (format other than filename.extension).  
  "Reconstruction Directory Contains No Files" - No files found in the subfolders.  
  "Reconstruction Directory Contains Invalid File Names" - A file contains a non-numeric character, only numbers are allowed.  
  "Reconstruction Directory Contains Invalid File Types" - A non-tif or tiff file exists in the subfolders, only tif or tiff are allowed. 
