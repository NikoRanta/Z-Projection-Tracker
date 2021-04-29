import os
from os import listdir
from os.path import isfile,join,isdir
import numpy as np
from skimage import io
import timeit
from tkinter import *
from tkinter import filedialog
import platform
import json


def Order_Holograms_After_Reconstruction(folderPath):
    '''
        Organizes the reconstruction folders into an array that can be called.  The first axis is z-slices and the second axis is the time points.
    '''
    
    Folder_Names = np.array([(f,float(f.name)) for f in os.scandir(folderPath)])
    #Descending_Order = Folder_Names[(-Folder_Names[:,1]).argsort()]
    Ascending_Order = Folder_Names[Folder_Names[:,1].argsort()]
    folder_names_combined = np.zeros((len(Ascending_Order),len(listdir(Ascending_Order[0,0].path)))).astype(np.unicode_)
    Organized_Files = []
    for x in range(len(Ascending_Order)):
        File_Names = [File_Names for File_Names in listdir(Ascending_Order[x,0].path) if isfile(join(Ascending_Order[x,0],File_Names))]
        z_slice_time_stamp_names = np.array([File_Names[x].split('.') for x in range(len(File_Names))])
        folder_names_combined[x] = np.array([z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][x][0]+'.'+z_slice_time_stamp_names[z_slice_time_stamp_names[:,0].astype(np.float).argsort()][x][1] for x in range(len(File_Names))])
        
    for x in range(len(folder_names_combined[:,0])):
        for y in range(len(folder_names_combined[0,:])):
            Organized_Files.append(Ascending_Order[x,0].path+'/'+str(folder_names_combined[x,y]))
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
    Input_Folder_Error_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Input_Spacing_Error.get(),window=Input_Folder_Error)
    Input_Subfolder_Error_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Input_Spacing_Error.get(),window=Input_Subfolder_Error)
    Input_Reconstruction_Files_Error_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Input_Spacing_Error.get(),window=Input_Reconstruction_Files_Error)
    Size_Dropdown_Error_Canvas = canvas.create_window(Error_Symbol_Horizontal.get(),Size_Spacing.get(),window=Size_Dropdown_Error)
    
    
    '''
        Check if reconstructions in the input folder selected are formatted properly
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
    
    if Size_Dropdown_Selection.get() == 'Select One':
        Errors_Found[3] = 1
    if Size_Dropdown_Selection.get() != 'Select One':
        canvas.delete(Size_Dropdown_Error_Canvas)
        Errors_Found[3] = 0
    
    
    
    '''
        Count the number of errors
    '''
    Error_Count = np.count_nonzero(Errors_Found!=0)
    
    '''
        Delete the error messages that are not needed.
    '''
       
    if Errors_Found[0] == 0:
        canvas.delete(Input_Error_Label_Canvas)
    #if Errors_Found[2] == 0:
    #    canvas.delete(Z_Value_Error_Label_Canvas)
    #    canvas.delete(Z_Value_Filename_Error_Canvas)
    
    if Error_Count == 0:
        canvas.delete(Overall_Error_Message_Canvas)
        GUI.update()
        Testing_Check.set(1)
        Z_Projection()

    

def Z_Projection():
    '''
        start - The starting point for reporting how long the processes have taken
        Reconstruction_Files - The files that have their paths denoted and are sorted by increasing value of Z
        Z_Slice_Values[1] - The z slice values, used for locating which slice the max value came from
        Z_Proj_Value - An array of the maximum value of each xy column
        Z_Proj_Loc - An array of the z slice where the maximum value is for each xy column
    '''
    start = timeit.default_timer()
    Reconstruction_Files,Z_Slice_Values = Order_Holograms_After_Reconstruction(Input_Directory_Text.get())
    Shape_Finding = io.imread(Reconstruction_Files[0][0])
    Z_Proj_Value = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
    Z_Proj_Loc = np.zeros((Reconstruction_Files.shape[1],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')
    
    for time_point in range(Reconstruction_Files.shape[1]):
        Reconstruction_Built = np.zeros((Reconstruction_Files.shape[0],Shape_Finding.shape[0],Shape_Finding.shape[1]),'<f4')

        for x in range(Reconstruction_Files.shape[0]):
            Reconstruction_Built[x,:,:] = io.imread(Reconstruction_Files[x][time_point])
            if x != 0 and x%5==0:
                print(f'Finished loading {x} z-slices out of {Reconstruction_Files.shape[0]} ({np.round(timeit.default_timer()-start,3)}) seconds')
            
        print(f'Finding Z Projection and Location for Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds')
        if Output_Max_Format.get() == 1:
            Z_Proj_Loc[time_point] = Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1].astype('<f4')
        if Output_Min_Format.get() == 1:
            Z_Proj_Loc[time_point] = Z_Slice_Values[np.argmin(Reconstruction_Built,axis=0),1].astype('<f4')
        print(f'\nCompleted Time Point #{time_point+1} ({np.round(timeit.default_timer()-start,3)}) seconds\n')
        
        #Put the json files in numerical order
        File_Names = np.array([(f,int(f.name.split('.')[0])) for f in os.scandir(Input_JSON_Folder_Text.get())])
        
        if Testing_Check.get() == 0:
            Saving = False
        if Testing_Check.get() == 1:
            Saving = True
        
        
        print('Edit JSON files')
        start = timeit.default_timer()
        #Opens each successive json file
        for JSON_File in range(File_Names.shape[0]):
            data = json.load(open(File_Names[JSON_File,0])) #Reads json file data
            
            for Time_Spots in data['Times']: #Reads the Particles Position values
                if Time_Spots == time_point and data['Particles_Position'][Time_Spots]: #Ignores None data
                    #Appends the Z Location information from the tif file into the list for each particle found
                    X_Location = int(data['Particles_Position'][Time_Spots][0])
                    Y_Location = int(data['Particles_Position'][Time_Spots][1])
                    if Size_Dropdown_Selection.get() == '1024x1024':
                        Z_Location = int(Z_Proj_Loc[Time_Spots,2*Y_Location,2*X_Location])
                    if Size_Dropdown_Selection.get() == '2048x2048':
                        Z_Location = int(Z_Proj_Loc[Time_Spots,Y_Location,X_Location])
                    data['Particles_Position'][Time_Spots].append(Z_Location)

            if Saving:
                json.dump(data,open(File_Names[JSON_File,0],'w')) #Saves the adjustments
        print(f'Took {np.round(timeit.default_timer()-start,3)} seconds')
        
    print(f'Program completed in ({np.round(timeit.default_timer()-start,3)}) seconds')

def Input_Folder():
    '''
        Asks the user for the input directory and fills the entry
    '''
    Input_Directory_Text.set('')
    Input_Direction_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Input_Directory_Text.set(Input_Direction_Chosen+'/')
    if Input_Directory_Text.get() == '/':
        Input_Directory_Text.set('(Required)')
def Input_JSON_Folder():
    '''
        Asks the user for the input directory and fills the entry
    '''
    Input_JSON_Folder_Text.set('')
    Input_JSON_Folder_Text_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Input_JSON_Folder_Text.set(Input_JSON_Folder_Text_Chosen+'/')
    if Input_JSON_Folder_Text.get() == '/':
        Input_JSON_Folder_Text.set('(Required)')




def Select_Min_Format(*args):
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

    
if __name__ == '__main__':
    '''
        The window/GUI, this section creates the main window the user interacts with
        GUI - name of the window
        canvas - name of the canvas that spans the window, where the objects are placed
    '''
    GUI = Tk()
    canvas = Canvas()
    canvas.pack(fill=BOTH, expand=YES)
    
    Entry_Width = 90
    Button_Label_Width = 29
    
    '''
        The objects placed on the window/interface
    '''
    
    Input_Directory_Text = StringVar()
    Input_Directory_Text.set('(Required)')
    Input_Directory_Text.set('D:/Reconstruction/Louie/Reconstruction/Amplitude/')
    Input_Directory_Text_Entry = Entry(GUI,textvariable=Input_Directory_Text,width=Entry_Width)
    Input_Directory_Button = Button(GUI,text='Select Reconstruction Input Directory',command=Input_Folder,width=Button_Label_Width)
    Start_Processing_Button = Button(GUI,text='Start Processing',command=Error_Checking,width=Button_Label_Width)
    Save_As_Hyperstack_Check = IntVar()
    Save_As_Singles_Check = IntVar()
    Introduction_Message = Label(GUI,text='Select the folder with your reconstructions for input and the output for where the projection data will be placed.')
    Output_Min_Max_Format_Label = Label(GUI,text='Output Mode:')
    Output_Min_Format = IntVar()
    Output_Min_Format.trace('w',Select_Min_Format)
    Output_Max_Format = IntVar()
    Output_Max_Format.set(1)
    Output_Max_Format.trace('w',Select_Max_Format)
    Output_Min_Max_Format_Changed = IntVar()
    Output_Max_Format_Checkbox = Checkbutton(GUI,text='Max Projection',variable=Output_Max_Format)
    Output_Min_Format_Checkbox = Checkbutton(GUI,text='Min Projection',variable=Output_Min_Format)
    Input_JSON_Folder_Text = StringVar()
    Input_JSON_Folder_Text.set('(Required)')
    Input_JSON_Folder_Text.set('D:/Reconstruction/Louie/tracks/')
    Input_JSON_Folder_Button = Button(GUI,text='Select Folder with JSON Tracks ONLY',command=Input_JSON_Folder,width=Button_Label_Width)
    Input_JSON_Folder_Entry = Entry(GUI,textvariable=Input_JSON_Folder_Text,width=Entry_Width)
    Size_Dropdown_Label = Label(GUI,text='JSON Resolution')
    Size_Dropdown_Selection = StringVar()
    Size_Dropdown_Selection.set('Select One')
    Size_Dropdown_Menu = OptionMenu(GUI,Size_Dropdown_Selection,'Select One','1024x1024','2048x2048')

    '''
        Error messages/symbols
    '''
    
    Overall_Error_Message = Label(GUI,text='*** Missing Correct Inputs(*), Please Correct and Try Again ***')
    Input_Error_Label = Label(GUI,text='*')
    Output_Error_Label = Label(GUI,text='*')
    Input_Folder_Error_Check = IntVar()
    Input_Subfolder_Error_Check = IntVar()
    Input_Reconstruction_Files_Error_Check = IntVar()
    Input_Folder_Error = Label(GUI,text='Reconstruction Directory Is Not A Valid Directory')
    Input_Subfolder_Error = Label(GUI,text='Reconstruction Directory Does Not Contain Valid Folders')
    Input_Reconstruction_Files_Error = Label(GUI,text='Reconstruction Directory Contains Invalid Holograms')
    Output_Directory_Folder_Error = Label(GUI,text='Output Is Not a Valid Directory')
    Testing_Check = IntVar()
    Size_Dropdown_Error = Label(GUI,text='*')

    '''
        The placement of each component in the vertical direction is determined by a spacing of 28 units, each next set is given a value of 28 units below the previous one.  This allows for a smooth increase should sections need to be added or removed.
    '''
    Intro_Spacing,Overal_Error_Spacing,Input_Spacing,Input_Spacing_Error,Output_Spacing,Z_Value_Spacing,Z_Loc_Spacing,Start_Process_Spacing,Label_Button_Horizontal,Entry_Horizontal,Start_Processing_Horizontal,Error_Symbol_Horizontal,gap,Z_Value_Error_Spacing,Z_Loc_Error_Spacing,Input_Output_Error_Horizontal,Output_Filenames_Horizontal,Stack_vs_Hyperstack_Spacing,Input_Stack_Horizontal,Input_Hyperstack_Horizontal,Output_Min_Max_Spacing,Max_Format_Horizontal,Min_Format_Horizontal,Input_JSON_Spacing,Size_Spacing = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()
    
    gap.set(28)
    
    Intro_Spacing.set(1*gap.get())
    Overal_Error_Spacing.set((Intro_Spacing.get()/gap.get()+1)*gap.get())
    Input_Spacing.set((Overal_Error_Spacing.get()/gap.get()+1)*gap.get())
    Input_Spacing_Error.set((Input_Spacing.get()/gap.get()+1)*gap.get())
    Input_JSON_Spacing.set((Input_Spacing_Error.get()/gap.get()+1)*gap.get())
    Output_Min_Max_Spacing.set((Input_JSON_Spacing.get()/gap.get()+1)*gap.get())
    Size_Spacing.set((Output_Min_Max_Spacing.get()/gap.get()+1)*gap.get())
    Start_Process_Spacing.set((Size_Spacing.get()/gap.get()+1)*gap.get())
    
    if platform.system() == 'Windows':
        Label_Button_Horizontal.set(150)
        Entry_Horizontal.set(532)
        Start_Processing_Horizontal.set(400)
        Error_Symbol_Horizontal.set(25)
        Input_Output_Error_Horizontal.set(200)
        Output_Filenames_Horizontal.set(600)
        Input_Stack_Horizontal.set(285)
        Input_Hyperstack_Horizontal.set(Input_Stack_Horizontal.get()+100)
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
    Output_Min_Max_Format_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Min_Max_Format_Label)
    Output_Min_Format_Canvas = canvas.create_window(Max_Format_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Min_Format_Checkbox)
    Output_Max_Format_Cancas = canvas.create_window(Min_Format_Horizontal.get(),Output_Min_Max_Spacing.get(),window=Output_Max_Format_Checkbox)
    Input_JSON_Folder_Button_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Input_JSON_Spacing.get(),window=Input_JSON_Folder_Button)
    Input_JSON_Folder_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Input_JSON_Spacing.get(),window=Input_JSON_Folder_Entry)
    Size_Dropdown_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Size_Spacing.get(),window=Size_Dropdown_Label)
    Size_Dropdown_Menu_Canvas = canvas.create_window(Max_Format_Horizontal.get(),Size_Spacing.get(),window=Size_Dropdown_Menu)
    Start_Processing_Button_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Start_Process_Spacing.get(),window=Start_Processing_Button)
    
    
    GUI.title("Z Projection Value and Location from Amplitude Reconstruction")
    w = 850 # width for the Tk GUI
    h = Start_Process_Spacing.get()+gap.get() # height for the Tk GUI
    ws = GUI.winfo_screenwidth() # width of the screen
    hs = GUI.winfo_screenheight() # height of the screen
    Percent_Horizontal = 50 #Percentage value
    Percent_Vertical = 50 #Percentage value
    x = (ws*Percent_Horizontal/100) - (w/2)
    y = (hs*Percent_Vertical/100) - (h/2)
    GUI.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GUI.mainloop()