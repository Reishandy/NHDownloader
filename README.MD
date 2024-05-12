# NHDownloader

NHDownloader is a Python-based command-line tool that allows you to download doujin from nhentai.net.

## Features

- Download doujin by ID or link.
- Specify the output file name.
- Save the file in .zip or .cbz format.

## Installation

This project requires Python and pip. Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python NHD.py [ID/LINK] [-c] [-o OUTPUT] [-h] [-v]
```
Where: 

- ID/LINK is the id or link of the doujin to be downloaded.
- -c or --cbz to save the file to .cbz format.
- -o OUTPUT or --output OUTPUT to specify the output file name.
- -h to display help information.
- -v to display the version of the program.

## License
[MIT](LICENSE)