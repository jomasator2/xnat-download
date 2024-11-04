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

The `xnat_downloader` CLI allows users to download imaging data from an XNAT (eXtensible Neuroimaging Archive Toolkit) server efficiently. This tool requires the XNAT server URL, a username, and the output directory to store downloaded data.

```bash
python3 -m xnat_downloader -o DIR_TO_SAVE -w XNAT_WEB -u USER
```

### Parameters

- **`-o, --output DIR_TO_SAVE`**  
  Specify the directory where the data will be saved. This path should be writable and have sufficient storage space for the downloaded files.
  
- **`-w, --web XNAT_WEB`**  
  URL of the XNAT server from which the data will be downloaded. This URL is generally in the form of `https://xnat.example.com`.
  
- **`-u, --user USER`**  
  The username for authentication on the XNAT server. This user should have the necessary permissions to access the data.

### Example

To download data from an XNAT server at `https://xnat.example.com`, using the username `myusername`, and save the data in the `data_downloads` directory, you would run:

```bash
python3 -m xnat_downloader -o data_downloads -w https://xnat.example.com -u myusername
```

### Additional Information

- **Authentication**: The script may prompt for a password after execution if the server requires it. Ensure the user account has the correct access permissions.
- **Output Directory**: Ensure the directory has enough storage for potentially large datasets, as neuroimaging data can be quite large.
- **Network Requirements**: A stable internet connection is recommended, as disconnections could interrupt large downloads.

### Troubleshooting

- **Permission Denied Error**: Ensure the specified output directory is accessible and that the user has write permissions.
- **Connection Timeout**: Check the URL of the XNAT server and ensure there is internet access.

## During Execution

Upon running the program, it will prompt you to enter the XNAT username (if not provided as an argument) and the password for that account:

```plaintext
user: lenna
password:
```

After login, the program will display a list of available projects, each associated with a unique number. Select the projects you want to download by entering the corresponding numbers separated by spaces. For example:

```plaintext
1) p0012023    2) p0022021    3) p0022022    4) p0022023    5) p0032021
6) p0032023    7) p0042021    8) p0052021    9) p0052022    10) p0062021

Choose the project(s): 1 3 4
```

This example will download projects `p0012023`, `p0022022`, and `p0022023`.

---

## Contributing

To contribute to the project, follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new feature branch** for your changes:
   ```bash
   git checkout -b feature/yourFeatureName
   ```
3. **Commit your changes** with a clear message:
   ```bash
   git commit -am "Add feature description"
   ```
4. **Push your branch** to GitHub:
   ```bash
   git push origin feature/yourFeatureName
   ```
5. **Create a Pull Request** through GitHub's interface, detailing the improvements or features added.

This process will initiate a review and, once approved, your changes will be merged into the main branch.
