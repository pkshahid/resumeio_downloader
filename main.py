import argparse
import os
import requests
import time
import json
from fpdf import FPDF

# Constants
VERSION = "1.0"
NAME_OF_PROGRAM = "resumeio2pdf"
COPYRIGHT = "Copyright (c) 2021, Leonid Sopov <leonid@sopov.org>"
COPY_URL = "https://github.com/sopov/resumeio2pdf/"

RESUME_PAGE = "https://resume.io/r/{}"
RESUME_META = "https://ssr.resume.tools/meta/ssid-{}?cache={}"
RESUME_IMG = "https://ssr.resume.tools/to-image/ssid-{}-{}.{}?cache={}&size={}"
RESUME_SIZE = 1800
TIMEOUT = 60  # 60 seconds timeout

# Command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Resume.io resume to PDF.")
    parser.add_argument("--url", type=str, help="Link to resume of the format: https://resume.io/r/SecureID")
    parser.add_argument("--sid", type=str, help="SecureID of the resume")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--verbose", action="store_true", help="Show detailed information")
    parser.add_argument("-y", "--overwrite", action="store_true", help="Overwrite existing PDF if it exists")
    return parser.parse_args()

# Function to fetch metadata
def fetch_resume_metadata(sid):
    cache_time = str(int(time.time()))
    url = RESUME_META.format(sid, cache_time)
    response = requests.get(url, timeout=TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata: {response.status_code}")
    return response.json()

# Function to generate a PDF from images
def generate_pdf(image_urls, output_filename, overwrite=False):
    if os.path.exists(output_filename) and not overwrite:
        print(f"{output_filename} already exists. Use --overwrite to replace.")
        return
    
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for idx, image_url in enumerate(image_urls):
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save image temporarily
            img_filename = f"temp_image_{idx}.png"
            with open(img_filename, "wb") as img_file:
                img_file.write(response.content)
            
            # Add image to PDF
            pdf.add_page()
            pdf.image(img_filename, x=10, y=10, w=190)  # Adjust size and position as needed
            
            # Clean up
            os.remove(img_filename)
        else:
            print(f"Failed to fetch image {idx}: {response.status_code}")
    
    pdf.output(output_filename)
    print(f"PDF saved as {output_filename}")

# Main program logic
def main():
    args = parse_arguments()
    
    if args.version:
        print(f"{NAME_OF_PROGRAM} version {VERSION}")
        return
    
    if not args.url or not args.sid:
        print("Error: Both --url and --sid are required.")
        return
    
    try:
        metadata = fetch_resume_metadata(args.sid)
        if args.verbose:
            print(f"Fetched resume metadata: {json.dumps(metadata, indent=2)}")
        
        # Assuming there are 2 images for demonstration
        image_urls = [
            RESUME_IMG.format(args.sid, 1, "png", str(int(time.time())), RESUME_SIZE),
            RESUME_IMG.format(args.sid, 2, "png", str(int(time.time())), RESUME_SIZE)
        ]
        
        generate_pdf(image_urls, "output_resume.pdf", args.overwrite)
    
    except Exception as e:
        print(f"Error: {str(e)}")

# Entry point
if __name__ == "__main__":
    main()
