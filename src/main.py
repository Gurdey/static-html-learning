from textnode import *
from functions import clear_public_directory, copy_static_to_public, generate_pages_recursive

def main():
    clear_public_directory()
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")


main()
