import os
import argparse
import re
from PIL import Image
from PIL.ExifTags import TAGS


class PathIsNotDirectory(Exception):
    def __init__(self, message="Path specified is not a directory"):
        super().__init__(message)


description = """
Simple image renamer
Command developed to rename your image files using timestamp information stored in metadata(EXIF) of image.
"""
epilog = """
File name is created based on format specified by user(required). 
Following tags are supported. Tags must be located within \'{}\':
YYYY - Year
MM   - Month
DD   - Day
hh   - Hours
mm   - Minutes
ss   - Seconds

Example: \"{YYYY}-{MM}-{DD}\"
Output: 2021-09-03.jpg
"""

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
import sys


parser.add_argument("-f", dest="format", required=True, type=str, help='format of the new file name')
parser.add_argument("-r", dest="recursive", default=False, action='store_true', help='search images recursively')
parser.add_argument("--dry-run", dest="dry_run", default=False, action='store_true',
                    help='run renamer without changing anything')
parser.add_argument(dest='path', help='Path to folder')
if len(sys.argv) == 1:
    parser.print_help()
args = parser.parse_args()

name_format = args.format
path = args.path
recursive = args.recursive
dry_run = args.dry_run

abs_path = (os.path.abspath(path))

# args for testing purpose (no need to specify arguments in command)
# name_format = "{YYYY}-{MM}-{DD}"
# path = "/mnt/data/GoogleDrive/ProjectsPython/image-renamer/jpg"
# folder_path = (os.path.abspath(path))
# recursive = False

if not os.path.exists(abs_path):
    raise FileNotFoundError("Path not exists")
if not os.path.isdir(abs_path):
    raise PathIsNotDirectory()

skipped_files = list()
processed_files = 0
for subdir, dirs, files in os.walk(abs_path):
    print(f"Processing folder {subdir}")
    for file in files:
        file_path = os.path.join(subdir, file)

        try:
            img = Image.open(file_path)
        except OSError:
            skipped_files.append((file_path, "Not an image file"))
            continue


        exif_data = img._getexif()
        if exif_data is None:
            skipped_files.append((file_path, "No EXIF data found"))
            continue

        exif_dict = {TAGS[k]: v for k, v in exif_data.items() if k in TAGS and type(v) is not bytes}
        # print(exif_dict)
        timestamp = (exif_dict.get('DateTimeOriginal') or exif_dict.get('DateTimeDigitized') or exif_dict.get(
            'DateTime'))

        if timestamp is None:
            skipped_files.append((file_path, "Missing timestamp"))
            continue

        timestamp_dict = re.match(r'(?P<YYYY>\d\d\d?\d?):(?P<MM>\d\d?):(?P<DD>\d\d?)'
                                  r' (?P<hh>\d\d?):(?P<mm>\d\d?):(?P<ss>\d\d?)',
                                  timestamp.strip()).groupdict()


        new_name = (name_format + f".{img.format.lower()}").format(**timestamp_dict).strip()
        print(f"{new_name} <- {file}")
        if not dry_run:
            old_file = os.path.join(subdir, file)
            new_file = os.path.join(subdir, new_name)
            os.rename(old_file, new_file)
        processed_files += 1

    if not recursive:
        break
print(f"List of skipped files: ")
for file, error in skipped_files:
    print(f"{error:15} : {file}")
print("Processed files: {s}{processed_files}".format(s="0/" if dry_run else "", processed_files=processed_files))
print(f"Skipped files: {len(skipped_files)}")
