from textnode import TextNode, TextType
from helper import markdown_to_html_node
import shutil
import os

def copy_directory(source, destination):
    # print(f"source={source}")
    # print(f"destination={destination}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    paths = os.listdir(source)
    # print(paths)
    for path in paths:
        src_path = os.path.join(source, path)
        dest_path = os.path.join(destination, path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_directory(src_path, dest_path)
    return

def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        line = line.strip()
        if "# " in line[:2]:
            return line[2:]
        else:
            raise Exception()
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_data = f.read()
    with open(template_path) as f:
        template_path_data = f.read()
    html_string = markdown_to_html_node(from_path_data).to_html()
    title = extract_title(from_path_data)
    dest_path_data = template_path_data.replace("{{ Title }}", title)
    dest_path_data = dest_path_data.replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(dest_path_data)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for dir in dir_list:
        if dir[-3:] == ".md":
            dest_file = dir[:-3] + ".html"
            generate_page(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, dest_file))
        else:
            generate_pages_recursive(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, dir))
    return

def main():
    copy_directory("./static", "./public")
    generate_pages_recursive("./content/", "./template.html", "./public/")


main()
