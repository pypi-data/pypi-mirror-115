# image-renamer
Command developed to rename your image files using timestamp information stored in metadata(EXIF) of image.

## Installation

### Using pip manager

    pip install image-renamer

### Manually
    
    git clone <github-link>
    cd <repository>
    python3 setup.py install

## Usage
```
Simple image renamer
Command developed to rename your image files using timestamp information stored in metadata(EXIF) of image.

positional arguments:
  path        Path to folder

optional arguments:
  -h, --help  show this help message and exit
  -f FORMAT   format of the new file name
  -r          search images recursively
  --dry-run   run renamer without changing anything

File name is created based on format specified by user(required). 
Following tags are supported. Tags must be located within '{}':
YYYY - Year
MM   - Month
DD   - Day
hh   - Hours
mm   - Minutes
ss   - Seconds

Example: "{YYYY}-{MM}-{DD}"
Output: 2021-09-03.jpg
```