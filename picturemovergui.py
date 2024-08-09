#Author: Devin Dulude
#Version: 1.1 (cleaned up code and comments)
#About: Python program created to use specifically with Fastfoto software to move
# the non-enhanced versions of your scanned photos to their own folder if you chose to keep them.
# This way you don't have duplicates in the folder when viewing the photos.

import tkinter as tk
import os, sys, shutil
from tkinter.filedialog import askdirectory
#tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
sourcedir = ""
originalsPath = ""
tocopy = []
debug = False


# prompts user to pick directory and adds it to the field
def handleDirectory():
    global sourcedir
    sourcedir = askdirectory()
    print("Using '" + sourcedir + "' as source directory")

    dir.delete(0, 'end')
    dir.insert(0, sourcedir)

# makes sure the path is valid and exists. Also makes sure we arent in a folder called Originals. Then checks for existing Originals
# folder and creates it if not exists.
def checkPath():
    global originalsPath, sourcedir
    sourcedir = dir.get()
    while True:
        if not(os.path.exists(sourcedir)):
            print("Invalid path entered. Path does not exist")
            tk.messagebox.showerror(title="Originals Photo Sorter", message="Invalid file path. Path does not exist.")
            break

        if str(sourcedir).endswith((r'/Originals', r'/Originals/')):
            print("Source folder IS 'Originals'. Source folder cannot be an 'Originals' folder")
            tk.messagebox.showerror(title="Originals Photo Sorter", message="Source folder cannot be 'Originals'.")
            break
        
        originalsPath = sourcedir + "/Originals"
        if not (os.path.exists(originalsPath)):
            print("Folder 'Originals' not found...creating")

            try:
                os.mkdir(originalsPath)
            except OSError as error:
                print(error)
                print("Couldn't create folder 'Originals', no action has been taken.")
                break
        else:
            if debug:
                print("Originals folder already exists, continuing")
            return True

# makes sure to only handle .jpg files and adds originalsPath to a tocopy list.
def sortPics():
    jpgs = []
    global tocopy

    # grab only jpgs
    for file in os.listdir(sourcedir):
        if str(file).lower().endswith('.jpg'):
            jpgs.append(file)

    # go through jpgs and filter out which to move
    for picture in jpgs:
        if (str(picture).endswith('_a.jpg')):
            continue # we never move anything that ends with _a, so we continue 

        if moveBside.get() == 0 and str(picture).endswith('_b.jpg'): # if not moving B side & ends with _b, dont add to queue and continue
            continue

        # finally, add this pic to queue
        tocopy.append(picture)
        if debug:
            print("queueing " + str(picture))
    

def movePics():
    for file in tocopy:
        thispic = os.path.join(sourcedir, file) 
        print("Moving '" + file + "' to '" + originalsPath)
        shutil.move(thispic, originalsPath)

def cleanup():
    global tocopy
    tocopy = []

def main():
    global tocopy
    
    if dir.get() == "":
        tk.messagebox.showerror(title="Originals Photo Sorter", message="Directory cannot be blank")    
        return    
    if not checkPath():
        # checkPath will throw the error, so we simply return in here.
        return
    
    sortPics()
    
    if len(tocopy) != 0:
        movePics()
        infomsg = "Moved " + str(len(tocopy))  + " pictures"
        print(infomsg)
        tk.messagebox.showinfo(title="Originals Photo Sorter", message=infomsg)
        
    else:
        print("No pictures to move.")
        tk.messagebox.showinfo(title="Originals Photo Sorter", message="No pictures to move.")
        
    cleanup()
        

#def guimain():
print("Originals Photo Sorter by Devin Dulude")
root = tk.Tk()
root.title("Originals Photo Sorter")
root.geometry("400x200")
content = tk.Frame(root)
frame = tk.Frame(content, borderwidth=5, relief=tk.RAISED, width=400, height=200)
dirLabel = tk.Label(content, text="Directory of photos")
dir = tk.Entry(content, width=50)
browseBtn = tk.Button(content, text="Browse", command=handleDirectory)
moveBside = tk.IntVar()
bSideBtn = tk.Checkbutton(root, text="Move reverse side photos?", variable=moveBside)
gobtn = tk.Button(content, text="Go", command=main)

content.grid(column=0, row=0)
dirLabel.grid(column=0, row=0)
dir.grid(column=0, row=1, padx=5)
browseBtn.grid(column=1, row=1)
bSideBtn.grid(column=0, row=1, sticky='W')
gobtn.grid(column=1, row=2)
root.mainloop()


#if __name__ == "__main__":
 #   guimain()

