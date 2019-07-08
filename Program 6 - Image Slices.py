
import os
try:
    from PIL import Image
    pil_failed = False
except ImportError:
    pil_failed = True

if pil_failed:
    MENU = """    Image Slicer

    Welcome to the image slicer.  You can provide a directory that has several images
    of the same size, and this program will take equal vertical slices out of each
    and construct a new image.

    1. Slice a PPM file.
    Q. Quit

    ==> """
    MENU_CHOICES = ["1", "Q"]
else:
    MENU = """    Image Slicer

    Welcome to the image slicer.  You can provide a directory that has several images
    of the same size, and this program will take equal vertical slices out of each
    and construct a new image.

    1. Slice a PPM file.
    2. Slice a jpg Image
    3. Quit

    ==> """
    MENU_CHOICES = ["1", "2", "3"]
    
DIRECTORY_PROMPT = "\nEnter a directory that contains valid image files ==> "
OUTPUT_PROMPT = "\nEnter the file to save the ppm to. ==> "
OUTPUT_JPG_PROMPT = "\nEnter the file to save the jpg to. ==> "


def get_directory(prompt : str) -> str:
    """ Prompts the user to enter a valid directory and only returns if it is given a valid one """

    while True:
        directory = input(prompt)
        if os.path.isdir(directory):
            return directory
        print("{} is not a valid directory.  Please enter a valid directory ".format(directory))


def get_option(prompt : str, choices : iter) -> str:
    """ Prompts the users and only allows the user to return when they've chosen one of the valid choices supplied """

    # upper case all the choices
    upper_choices = [item.upper() for item in choices]
    while True:
        choice = input(prompt).upper()
        if choice in upper_choices:
            return choice
        print("You must enter one of the following {}".format(",".join(choices)))


def get_file(directory : str, file : str) -> dict:
    """ Returns a dictionary of the file information. """

    try:
    
        open_file = open(os.path.join(directory, file))
        file_lst = [line.strip() for line in open_file.readlines()]
        open_file.close()

        file_dict = {}
        file_dict["type"] = file_lst[0]
        file_dict["resolution"] = file_lst[1]
        file_dict["width"] = int(file_lst[1].split(" ")[0])
        file_dict["height"] = int(file_lst[1].split(" ")[1])
        file_dict["bitdepth"] = file_lst[2]
        file_dict["pixels"] = [(file_lst[pixel_index], file_lst[pixel_index + 1], file_lst[pixel_index + 2]) for pixel_index in range(3, len(file_lst), 3)]

        return file_dict

    except IOError:
        print("Could not open the file {} at {}".format(file, source_directory))


def load_files(source_directory : str) -> dict:
    """ Gets the ppm files from the source directory and loads them into a dictionary """
    files = {}

    # loop through files in the source directory
    for file in os.listdir(source_directory):
        if file.lower().endswith(".ppm"):
                file_struct = get_file(source_directory, file)
                files[file] = file_struct
    return files


def valid_ppms(files : dict) -> bool:
    """ Checks if the ppm files are valid.  If not then it will return false, otherwise True """

    file_lst = list(files.keys())

    # Use the files file in the file list as the one to compare all others against.
    # If any of the values aren't equal, then they can't be used.
    errors = []
    compare_file = file_lst[0]

    # Test if there is enough pixels for the resolution.
    for name, file in files.items():
        if len(file["pixels"]) != file["width"] * file["height"]:
            errors.append("{} does not have correct number of pixels, {}x{} != {} pixels".format(name, file["width"], file["height"], len(file["pixels"])))
        if file["type"].upper() != "P3":
            errors.append("{} does not have PPM as its first line".format(name))
        if file["bitdepth"] != "255":
            errors.append("{} does not have 255 as its bit depth".format(name))

    # Check width of all the files.        
    for other_file in file_lst[1:]:
        if files[other_file]["width"] != files[compare_file]["width"]:
            errors.append("{} does not have the same width as {}".format(other_file, compare_file))
        if files[other_file]["height"] != files[compare_file]["height"]:
            errors.append("{} does not have the same height as {}".format(other_file, compare_file))

    if len(errors) == 0:
        return True
    else:
        print("\n".join(errors))
        return False

def get_output_file(prompt : str):
    """ Ask the user for file to output the image to. """
    while True:
        try:
            file_name = input(prompt)
            file = open(file_name, "w")
            return file
        except IOError:
            print("Could not open the file {} for write access.  Please try another ".format(file_name))


