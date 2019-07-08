########################################################################
##
## CS 101
## Program #6
## Name: Harrison Lara
## Email: hrlwwd@mail.umkc.edu
##
## PROBLEM :
##
## You’ll be given directories that have 2 file formats.  You are required to
## implement a solution that reads the text based PPM files.  Since they are text
## files you can open with them with the python open function just like any text
## file.  The directories will also have jpg files.  Using the jpg files will be
## extra credit.  The program you write will ask the user for a directory, if
## the files in that directory are valid image files then you will sort them by
## their names and create a new image with slices of the other images.  The
## number of images in each directory will not be constant.  If there are 10
## source images, then your output image will take 1/10 of a horizontal slice
## from the input images. 
##
## ALGORITHM :
##
##  • Imports
##      o Os
##      o Glob
##      o Image
## • Set variables
##      o   Empty list
## • Greeting
##      o ‘Welcome to the image slicer.  You can provide a directory that has several images of the same size, and this program will take equal vertical slices out of each and construct a new image.’
## • Set master loop
## • Functions
## • Ask for which directory needs to be opened (get input)
##      o ‘Enter a directory that contains valid image files’
##           Try and except
##           Use ‘r’ to read file, encoding = utf-8
## • Set path to variable, use glob and os to open only .ppm files
## • Prompt user for output file and use ‘w’ to write to directory, add on ‘.ppm’, include to check for the correct resolution for each picture
##      o Try/except 
## • Check for valid header (first line P3, second line 225)
## • Overlap from green to blue to red to black , 100 – 75 – 50 – 25, instead of slicing each 25% 
## • Create a list to store each red, green and blue value
##      o Make sub lists if needed to hold all the values taken
## • Or keep all of the color values in a dictionary
##      o Key: tuple
##           Y, x, color
## • Or list of tuple with row/ column to index
##      o Index = row*total_columns + col
## • Load each file at separate times
##      o Loading all at once can create issues
##      o Each open file handle should be put into its own list
## • Use sort method to order all the picture file names into order the order process of each image is taken in. 
## • Check progress of image slicing in Gimp2 (install gimp2 before the start of the program)
## • Close all files that have been opened
##      o .close() method
## • Exit/close program
## • Extra Credit:
##      o Ask user for input: 
##           Slice a PPM file. 
##           Slice a Jpg Image 
##           Quit
##      o Try and except for correct/ wrong input till 1,2,3 is chosen as their file choice or to exit. 
## 
## ERROR HANDLING:
##     IOError, TypeError
##
## OTHER COMMENTS:
##      None
##
########################################################################

# Imports
import os
import glob

# Set variables
dom_list = []
file_list = []
empty = []

# Create master loop
create = True
while create:

    # Greeting
    print(
        'Welcome to the image slicer. You can provide a directory that has several images of the same size, and this program will take equal slices out of each and construct a new image.')

    # Ask for input directory
    while True:
        try:
            input_file = input("Please enter the directory you want to get the files from:")
            for filename in sorted(glob.glob(os.path.join('*.ppm'))):
                file_obj = open(filename, "r", encoding="utf-8")
                empty.append(file_obj)
            break
        except IOError:
            print('Please enter a valid directory.')
        except TypeError:
            print('Please enter a valid directory.')

    # Set list to get colors
    for file in empty:
        for value in file:
            file_list.append(str(value.rstrip()))
        dom_list.append(file_list)

    # Ask for output file
    while True:
        try:
            output_file = input('Please enter location for image: ')
            for outName in (glob.glob(os.path.join('*.ppm'))):
                file_object = open(outName, "w", encoding="utf-8")
            break
        except TypeError:
            print('Please enter a valid location.')
        except IOError:
            print('Please enter a valid location.')

    # Take resolution of the three colors and place into the dominant list then split them
    res_list = str(dom_list[1]).split(' ')
    res = int(int((int(res_list[0]) * int(res_list[1])) * 3))
    num_files = int(len(file_list))
    header = dom_list[0][0:3]
    strip_cnt = 0

    # tell user what is happening and take item from the header for output file
    for item in header:
        print((item + '\n'), file=file_object)
    print('Writing pixels to file')

    for number in range(0, len(dom_list)):
        strip_cnt += 1
        if strip_cnt == 1:
            strip = (dom_list[number][3:(int(res / num_files) + 3)])
            for item in strip:
                print((item + '\n'), file=file_object)

        elif strip_cnt >= 2:
            strip = dom_list[number][(int(res / num_files) * (strip_cnt - 1)):((int(res / num_files)) * strip_cnt)]
            for item in strip:
                print((item + '\n'), file=file_object)

    for item in file_list:
        item.close()
    file_object.close()
