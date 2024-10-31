# XNAT Downloader
## Overview
The **XNAT Downloader** is a command-line tool designed for efficiently downloading project data from **XNAT** (eXtensible Neuroimaging Archive Toolkit) using REST API requests. XNAT is a widely used open-source platform for managing, sharing, and analyzing neuroimaging and related medical imaging data. This tool leverages XNAT's RESTful API to automate and simplify the download process, making it ideal for users who need to handle large datasets and access data programmatically.

### Key Features:
1. **Command-Line Interface (CLI)**: Operates entirely from the command line, enabling quick integration into scripts and pipelines. Users can specify project details and customize download settings directly from the CLI.

2. **REST API Integration**: The tool uses XNAT's REST API endpoints to authenticate, query, and retrieve project data. This allows for flexible and secure interaction with XNAT servers.

3. **Customizable Download Options**:
   - **Selective Data Download**: Users can specify which elements of a project to download, such as specific scans, sessions, or metadata, minimizing unnecessary data transfer.
   - **Download Filters**: Filters can be applied based on project attributes or scan types, allowing the user to focus on relevant datasets.
   - **Folder Structure Preservation**: The tool recreates the original project structure on the local machine, organizing files and directories in a way that mirrors XNAT’s organization.

4. **Efficient Data Transfer**:
   - **Parallel Downloading**: The tool often supports parallel or batch downloading to improve download speeds, particularly with large datasets.
   - **Resume Capability**: In cases of interrupted downloads, the tool can resume from where it left off, enhancing robustness for unstable connections.

5. **Authentication and Security**:
   - The XNAT Downloader supports secure login using API keys or credentials, keeping user data safe.
   - It maintains compatibility with various authentication methods configured on the XNAT server, such as OAuth or single sign-on (SSO).

## Installation

```bash
python3 -m pip install git+https://github.com/BIMCV-CSUSP/xnat-download.git#egg=xnat_downloader
```

## Usage

An example of execution is:

```bash
python3 -m xnat_downloader -o DIR_TO_SAVE -w XNAT_WEB -u USER
```
### Command Options

1. **`-o DIR_TO_SAVE`** (Output Directory):
   - Specifies the directory where the downloaded data will be saved.
   - `DIR_TO_SAVE` is a path to the local directory in which you want to store the files downloaded from XNAT.
   - Example: `-o /path/to/local/directory`

2. **`-w XNAT_WEB`** (XNAT Web URL):
   - Indicates the URL of the XNAT server from which the data will be downloaded.
   - `XNAT_WEB` is the base URL of the XNAT instance (e.g., `https://central.xnat.org`).
   - Example: `-w https://xnat.example.com`

3. **`-u USER`** (Username):
   - Specifies the username for authentication on the XNAT server.
   - `USER` should be a valid XNAT account with permission to access the projects and data you wish to download.
   - After entering this command, the tool may prompt you to enter the password or an API token for secure authentication.

### Full Command Example
Here’s an example of how to use the command to download data:

```bash
python3 -m xnat_downloader -o /path/to/save/data -w https://xnat.example.com -u myusername
```

This command will:
1. Access the XNAT server at `https://xnat.example.com` using the provided username (`myusername`).
2. Download the specified data to `/path/to/save/data` on your local system.

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
