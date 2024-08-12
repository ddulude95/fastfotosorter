#Author: Devin Dulude
#Version: 1.3
#About: Python program created to use specifically with Fastfoto software to move
# the non-enhanced versions of your scanned photos to their own folder if you chose to keep them.
# This way you don't have duplicates in the folder when viewing the photos. Also can batch rename photos.

import tkinter as tk
import os, sys, shutil
from tkinter.filedialog import askdirectory
#tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
sourcedir = ""
TITLE = "Originals Photo Sorter"
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
def checkPath(checkOrig: bool):
    global originalsPath, sourcedir
    sourcedir = dir.get()

    if not(os.path.exists(sourcedir)):
        print("Invalid path entered. Path does not exist")
        tk.messagebox.showerror(title="Originals Photo Sorter", message="Invalid file path. Path does not exist.")
        return False

    if checkOrig:
        originalsPath = sourcedir + "/Originals"
        if str(sourcedir).endswith((r'/Originals', r'/Originals/')):
            print("Source folder IS 'Originals'. Source folder cannot be an 'Originals' folder")
            tk.messagebox.showerror(title="Originals Photo Sorter", message="Source folder cannot be 'Originals'.")
            return False            

        if not (os.path.exists(originalsPath)):
            print("Folder 'Originals' not found...creating")

            try:
                os.mkdir(originalsPath)
            except OSError as error:
                print(error)
                print("Couldn't create folder 'Originals', no action has been taken.")
                return False
            return True # If we got here, it was successful in creating the folder            
        else:
            if debug:
                print("Originals folder already exists, continuing")
            return True
        
    else:
        return True

# makes sure to only handle .jpg files and adds originalsPath to a tocopy list.
def sortPics(rename: bool):
    jpgs = []
    global tocopy
    numChanges = 0

    # grab only jpgs
    for file in os.listdir(sourcedir):
        if str(file).lower().endswith('.jpg'):
            jpgs.append(file)

    if rename:
        for picture in jpgs:
            old_name = str(picture)
            if whatfield.get() in old_name:
                new_name = old_name.replace(whatfield.get(), withfield.get())
                os.rename( (os.path.join(sourcedir, old_name)), (os.path.join(sourcedir, new_name)) )
                numChanges += 1

    else:
        # go through jpgs and filter out which to move
        for picture in jpgs:
            if (str(picture).endswith('_a.jpg')):
                continue # we never move anything that ends with _a, so we continue 

            if moveBside.get() == 0 and str(picture).endswith('_b.jpg'): # if not moving B side & ends with _b, dont add to queue and continue
                continue

            # finally, add this pic to queue
            tocopy.append(picture)
            numChanges += 1
            if debug:
                print("queueing " + str(picture))

    return numChanges
    

def movePics():
    for file in tocopy:
        thispic = os.path.join(sourcedir, file) 
        print("Moving '" + file + "' to '" + originalsPath)
        shutil.move(thispic, originalsPath)

def cleanup():
    global tocopy
    tocopy = []

def startRename():
    if not checkPath(False):
        # checkPath will throw the error, so we simply return in here.
        return
    
    if whatfield.get() == "":
        tk.messagebox.showerror(title=TITLE, message="'Replace what' field cant be blank!")
        return
    
    if withfield.get() == "":
        okay = tk.messagebox.askokcancel(title=TITLE, message="'Replace with' field is empty. This will erase " + str(whatfield.get()) + " from the filename. This cannot be undone.\n\nContinue?")
        if not okay:
            return

    numRenamed = sortPics(True)

    if numRenamed != 0:
        infomsg = "Renamed " + str(numRenamed)  + " pictures"
        print(infomsg)
        tk.messagebox.showinfo(title=TITLE, message=infomsg)
        
    else:
        print("No pictures to rename.")
        tk.messagebox.showinfo(title=TITLE, message="No pictures to rename.")

def startMove():
    if not checkPath(True):
        # checkPath will throw the error, so we simply return in here.
        return
    
    count = sortPics(False)
    
    if count != 0:
        movePics()
        infomsg = "Moved " + str(count)  + " pictures"
        print(infomsg)
        tk.messagebox.showinfo(title=TITLE, message=infomsg)
        
    else:
        print("No pictures to move.")
        tk.messagebox.showinfo(title=TITLE, message="No pictures to move.")
        
    cleanup()

def main(action):
    if dir.get() == "":
        tk.messagebox.showerror(title=TITLE, message="Directory cannot be blank")    
        return

    match action:
        case 1:
            startMove()
        case 2:
            startRename()
            
        

#def guimain():
print("Originals Photo Sorter by Devin Dulude")
root = tk.Tk()
root.title(TITLE)
root.geometry("400x200")
content = tk.Frame(root)
frame = tk.Frame(content, borderwidth=5, relief=tk.RAISED, width=400, height=200)


dirLabel = tk.Label(content, text="Directory of photos")
dir = tk.Entry(content, width=50)
whatlabel = tk.Label(content, text="Replace what")
whatfield = tk.Entry(content, width=40)
withlabel = tk.Label(content, text="Replace with")
withfield = tk.Entry(content, width=40)


browseBtn = tk.Button(content, text="Browse", command=handleDirectory)
moveBside = tk.IntVar()
bSideBtn = tk.Checkbutton(root, text="Move reverse side photos?", variable=moveBside)
gobtn = tk.Button(content, text="Move", command=lambda: main(1))
renamebtn = tk.Button(content, text="Rename", command=lambda: main(2))

content.grid(column=0, row=0)
dirLabel.grid(column=0, row=0)
dir.grid(column=0, row=1, padx=5)
whatlabel.grid(column=0, row=3)
whatfield.grid(column=0, row=4)
withlabel.grid(column=0, row=5)
withfield.grid(column=0, row=6)

browseBtn.grid(column=1, row=1)
bSideBtn.grid(column=0, row=1, sticky='W')
gobtn.grid(column=1, row=6)
renamebtn.grid(column=0, row=7)

root.mainloop()


#if __name__ == "__main__":
 #   guimain()

