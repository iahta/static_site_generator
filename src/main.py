from textnode import TextNode
from extract_title import generate_page
import os
import shutil

def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
 
    os.mkdir(dest_dir)
    
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_static(source_path, dest_path)




if __name__ == "__main__":
    main()



"""def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)"""