def get_index_from_rowcol(row : int, col : int, width : int) -> int:
    """ Given a row and column and the width of the image we can get the index """
    return row * width + col


def create_output_ppm(source_images : dict) -> dict:
    """ Writes out the ppm file. """

    files = sorted([name for name in source_images.keys()], key=lambda item: item.upper())

    # Create the output result dictionary file 
    result = {}
    result["type"] = source_images[files[0]]["type"]
    result["resolution"] = source_images[files[0]]["resolution"]
    result["width"] = source_images[files[0]]["width"]
    result["height"] = source_images[files[0]]["height"]
    result["bitdepth"] = source_images[files[0]]["bitdepth"]
    result["pixels"] = []

    slices = len(files)
    # loop through all the pixels and create the output image
    for y in range(result["height"]):
        for x in range(result["width"]):
            # Get the red green and blue value for the current pixel
            image = int(x / result["width"] * slices)     # which image index to use for result

            pixel_index = get_index_from_rowcol(y, x, result["width"])
            pixel = source_images[files[image]]["pixels"][pixel_index]
            result["pixels"].append(pixel)

    return result


def write_ppm(output_ppm, output_dict : dict):
    """ takes the output dict and writes it to the output file """

    print(output_dict["type"], file=output_ppm)
    print(output_dict["resolution"], file=output_ppm)
    print(output_dict["bitdepth"], file=output_ppm)

    for pixels in output_dict["pixels"]:
        print(pixels[0], file=output_ppm)
        print(pixels[1], file=output_ppm)
        print(pixels[2], file=output_ppm)

def slice_ppms():
    """ Asks for input and stitches slices of images into a result. """

    valid_images = False
    while not valid_images:
        directory = get_directory(DIRECTORY_PROMPT)

        files = load_files(directory)                 # Load files
        valid_images = valid_ppms(files)

    output_dict = create_output_ppm(files)

    output_ppm = get_output_file(OUTPUT_PROMPT)
    write_ppm(output_ppm, output_dict)
    output_ppm.close()


def load_jpg_files(source_directory : str) -> dict:
    """ Gets the ppm files from the source directory and loads them into a dictionary """
    files = {}

    # loop through files in the source directory
    for file in os.listdir(source_directory):
        if file.lower().endswith(".jpg"):
                path_file = os.path.join(source_directory, file)
                try:
                    files[file] = Image.open(path_file)
                except FileNotFoundError:
                    print("{} could not be found to load".format(os.join(source_directory, file)))
                except IOError:
                    print("{} could not be loaded due to an IO Error".format(os.join(source_directory, file)))
                    
    return files


def validate_jpgs(images : dict) -> bool:
    """ Returns True if all the images have the same size """

    errors = []
    files = list(images.keys())
    first_file = files[0]

    for file in files[1:]:
        if images[file].size != images[first_file].size:
            errors.append("{} and {} are not the same sizes, {} vs {}".format(file, first_file, images[file].size, images[first_file].size))

    if len(errors) == 0:
        return True
    else:
        print("Many of the files were inconsistent in size.")
        print("All jpgs in the directory must be the same size}")
        print("\n".join(errors))
        return False


def create_output_jpg(images : dict):
    """ Go through the images and create a new image with the slices """

    files = sorted([name for name in images.keys()], key=lambda item: item.upper())
    slices = len(files)

    new_image = Image.new(images[files[0]].mode, images[files[0]].size)

    for y in range(images[files[0]].size[1]):
        for x in range(images[files[0]].size[0]):

            image_idx = int(x / images[files[0]].size[0] * slices)     # which image index to use for result
            new_image.putpixel((x,y), images[files[image_idx]].getpixel((x,y)))

    return new_image


def slice_jpgs():
    """ Asks for a directory of images and creates a new image of slices of the original """
    valid_images = False
    while not valid_images:
        directory = get_directory(DIRECTORY_PROMPT)
        images = load_jpg_files(directory)

        valid_images = validate_jpgs(images)        

    out_img = create_output_jpg(images)

    while True:
        try:
            output_filename = input(OUTPUT_JPG_PROMPT)
            out_img.save(output_filename)
            break
        except IOError:
            print("Could not save to file {}, choose another name".format(output_filename))
            

playing = True
while playing:

    # Get the users choice
    choice = get_option(MENU, MENU_CHOICES)

    if   choice == "1":             # Convert PPM
        slice_ppms()
    elif choice == "2":             # Convert JPG
        slice_jpgs()
    else:                           # Exit the program
        playing = False
