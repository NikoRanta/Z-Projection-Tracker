import os
from os import listdir
from os.path import isfile,join,isdir
import numpy as np
from skimage import io
import timeit
from tkinter import *
from tkinter import filedialog
import platform


def Order_Holograms_After_Reconstruction(folderPath):
    '''
        Organizes the reconstruction folders into an array that can be called.  The first axis is z-slices and the second axis is the time points. [z,t]
    '''
    
    #Finds folder names
    Folder_Names = np.array([(f,float(f.name)) for f in os.scandir(folderPath)])
    #Orders folder names
    Ascending_Order = Folder_Names[Folder_Names[:,1].argsort()]
    #Creates 2D array to place file path in first column and folder numeric value in second column
    folder_names_combined = np.zeros((len(Ascending_Order),len(listdir(Ascending_Order[0,0].path)))).astype(np.unicode_)
    
    for z_slice in range(len(Ascending_Order)):
        #Finds file names of each time point for 
        File_Names = [File_Names for File_Names in listdir(Ascending_Order[z_slice,0].path) if isfile(join(Ascending_Order[z_slice,0],File_Names))]
        #Splits apart the folder names ('-10.000' becomes ['-10','000'] )
        z_slice_time_stamp_names = np.array([File_Names[time_point].split('.') for time_point in range(len(File_Names))])
        #Puts the folder names in ascending numberic order
        folder_names_combined[z_slice] = np.array([z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][t_slice][0]+'.'+z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][t_slice][1] for t_slice in range(len(File_Names))])
        
    #Create a list of all file paths and folder names
    Organized_Files = []
    for x in range(len(folder_names_combined[:,0])):
        for y in range(len(folder_names_combined[0,:])):
            Organized_Files.append(Ascending_Order[x,0].path+'/'+str(folder_names_combined[x,y]))
    
    #Converts the Organized_Files list into an array that is reshaped from a 1D array into a 2D array with rows equal to the number of z-slices and columns equal to the number of time points
    Organized_Files = np.array(Organized_Files).reshape((len(folder_names_combined[:,0]),len(folder_names_combined[0,:])))
    
    return Organized_Files,Ascending_Order

