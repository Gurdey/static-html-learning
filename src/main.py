from textnode import *
import sys
from functions import clear_public_directory, copy_static_to_public, generate_pages_recursive

def main():
    dest_path = "public"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        dest_path = "docs"
    clear_public_directory(dest_path)
    copy_static_to_public(target_dir= dest_path)
    generate_pages_recursive("content", "template.html", dest_path, basepath)

main()
