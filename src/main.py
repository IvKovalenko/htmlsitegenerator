from textnode import *
from htmlnode import *
from markdown_blocks import *
from inline_markdown import extract_title
from pathlib import Path
import os
import shutil
import sys

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} \n to {dest_path} \n using {template_path}.")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
    html = markdown_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)
    filled_template = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html)
    # Replace href and src with basepath
    filled_template = filled_template.replace('href="/', f'href="{basepath}/').replace('src="/', f'src="{basepath}/')
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write the final HTML to the destination file
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(filled_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                generate_page(from_path, template_path, dest_path, basepath)

def generate_pages_recursive_bootdev(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    print(f"Base path: {basepath}")
    # path  
    src = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/static/')
    #dest = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/public/')
    dest = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/docs/')
    destination = shutil.copytree(src, dest, dirs_exist_ok=True)  
    # Print path of newly created file  
    print("Destination path:", destination)
    #generate_pages_recursive_bootdev("content", "template.html", "public", basepath)
    generate_pages_recursive_bootdev("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()