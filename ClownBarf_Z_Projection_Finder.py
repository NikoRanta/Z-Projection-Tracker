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
    Errors_Found = np.zeros(4)
    '''
        All error symbols are drawn to allow the program to properly remove them should the error be fixed.  Without creating them, a tkinter variable error occurs.
    '''
    Overall_Error_Message_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),gap.get(),window=Overall_Error_Message)
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
    if Z_Project_Value_Name.get() == '(Required)':
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
    if Z_Project_Loc_Name.get() == '(Required)':
        Errors_Found[3] = 1
    try:
        with open(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif','w') as file:
            pass
    except:
        Errors_Found[3] = 1
    else:
        os.remove(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif')
        
        
        
    
    '''
        Count the number of errors
    '''
    Error_Count = np.count_nonzero(Errors_Found!=0)
    
    '''
        Delete the error messages that are not needed.
    '''
    if Error_Count == 0:
        canvas.delete(Overall_Error_Message_Canvas)
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
    
    
    return Error_Count

    

def Z_Projection():
    Errors = Error_Checking()
    if Errors == 0:
        GUI.update()
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
                
            print(f'Finding Z Projection and Location for Time Point #{time_point} ({np.round(timeit.default_timer()-start,3)}) seconds')
            Z_Proj_Value[time_point],Z_Proj_Loc[time_point] = np.max(Reconstruction_Built,axis=0),Z_Slice_Values[np.argmax(Reconstruction_Built,axis=0),1]
            print(f'Completed Time Point #{time_point} ({np.round(timeit.default_timer()-start,3)}) seconds')
        
        
        print(f'Saving Z Projection tif File ({np.round(timeit.default_timer()-start,3)}) seconds')
        io.imsave(Output_Directory_Text.get()+Z_Project_Value_Name.get()+'.tif',Z_Proj_Value)
        print(f'Saving Z Location tif File ({np.round(timeit.default_timer()-start,3)}) seconds')
        io.imsave(Output_Directory_Text.get()+Z_Project_Loc_Name.get()+'.tif',Z_Proj_Loc)
        
        
        print(f'Program completed in ({np.round(timeit.default_timer()-start,3)}) seconds')

def Input_Folder():
    Input_Directory_Text.set('')
    Input_Direction_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Input_Directory_Text_Entry.insert(END,Input_Direction_Chosen+'/')
    if Input_Directory_Text.get() == '/':
        Input_Directory_Text.set('(Required)')
    
def Output_Folder():
    Output_Directory_Text.set('')
    Output_Directory_Chosen = filedialog.askdirectory(parent=GUI,title='Choose a directory')
    Output_Directory_Text_Entry.insert(END,Output_Directory_Chosen+'/')
    if Output_Directory_Text.get() == '/':
        Output_Directory_Text.set('(Required)')
    
if __name__ == '__main__':
    GUI = Tk()
    canvas = Canvas()
    canvas.pack(fill=BOTH, expand=YES)
    
    Entry_Width = 90
    Button_Label_Width = 29
    
    GUI_Components_Show = True
    if GUI_Components_Show:
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
        Z_Project_Loc_Name.set('(Required)')1
        Z_Project_Loc_Name_Entry = Entry(GUI,textvariable=Z_Project_Loc_Name,width=Entry_Width)
        Z_Project_Loc_Name_Label = Label(GUI,text='Input Z Location Output Filename:',width=Button_Label_Width)
        Start_Processing_Button = Button(GUI,text='Start Processing',command=Z_Projection,width=Button_Label_Width)
    
    Error_Label_Show = True
    if Error_Label_Show:
        Overall_Error_Message = Label(GUI,text='*** Missing Correct Inputs(*), Please Correct and Try Again ***')
        Input_Error_Label = Label(GUI,text='*')
        Output_Error_Label = Label(GUI,text='*')
        Z_Value_Error_Label = Label(GUI,text='*')
        Z_Loc_Error_Label = Label(GUI,text='*')
        Input_Folder_Error_Check = IntVar()
        Input_Subfolder_Error_Check = IntVar()
        Input_Reconstruction_Files_Error_Check = IntVar()
        Input_Folder_Error = Label(GUI,text='Reconstruction Directory Is Not A Valid Directory')
        Input_Subfolder_Error = Label(GUI,text='Reconstruction Directory Does Not Contain Valid Folders')
        Input_Reconstruction_Files_Error = Label(GUI,text='Reconstruction Directory Contains Invalid Holograms')
        Output_Directory_Folder_Error = Label(GUI,text='Output Is Not a Valid Directory')
        Z_Value_Filename_Error = Label(GUI,text='Z Projection is an Invalid Filename')
        Z_Loc_Filename_Error = Label(GUI,text='Z Location is an Invalid Filename')
    
    Spacing_Show = True
    if Spacing_Show:
        Input_Spacing,Output_Spacing,Z_Value_Spacing,Z_Loc_Spacing,Start_Process_Spacing,Label_Button_Horizontal,Entry_Horizontal,Start_Processing_Horizontal,Error_Symbol_Horizontal,gap,Z_Value_Error_Spacing,Z_Loc_Error_Spacing,Input_Output_Error_Horizontal,Output_Filenames_Horizontal = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()
        
        gap.set(28)
        
        Input_Spacing.set(2*gap.get())
        Output_Spacing.set((Input_Spacing.get()/gap.get()+1)*gap.get())
        Z_Value_Spacing.set((Output_Spacing.get()/gap.get()+1)*gap.get())
        Z_Loc_Spacing.set((Z_Value_Spacing.get()/gap.get()+1)*gap.get())
        Z_Value_Error_Spacing.set((Z_Loc_Spacing.get()/gap.get()+1)*gap.get())
        Z_Loc_Error_Spacing.set((Z_Value_Error_Spacing.get()/gap.get()+1)*gap.get())
        Start_Process_Spacing.set((Z_Loc_Error_Spacing.get()/gap.get()+1)*gap.get())
        
        if platform.system() == 'Windows':
            Label_Button_Horizontal.set(150)
            Entry_Horizontal.set(532)
            Start_Processing_Horizontal.set(400)
            Error_Symbol_Horizontal.set(25)
            Input_Output_Error_Horizontal.set(200)
            Output_Filenames_Horizontal.set(600)
        
        if platform.system() == 'Mac':
            Label_Button_Horizontal.set(170)
            Entry_Horizontal.set(730)
            Start_Processing_Horizontal.set(400)
            Error_Symbol_Horizontal.set(25)
            Input_Output_Error_Horizontal.set(200)
            Output_Filenames_Horizontal.set(600)
        
    
    Canvas_Show = True
    if Canvas_Show:
        Input_Directory_Button_Canvas =  canvas.create_window(Label_Button_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Button)
        Input_Directory_Text_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Input_Spacing.get(),window=Input_Directory_Text_Entry)
        Output_Directory_Button_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Output_Spacing.get(),window=Output_Directory_Button)
        Output_Directory_Text_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Output_Spacing.get(),window=Output_Directory_Text_Entry)
        Z_Project_Value_Name_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Value_Name_Label)
        Z_Project_Value_Name_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Z_Value_Spacing.get(),window=Z_Project_Value_Name_Entry)
        Z_Project_Loc_Name_Label_Canvas = canvas.create_window(Label_Button_Horizontal.get(),Z_Loc_Spacing.get(),window=Z_Project_Loc_Name_Label)
        Z_Project_Loc_Name_Entry_Canvas = canvas.create_window(Entry_Horizontal.get(),Z_Loc_Spacing.get(),window=Z_Project_Loc_Name_Entry)
        Start_Processing_Button_Canvas = canvas.create_window(Start_Processing_Horizontal.get(),Start_Process_Spacing.get(),window=Start_Processing_Button)
    
    
    GUI.title("Z Projection Value and Location from Amplitude Reconstruction")
    w = 850 # width for the Tk GUI
    h = Start_Process_Spacing.get()+gap.get() # height for the Tk GUI
    ws = GUI.winfo_screenwidth() # width of the screen
    hs = GUI.winfo_screenheight() # height of the screen
    Percent_Horizontal = 30 #Percentage value
    Percent_Vertical = 50 #Percentage value
    x = (ws*Percent_Horizontal/100) - (w/2)
    y = (hs*Percent_Vertical/100) - (h/2)
    GUI.geometry('%dx%d+%d+%d' % (w, h, x, y))
    GUI.mainloop()