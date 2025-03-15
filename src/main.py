from textnode import *
from htmlnode import *
from markdown_blocks import *
from inline_markdown import extract_title
from pathlib import Path
import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} \n to {dest_path} \n using {template_path}.")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    #print(f"markdown_content ={markdown_content}")
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
    #print(f"template_content ={template_content}")
    html = markdown_to_html_node(markdown_content).to_html()
    #print(f"html ={html}")
    page_title = extract_title(markdown_content)
    filled_template = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html)
    #print(f"filled_template ={filled_template}")
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write the final HTML to the destination file
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(filled_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                generate_page(from_path, template_path, dest_path)

def generate_pages_recursive_bootdev(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def main():
    # path  
    src = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/static/')
    dest = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/public/')
    destination = shutil.copytree(src, dest, dirs_exist_ok=True)  
    # Print path of newly created file  
    print("Destination path:", destination)
    generate_pages_recursive_bootdev("content", "template.html", "public")

if __name__ == "__main__":
    main()