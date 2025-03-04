from PIL import Image, ImageOps
import glob, os
import pandas
import piexif


# colors to help errors stand out

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_orientation(image_path):
    exif_dict = piexif.load(image_path)
    orientation = exif_dict["0th"][piexif.ImageIFD.Orientation]
    return orientation


def image_fixer(extensions=['png', 'jpg', 'jpeg']):

    # get the database

    db = pandas.read_csv('data/champion_data.csv')
    
    # iterate through all the types

    for extension in extensions:

        # iterate through all the files in each type
        
        for infile in glob.glob(f"uploads/photos/champions/*.{extension}"):

            print("Fixing " + infile)

            file, ext = os.path.splitext(infile)

            im = Image.open(infile)

            #orientation = get_orientation(infile)

            #print(orientation)

            im = ImageOps.exif_transpose(im)

            im.save(file + ".webp", "webp")

            # delete the old file
            os.remove(infile)

            print(bcolors.OKBLUE + "Fixed " + infile + " to " + file + ".webp" + bcolors.ENDC)


        # iterate through db images and replace the extension with .webp
        for index, row in db.iterrows():
            src = row['image']

            if src.endswith(extension):

                db.at[index, 'image'] = src.replace(extension, 'webp')

                print(bcolors.OKGREEN + "Fixed " + src + " to " + src.replace(extension, 'webp') + bcolors.ENDC)


    # save the database
    db.to_csv('data/champion_data.csv', index=False)

    print(bcolors.OKGREEN + "Done!" + bcolors.ENDC)


image_fixer(['png', 'jpg', 'jpeg'])

# manual rotate images