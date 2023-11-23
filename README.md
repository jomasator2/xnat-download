# XNAT Downloader

This software allows the user to download one project from XNAT platform (version XNAT >= 1.7.4.1). The aplication execution need Python version >= 3.8.

## Installation

```bash
python3 -m pip install git+https://github.com/BIMCV-CSUSP/xnat-download.git#egg=xnat_downloader
```

or

```bash
git clone https://github.com/BIMCV-CSUSP/xnat-download.git
cd xnat-download
pip install -e .
```

## Usage

An example of execution is:

```bash
python3 -m xnat_downloader -o DIR_TO_SAVE -w XNAT_WEB -u USER
```

or

```bash
xnat_downloader -o DIR_TO_SAVE -w XNAT_WEB -u USER
```

## During Execution

When we execute the program, it will ask for the XNAT user (if it was not set as an argument) and the password of that user.

Then, the program will ask us which projects we want to download, just enter the numbers associated with the projects separated with space.

    user: lenna
    password:

    1) p0012023         2) p0022021         3) p0022022         4) p0022023         5) p0032021         
    6) p0032023         7) p0042021         8) p0052021         9) p0052022         10) p0062021         
     
    Choose the project: 1 3 4 

## Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
