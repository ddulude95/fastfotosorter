# Fastfoto Sorter
GUI python script to move original photos from enhanced ones - used with Epson Fastfoto.
![Fastfoto sorter gui](./fastfotosorter.png?raw=true "FastFotoSorter")

# How to use
Only written to work with Windows. Make sure you have Python 3 installed, download picturemovergui.py and double click it. Click browse to browse to your directory of photos, or paste in a directory. Choose to move reverse sides of photos or not. Press Go. The command prompt will display console output. 

# How it works
Fastfoto can generate enhanced versions of your photos as well as scan the back sides. These files get appened a suffix with _a and _b respectively. This program, given a directory of .jpgs, will automatically move the original copies to their own folder called "Originals" and the user can choose to move the B sides or not.
