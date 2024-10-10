# resumeio_downloader
Python program to download resume as PDF from Resume.io 


# Setup

1. Create a python virtual environment
    ` virtualenv venv `

2. Activate virtual environment
    ` . venv/bin/activate `

3. Install Requirements
    ` pip install requirments.txt `

# Parameters

1. URL : Resume.io profile URL with ` --url ` parameter.
2. SID : Resume.io security id with ` --sid ` parameter.
3. ` --overwrite ` or ` -y ` to overwrite existing downloded resume.
4. ` --verbose ` to show detailed informations.

# Usage

Run the following python command in shell
    ` python main.py --sid <YOUR RESUME.IO SECURITY ID> --url <RESUME URL> `