def Error_Checking():
    '''
        Determine if there are any errors in the entries that would not allow the program to run to completion with the input folder, folder output, and file names selected.
        
        Errors_Found have 4 errors to check for:
            0 - The input folder exists, there are only properly named subfolders in this folder, all files in the subfolders are properly named and tif or tiff files.
            1 - The output folder exists
            2 - Z Projection name is valid
            3 - Z Location name is valid
        
        If all of these checks pass, then the Error_Count will return a 0.
    '''
    Errors_Found = np.zeros(5)
    '''
        All error symbols are drawn to allow the program to properly remove them should the error be fixed.  Without creating them, a tkinter variable error occurs.
    '''
    Overall_Error_Message_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Overal_Error_Spacing.get(),window=Overall_Error_Message)
    Input_Error_Label_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Input_Spacing.get(),window=Input_Error_Label)
    Output_Error_Label_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Output_Spacing.get(),window=Output_Error_Label)
    Z_Value_Error_Label_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Value_Error_Label)
    Z_Loc_Error_Label_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Z_Loc_Spacing.get(),window=Z_Loc_Error_Label)
    Input_Folder_Error_Canvas = canvas.create_window(Input_Output_Error_Horizontal.get(),Z_Value_Error_Spacing.get(),window=Input_Folder_Error)
    Input_Subfolder_Error_Canvas = canvas.create_window(Input_Output_Error_Horizontal.get(),Z_Value_Error_Spacing.get(),window=Input_Subfolder_Error)
    Input_Reconstruction_Files_Error_Canvas = canvas.create_window(Input_Output_Error_Horizontal.get(),Z_Value_Error_Spacing.get(),window=Input_Reconstruction_Files_Error)
    Output_Directory_Folder_Error_Canvas = canvas.create_window(Input_Output_Error_Horizontal.get(),Z_Loc_Error_Spacing.get(),window=Output_Directory_Folder_Error)
    Z_Value_Filename_Error_Canvas = canvas.create_window(Output_Filenames_Horizontal.get(),Z_Value_Error_Spacing.get(),window=Z_Value_Filename_Error)
    Z_Loc_Filename_Error_Canvas = canvas.create_window(Output_Filenames_Horizontal.get(),Z_Loc_Error_Spacing.get(),window=Z_Loc_Filename_Error)
    Projection_Output_Method_Error_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Pipeline_Menu_Spacing.get(),window=Projection_Output_Method_Error)
    Projection_Output_Method_Error_Message_Canvas = canvas.create_window(Output_Filenames_Horizontal.get(),Pipeline_Menu_Spacing.get(),window=Projection_Output_Method_Error_Message)
    
    #Error symbol moves if Z Location is the selected method
    if Pipeline_Method_Selection.get() == 'Z Location Value':
        Z_Loc_Error_Label_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Loc_Error_Label)
    
    
    '''
        Check if reconstructions in the input folder selected are formatted properly
        
        Proper format for reconstruction folder:
            Main folder:
                Any valid name
                Must contain only sub-folders with names that are numbers such as -20.000 or 0.000 that correspond to the z-slices created during the reconstruction
                Beware of hidden folders/files, will return a result in "Reconstruction directory does not contain valid Folders"
                    To check if this is the cause:
                        1)Open command prompt and change the directory to the folder being selected. (typically cd [folder address])
                        2)Print all directories with:
                            2a) Windows: "dir"
                            2b) Mac/Linux: "ls" (this is a lower case L)
                        3)If anything other than the expected folders appear on the list, this is the cause.  Otherwise check inside sub-folders
            
            Sub-folders:
                Name can only be a number with two sections separated by a period that correspond to the z-slices that were reconstructed.  Example folder names are "10.000", "10.250", "-20.000", and "0.000"
            
            Image files:
                Only tif/tiff files allowed inside of the sub-folders
                Name must be an integer that corresponds to the time point where it was reconstructed from
                Can't be placed outside of the sub-folders
    '''
    if not isdir(Input_Directory_Text.get()):
        Errors_Found[0] = 1
        Input_Folder_Error_Check.set(1)
    if isdir(Input_Directory_Text.get()):
        Input_Folder_Error_Check.set(0)
        
    if Input_Folder_Error_Check.get() == 0:
        try:
            Folder_Names = np.array([(f,float(f.name)) for f in os.scandir(Input_Directory_Text.get())])
        except ValueError:
            Errors_Found[0] = 1
            Input_Subfolder_Error_Check.set(1)
        else:
            if len(Folder_Names) == 0:
                Errors_Found[0] = 1
                Input_Subfolder_Error_Check.set(1)
            if len(Folder_Names) > 0:
                Descending_Order = Folder_Names[(-Folder_Names[:,1]).argsort()]
                Input_Subfolder_Error_Check.set(0)
        if Input_Subfolder_Error_Check.get() == 0: 
            Folder_Names = np.array([(f,float(f.name)) for f in os.scandir(Input_Directory_Text.get())])
            Descending_Order = Folder_Names[(-Folder_Names[:,1]).argsort()]
            for folders in range(len(Descending_Order)):
                try:
                    [[File_Names.split('.')[0],File_Names.split('.')[1]] for File_Names in listdir(Descending_Order[folders,0].path) if isfile(join(Descending_Order[folders,0],File_Names))]
                except:
                    Input_Reconstruction_Files_Error_Check.set(1)
                else:
                    File_Names = [[File_Names.split('.')[0],File_Names.split('.')[1]] for File_Names in listdir(Descending_Order[folders,0].path) if isfile(join(Descending_Order[folders,0],File_Names))]
                    if len(File_Names) == 0:
                        Input_Reconstruction_Files_Error_Check.set(1)
                    if len(File_Names)>0:
                        filename_check = np.zeros(len(File_Names))
                        filetype_check = np.zeros(len(File_Names)).astype(np.unicode_)
                        issues_found = 0
                        for x in range(len(File_Names)):
                            proceed = 0
                            try:
                                filename_check[x] = File_Names[x][0]
                            except ValueError:
                                issues_found = 1
                                Input_Reconstruction_Files_Error_Check.set(1)
                                break
                            if File_Names[x][1] != 'tif' and File_Names[x][1] != 'tiff':
                                issues_found = 1
                                Input_Reconstruction_Files_Error_Check.set(1)
                                break
                        if issues_found==1:
                            Errors_Found[0] = 1
                            Input_Reconstruction_Files_Error_Check.set(1)
                            break
            if issues_found == 0:     
                Input_Reconstruction_Files_Error_Check.set(0)
               
    if Input_Folder_Error_Check.get() == 0:
        canvas.delete(Input_Folder_Error_Canvas)
    if Input_Subfolder_Error_Check.get() == 0:
        canvas.delete(Input_Subfolder_Error_Canvas)
    if Input_Reconstruction_Files_Error_Check.get() == 0:
        canvas.delete(Input_Reconstruction_Files_Error_Canvas)
    if Input_Folder_Error_Check.get() == 0 and Input_Subfolder_Error_Check.get() == 0 and Input_Reconstruction_Files_Error_Check.get() == 0:
        canvas.delete(Input_Error_Label_Canvas)
    
    '''
        Check if the output directory exists
    '''
    if not isdir(Output_Directory_Text.get()):
        Errors_Found[1] = 1
    if isdir(Output_Directory_Text.get()):
        canvas.delete(Output_Error_Label_Canvas)
        canvas.delete(Output_Directory_Folder_Error_Canvas)
    '''
        Check that Z Projection filename is valid
    '''
    if Z_Project_Value_Name.get() == '(Required)' and (Pipeline_Method_Selection.get() == 'Z Projection Value' or Pipeline_Method_Selection.get() == 'Both'):
        Errors_Found[2] = 1
    try:
        with open(Output_Directory_Text.get()+Z_Project_Value_Name.get()+'.tif','w') as file:
            pass
    except:
        Errors_Found[2] = 1
    else:
        os.remove(Output_Directory_Text.get()+Z_Project_Value_Name.get()+'.tif')
        
    '''
        Check that Z Location filename is valid
    '''
    if Z_Project_Loc_Name.get() == '(Required)' and (Pipeline_Method_Selection.get() == 'Z Location Value' or Pipeline_Method_Selection.get() == 'Both'):
        Errors_Found[3] = 1
    try:
        with open(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif','w') as file:
            pass
    except:
        Errors_Found[3] = 1
    else:
        os.remove(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif')
        
    if Pipeline_Method_Selection.get() == 'Select One':
        Errors_Found[4] = 1
    
    '''
        Count the number of errors
    '''
    Error_Count = np.count_nonzero(Errors_Found!=0)
    
    '''
        Delete the error messages that are not needed.
    '''
       
    if Errors_Found[0] == 0:
        canvas.delete(Input_Error_Label_Canvas)
    if Errors_Found[1] == 0:
        canvas.delete(Output_Error_Label_Canvas)
    if Errors_Found[2] == 0:
        canvas.delete(Z_Value_Error_Label_Canvas)
        canvas.delete(Z_Value_Filename_Error_Canvas)
    if Errors_Found[3] == 0:
        canvas.delete(Z_Loc_Error_Label_Canvas)
        canvas.delete(Z_Loc_Filename_Error_Canvas)
    if Errors_Found[4] == 0:
        canvas.delete(Projection_Output_Method_Error_Canvas)
        canvas.delete(Projection_Output_Method_Error_Message_Canvas)
    
    
    if Error_Count == 0:
        canvas.delete(Overall_Error_Message_Canvas)
        GUI.update()
        Save_Option_Window()

def Z_Projection():
    '''
        start - The starting point for reporting how long the processes have taken
        Reconstruction_Files - The files that have their paths denoted and are sorted by increasing value of Z
        Z_Slice_Values[1] - The z slice values, used for locating which slice the max value came from
        Z_Proj_Loc - An array of the z slice where the maximum value is for each (x,y) column
        
        Reconstruction files are first organized and processed one time point at a time.  The z-stack is built 
        for the current time point and depending upon the method chosen either the max value, location of max value,
        or both are saved in a 2D array.
    '''
    start = timeit.default_timer()
    
    #Compiles the folderpath and z-slice values for the reconstruction folder given into an array with the format of [z,t]
    Reconstruction_Files,Z_Slice_Values = Order_Holograms_After_Reconstruction(Input_Directory_Text.get())
    
    #Load first tif to get size of image
    Shape_Finding = io.imread(Reconstruction_Files[0][0])
    
    #Saving output(s) as hyperstack(s) (t,x,y)
    if Save_As_Hyperstack_Check.get() == 1:
    
        #Create empty output arrays dependent upon method chosen
        if Pipeline_Method_Selection.get() == 'Both':
            Z_Proj_Value = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
            Z_Proj_Loc = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        if Pipeline_Method_Selection.get() == 'Z Projection Value':
            Z_Proj_Value = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        if Pipeline_Method_Selection.get() == 'Z Location Value':
            Z_Proj_Loc = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        
        #Run for every time point
        for time_point in range(Reconstruction_Files.shape[1]):
            #Create empty input array
            Reconstruction_Built = np.zeros((Reconstruction_Files.shape[0],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')

            #Populate input array with holograms
            for x in range(Reconstruction_Files.shape[0]):
                Reconstruction_Built[x,:,:] = io.imread(Reconstruction_Files[x][time_point])
                #Print progress every 5 z-slices
                if x != 0 and x%5==0:
                    print(f'Finished loading {x} z-slices out of {Reconstruction_Files.shape[0]} ({np.round(timeit.default_timer()-start,3)}) seconds')
            
            
            print(f'Finding Z Projection and Location for Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds')
            #Minimum Projection used
            if Output_Min_Format.get() == 1:
                if Pipeline_Method_Selection.get() == 'Both':
                    Z_Proj_Value[time_point],Z_Proj_Loc[time_point] = np.min(Reconstruction_Built,axis=0),Z_Slice_Values[np.argmin(Reconstruction_Built,axis=0),1].astype('<f4')
                if Pipeline_Method_Selection.get() == 'Z Projection Value':
                    Z_Proj_Value[time_point] = np.min(Reconstruction_Built,axis=0)
                if Pipeline_Method_Selection.get() == 'Z Location Value':
                    Z_Proj_Loc[time_point] = Z_Slice_Values[np.argmin(Reconstruction_Built,axis=0),1].astype('<f4')
            
            #Maximum Projection used
            if Output_Max_Format.get() == 1:
                if Pipeline_Method_Selection.get() == 'Both':
                    Z_Proj_Value[time_point],Z_Proj_Loc[time_point] = np.max(Reconstruction_Built,axis=0),Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1].astype('<f4')
                if Pipeline_Method_Selection.get() == 'Z Projection Value':
                    Z_Proj_Value[time_point] = np.max(Reconstruction_Built,axis=0)
                if Pipeline_Method_Selection.get() == 'Z Location Value':
                    Z_Proj_Loc[time_point] = Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1].astype('<f4')
            
            print(f'\nCompleted Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds\n')
        
        #Save output arrays dependent upon method chosen
        if Pipeline_Method_Selection.get() == 'Both':
            print(f'Saving Z Projection tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
            io.imsave(Output_Directory_Text.get()+Z_Project_Value_Name.get()+'.tif',Z_Proj_Value,check_contrast=False)
            print(f'Saving Z Location tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
            io.imsave(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif',Z_Proj_Loc,check_contrast=False)
        if Pipeline_Method_Selection.get() == 'Z Projection Value':
            print(f'Saving Z Projection tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
            io.imsave(Output_Directory_Text.get()+Z_Project_Value_Name.get()+'.tif',Z_Proj_Value,check_contrast=False)
        if Pipeline_Method_Selection.get() == 'Z Location Value':
            print(f'Saving Z Location tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
            io.imsave(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif',Z_Proj_Loc,check_contrast=False)
        
    
    #Saving output(s) as time-stack(s) (x,y)
    if Save_As_Singles_Check.get() == 1:
        
        #Create empty output arrays dependent upon method chosen
        if Pipeline_Method_Selection.get() == 'Both':
            Z_Proj_Value = np.zeros((Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
            Z_Proj_Loc = np.zeros((Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        if Pipeline_Method_Selection.get() == 'Z Projection Value':
            Z_Proj_Value = np.zeros((Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        if Pipeline_Method_Selection.get() == 'Z Location Value':
            Z_Proj_Loc = np.zeros((Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
        
        #Run for every time point
        for time_point in range(Reconstruction_Files.shape[1]):
            #Create empty input array
            Reconstruction_Built = np.zeros((Reconstruction_Files.shape[0],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')

            #Populate input array with holograms
            for x in range(Reconstruction_Files.shape[0]):
                Reconstruction_Built[x,:,:] = io.imread(Reconstruction_Files[x][time_point])
                if x != 0 and x%5==0:
                    print(f'Finished loading {x} z-slices out of {Reconstruction_Files.shape[0]} ({np.round(timeit.default_timer()-start,3)}) seconds')
            
            #Minimum Projection used
            if Output_Min_Format.get() == 1:
                print(f'Finding Z Projection and Location for Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds')
                if Pipeline_Method_Selection.get() == 'Both':
                    Z_Proj_Value,Z_Proj_Loc = np.min(Reconstruction_Built,axis=0),Z_Slice_Values[np.argmin(Reconstruction_Built,axis=0),1].astype('<f4')
                if Pipeline_Method_Selection.get() == 'Z Projection Value':
                    Z_Proj_Value = np.min(Reconstruction_Built,axis=0)
                if Pipeline_Method_Selection.get() == 'Z Location Value':
                    Z_Proj_Loc = Z_Slice_Values[np.argmin(Reconstruction_Built,axis=0),1].astype('<f4')
            
            #Maximum Projection used
            if Output_Max_Format.get() == 1:
                print(f'Finding Z Projection and Location for Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds')
                if Pipeline_Method_Selection.get() == 'Both':
                    Z_Proj_Value,Z_Proj_Loc = np.max(Reconstruction_Built,axis=0),Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1].astype('<f4')
                if Pipeline_Method_Selection.get() == 'Z Projection Value':
                    Z_Proj_Value = np.max(Reconstruction_Built,axis=0)
                if Pipeline_Method_Selection.get() == 'Z Location Value':
                    Z_Proj_Loc = Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1].astype('<f4')
            
            print(f'\nCompleted Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds\n')
            
            
            #Creates the time point section of the file name (for example, this places three 0's in the file name '[name_chosen]_00011.tif')
            fileName_Time_Point_Addition = '0'*(5-len(str(time_point+1)))+str(time_point+1)
            
            #Save output arrays dependent upon method chosen
            if Pipeline_Method_Selection.get() == 'Both':
                print(f'Saving Z Projection tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
                io.imsave(Output_Directory_Text.get()+Z_Project_Value_Name.get()+_+fileName_Time_Point_Addition+'.tif',Z_Proj_Value,check_contrast=False)
                print(f'Saving Z Location tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
                io.imsave(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+_+fileName_Time_Point_Addition+'.tif',Z_Proj_Loc,check_contrast=False)
            if Pipeline_Method_Selection.get() == 'Z Projection Value':
                print(f'Saving Z Projection tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
                io.imsave(Output_Directory_Text.get()+Z_Project_Value_Name.get()+_+fileName_Time_Point_Addition+'.tif',Z_Proj_Value,check_contrast=False)
            if Pipeline_Method_Selection.get() == 'Z Location Value':
                print(f'Saving Z Location tif File ({np.round(timeit.default_timer()-start,3)}) seconds\n')
                io.imsave(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+_+fileName_Time_Point_Addition+'.tif',Z_Proj_Loc,check_contrast=False)
    
    print(f'Program completed in ({np.round(timeit.default_timer()-start,3)}) seconds')

def Input_Folder():
    '''
        Asks the user for the input directory and fills the entry
    '''
    Input_Directory_Text.set('')
    Input_Direction_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Input_Directory_Text_Entry.insert(END,Input_Direction_Chosen+'/')
    if Input_Directory_Text.get() == '/':
        Input_Directory_Text.set('(Required)')
    
def Output_Folder():
    '''
        Asks the user for the output directory and fills the entry
    '''
    Output_Directory_Text.set('')
    Output_Directory_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Output_Directory_Text_Entry.insert(END,Output_Directory_Chosen+'/')
    if Output_Directory_Text.get() == '/':
        Output_Directory_Text.set('(Required)')
 
 
def Select_Min_Format(*args):
    '''
        Select the minimum projection operation, below looks convoluted but is necessary to avoid a feedback loop due to both
        Output_Min_Format and Output_Max_Format calling a function when their value is changed.  To accomplish this, checks are
        put in place that only let one variable be adjusted per cycle.
    '''
    Min_Max_Format_Change_Processed = False
    if Output_Min_Max_Format_Changed.get() == 1:
        Min_Max_Format_Change_Processed = True
    if Output_Min_Max_Format_Changed.get() == 0:
        Output_Min_Max_Format_Changed.set(1)
        Output_Min_Format.set(1)
        Output_Max_Format.set(0)
    if Min_Max_Format_Change_Processed == True:
        Min_Max_Format_Change_Processed = False
        Output_Min_Max_Format_Changed.set(0)
    
def Select_Max_Format(*args):
    '''
        Select the maximum projection operation, below looks convoluted but is necessary to avoid a feedback loop due to both
        Output_Min_Format and Output_Max_Format calling a function when their value is changed.  To accomplish this, checks are
        put in place that only let one variable be adjusted per cycle.
    '''
    Min_Max_Format_Change_Processed = False
    if Output_Min_Max_Format_Changed.get() == 1:
        Min_Max_Format_Change_Processed = True
    if Output_Min_Max_Format_Changed.get() == 0:
        Output_Min_Max_Format_Changed.set(1)
        Output_Min_Format.set(0)
        Output_Max_Format.set(1)
    if Min_Max_Format_Change_Processed == True:
        Min_Max_Format_Change_Processed = False
        Output_Min_Max_Format_Changed.set(0)

def Save_Option_Window():
    '''
        The pop window to prompt the user to save as individual tifs or as a hyperstack
    '''
    save_choices = Tk()
    save_canvas = Canvas(save_choices)
    save_canvas.pack()
    
    def Save_As_Hyperstack():
        '''
            Sets the checks to save as a hyperstack
        '''
        Save_As_Hyperstack_Check.set(1)
        Save_As_Singles_Check.set(0)
        Close_And_Run()
    
    def Save_As_Singles():
        '''
            Sets the checks to save as individual time stacka
        '''
        Save_As_Hyperstack_Check.set(0)
        Save_As_Singles_Check.set(1)
        Close_And_Run()
    
    def Close_And_Run():
        '''
            Closes window when done
        '''
        save_choices.destroy()
        Z_Projection()
        
    '''
        Creates objects to place on pop-up window
    '''
    Save_Options_Label = Label(save_canvas,text='Save derivative tifs as a hyperstack or individual files?')
    Save_Options_Label_Canvas = save_canvas.create_window(150,28,window=Save_Options_Label)
    Save_As_Hyperstack_Button = Button(save_choices,text='Save as hyperstack',command=Save_As_Hyperstack)
    Save_As_Hyperstack_Button_Canvas = save_canvas.create_window(75,56,window=Save_As_Hyperstack_Button)
    Save_As_Singles_Button = Button(save_choices,text='Save individual tifs',command=Save_As_Singles)
    Save_As_Singles_Button_Canvas = save_canvas.create_window(225,56,window=Save_As_Singles_Button)
    
    '''
        Set window parameters
    '''
    save_choices.title('Save Options')
    w = 300 # width for the Tk save_choices
    h = 100 # height for the Tk save_choices
    ws = save_choices.winfo_screenwidth() # width of the screen
    hs = save_choices.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    save_choices.geometry('%dx%d+%d+%d' % (w, h, x, y))

def Pipeline_Choice_Selected(*args):
    '''
        Populate the objects on the main window dependent upon which projection method is chosen
        
        Creates all canvases at the start and either deletes the unused or moves the used in the case of only Z Location desired
    '''
    Z_Project_Value_Name_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Value_Name_Label)
    Z_Project_Value_Name_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Value_Name_Entry)
    Z_Project_Loc_Name_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Z_Loc_Spacing.get(),window=Z_Project_Loc_Name_Label)
    Z_Project_Loc_Name_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Z_Loc_Spacing.get(),window=Z_Project_Loc_Name_Entry)
    
    if Pipeline_Method_Selection.get() == 'Select One':
        canvas.delete(Z_Project_Value_Name_Label_Canvas)
        canvas.delete(Z_Project_Value_Name_Entry_Canvas)
        canvas.delete(Z_Project_Loc_Name_Label_Canvas)
        canvas.delete(Z_Project_Loc_Name_Entry_Canvas)
    if Pipeline_Method_Selection.get() == 'Z Projection Value':
        canvas.delete(Z_Project_Loc_Name_Label_Canvas)
        canvas.delete(Z_Project_Loc_Name_Entry_Canvas)
    if Pipeline_Method_Selection.get() == 'Z Location Value':
        canvas.delete(Z_Project_Value_Name_Label_Canvas)
        canvas.delete(Z_Project_Value_Name_Entry_Canvas)
        Z_Project_Loc_Name_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Loc_Name_Label)
        Z_Project_Loc_Name_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Loc_Name_Entry)
    
    
    
if __name__ == '__main__':
    '''
        The window/GUI, this section creates the main window the user interacts with
        GUI - name of the window
        canvas - name of the canvas that spans the window, where the objects are placed
    '''
    GUI = Tk()
    canvas = Canvas()
    canvas.pack(fill=BOTH, expand=YES)
    
    '''
        Entity sizes defined here
    '''
    Entry_Width = 90
    Button_Label_Width = 29
    Menu_Width = 160
    
    '''
        The objects placed on the window/interface
    '''
    
    Input_Directory_Text = StringVar()
    Input_Directory_Text.set('(Required)')
    Input_Directory_Text_Entry = Entry(GUI,textvariable=Input_Directory_Text,width=Entry_Width)
    Input_Directory_Button = Button(GUI,text='Select Reconstruction Input Directory',command=Input_Folder,width=Button_Label_Width)
    Output_Directory_Text = StringVar()
    Output_Directory_Text.set('(Required)')
    Output_Directory_Button = Button(GUI,text='Select Projection Output Directory',command=Output_Folder,width=Button_Label_Width)
    Output_Directory_Text_Entry = Entry(GUI,textvariable=Output_Directory_Text,width=Entry_Width)
    Z_Project_Value_Name = StringVar()
    Z_Project_Value_Name.set('(Required)')
    Z_Project_Value_Name_Entry = Entry(GUI,textvariable=Z_Project_Value_Name,width=Entry_Width)
    Z_Project_Value_Name_Label = Label(GUI,text='Input Z Projection Output Filename:',width=Button_Label_Width)
    Z_Project_Loc_Name = StringVar()
    Z_Project_Loc_Name.set('(Required)')
    Z_Project_Loc_Name_Entry = Entry(GUI,textvariable=Z_Project_Loc_Name,width=Entry_Width)
    Z_Project_Loc_Name_Label = Label(GUI,text='Input Z Location Output Filename:',width=Button_Label_Width)
    Start_Processing_Button = Button(GUI,text='Start Processing',command=Error_Checking,width=Button_Label_Width)
    Save_As_Hyperstack_Check = IntVar()
    Save_As_Singles_Check = IntVar()
    Introduction_Message = Label(GUI,text='Select the folder with your reconstructions for input and the output for where the projection data will be placed.')
    Pipeline_Method_Selection = StringVar()
    Pipeline_Method_Selection.set('Select One')
    Pipeline_Method_Selection.trace('w',Pipeline_Choice_Selected)
    Pipeline_Method_Menu = OptionMenu(GUI,Pipeline_Method_Selection,'Select One','Z Projection Value','Z Location Value','Both')
    Pipeline_Method_Label = Label(GUI,text='Desired Projection Output:')
    Output_Min_Max_Format_Label = Label(GUI,text='Output Mode:')
    Output_Min_Format = IntVar()
    Output_Min_Format.trace('w',Select_Min_Format)
    Output_Max_Format = IntVar()
    Output_Max_Format.set(1)
    Output_Max_Format.trace('w',Select_Max_Format)
    Output_Min_Max_Format_Changed = IntVar()
    Output_Max_Format_Checkbox = Checkbutton(GUI,text='Max Projection',variable=Output_Max_Format)
    Output_Min_Format_Checkbox = Checkbutton(GUI,text='Min Projection',variable=Output_Min_Format)

    '''
        Error messages/symbols
    '''
    Overall_Error_Message = Label(GUI,text='*** Missing Correct Inputs("#)"), Please Correct and Try Again ***')
    Input_Error_Label = Label(GUI,text='1)')
    Output_Error_Label = Label(GUI,text='2)')
    Z_Value_Error_Label = Label(GUI,text='3)')
    Z_Loc_Error_Label = Label(GUI,text='4)')
    
    Input_Folder_Error_Check = IntVar()
    Input_Subfolder_Error_Check = IntVar()
    Input_Reconstruction_Files_Error_Check = IntVar()
    Input_Folder_Error = Label(GUI,text='1) Reconstruction Directory Is Not A Valid Directory')
    Input_Subfolder_Error = Label(GUI,text='1) Reconstruction Directory Does Not Contain Valid Folders')
    Input_Reconstruction_Files_Error = Label(GUI,text='1) Reconstruction Directory Contains Invalid Holograms')
    Output_Directory_Folder_Error = Label(GUI,text='2) Output Is Not a Valid Directory')
    Z_Value_Filename_Error = Label(GUI,text='3) Z Projection is an Invalid Filename')
    Z_Loc_Filename_Error = Label(GUI,text='4) Z Location is an Invalid Filename')
    Projection_Output_Method_Error = Label(GUI,text='5)')
    Projection_Output_Method_Error_Message = Label(GUI,text='5) Select an option')

    '''
        The placement of each component in the vertical direction is determined by a spacing of 28 units, each next set is given a value of 28 units below the previous one.  This allows for a smooth increase should sections need to be added or removed.
    '''
    Intro_Spacing,Overal_Error_Spacing,Input_Spacing,Output_Spacing,Z_Value_Spacing,Z_Loc_Spacing,Start_Process_Spacing,Label_Button_Horizontal,Entry_Horizontal,Start_Processing_Horizontal,Error_Symbol_Horizontal,gap,Z_Value_Error_Spacing,Z_Loc_Error_Spacing,Input_Output_Error_Horizontal,Output_Filenames_Horizontal,Pipeline_Menu_Horizontal,Pipeline_Menu_Spacing,Canvas_Height,Output_Min_Max_Spacing,Max_Format_Horizontal,Min_Format_Horizontal = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()
    
    gap.set(28)
    
    Intro_Spacing.set(1*gap.get())
    Overal_Error_Spacing.set((Intro_Spacing.get()/gap.get()+1)*gap.get())
    Input_Spacing.set((Overal_Error_Spacing.get()/gap.get()+1)*gap.get())
    Output_Spacing.set((Input_Spacing.get()/gap.get()+1)*gap.get())
    Pipeline_Menu_Spacing.set((Output_Spacing.get()/gap.get()+1)*gap.get())
    Output_Min_Max_Spacing.set((Pipeline_Menu_Spacing.get()/gap.get()+1)*gap.get())
    Z_Value_Spacing.set((Output_Min_Max_Spacing.get()/gap.get()+1)*gap.get())
    Z_Loc_Spacing.set((Z_Value_Spacing.get()/gap.get()+1)*gap.get())
    Z_Value_Error_Spacing.set((Z_Loc_Spacing.get()/gap.get()+1)*gap.get())
    Z_Loc_Error_Spacing.set((Z_Value_Error_Spacing.get()/gap.get()+1)*gap.get())
    Start_Process_Spacing.set((Z_Loc_Error_Spacing.get()/gap.get()+1)*gap.get())
    Canvas_Height.set((Start_Process_Spacing.get()/gap.get()+1)*gap.get())
    
    if platform.system() == 'Windows':
        Label_Button_Horizontal.set(150)
        Entry_Horizontal.set(532)
        Start_Processing_Horizontal.set(400)
        Error_Symbol_Horizontal.set(25)
        Input_Output_Error_Horizontal.set(200)
        Output_Filenames_Horizontal.set(600)
        Pipeline_Menu_Horizontal.set(337)
        Max_Format_Horizontal.set(310)
        Min_Format_Horizontal.set(Max_Format_Horizontal.get()+125)
    
    if platform.system() == 'Mac':
        Label_Button_Horizontal.set(170)
        Entry_Horizontal.set(730)
        Start_Processing_Horizontal.set(400)
        Error_Symbol_Horizontal.set(25)
        Input_Output_Error_Horizontal.set(200)
        Output_Filenames_Horizontal.set(600)
    

    '''
        Initial placement of the components onto the window
    '''
    Introduction_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Intro_Spacing.get(),window=Introduction_Message)
    Input_Directory_Button_Canvas =  canvas.create_window(Label_Button_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Button)
    Input_Directory_Text_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Text_Entry)
    Output_Directory_Button_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Output_Spacing.get(),window=Output_Directory_Button)
    Output_Directory_Text_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Output_Spacing.get(),window=Output_Directory_Text_Entry)
    Output_Min_Max_Format_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Min_Max_Format_Label)
    Output_Min_Format_Canvas = canvas.create_window(Max_Format_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Min_Format_Checkbox)
    Output_Max_Format_Cancas = canvas.create_window(Min_Format_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Max_Format_Checkbox)
    Pipeline_Method_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Pipeline_Menu_Spacing.get(),window=Pipeline_Method_Label)
    Pipeline_Method_Menu_Canvas = canvas.create_window(Pipeline_Menu_Horizontal.get(),Pipeline_Menu_Spacing.get(),window=Pipeline_Method_Menu,width=Menu_Width)
    Start_Processing_Button_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Start_Process_Spacing.get(),window=Start_Processing_Button)
    
    
    GUI.title("Z Projection Value and Location from Amplitude Reconstruction")
    w = 850 # width for the Tk GUI
    h = Canvas_Height.get() # height for the Tk GUI
    ws = GUI.winfo_screenwidth() # width of the screen
    hs = GUI.winfo_screenheight() # height of the screen
    Percent_Horizontal = 50 #Percentage value
    Percent_Vertical = 50 #Percentage value
    x = (ws*Percent_Horizontal/100) - (w/2)
    y = (hs*Percent_Vertical/100) - (h/2)
    GUI.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GUI.mainloop()
