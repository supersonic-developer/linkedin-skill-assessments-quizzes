import os
import re
import shutil

class FileModifier:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.sub_dirs = self.list_sub_dirs()

    def delete_non_english_files(self):
        # Iterate through all the subdirectories in the root directory
        for subdir in self.sub_dirs:
            # Iterate through all files in the subdirectory
            for file_name in os.listdir(subdir):
                file_path = os.path.join(subdir, file_name)
                if os.path.isfile(file_path):
                    # Check if the file is a non-English quiz file
                    if file_name.endswith('.md') and '-quiz-' in file_name:
                        print(f"Deleting non-English file: {file_path}")
                        os.remove(file_path)

    def list_sub_dirs(self):
        subdirs = []
        # Iterate through all the subdirectories in the root directory
        for subdir in os.listdir(self.root_dir):
            subdir_path = os.path.join(self.root_dir, subdir)
            if os.path.isdir(subdir_path):
                subdirs.append(subdir_path)
        return subdirs

    def rename_images_and_update_references(self):
        # Regular expression pattern for image references
        pattern = r'!\[.*?\]\((.*?)\)'
        # Iterate through all the subdirectories in the root directory
        for subdir in self.sub_dirs:
            for md_file in os.listdir(subdir):
                # Select only markdown files
                if md_file.endswith('.md'):
                    md_file_path = os.path.join(subdir, md_file)

                    # Read the content of the markdown file
                    with open(md_file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # Find all image references in the markdown file
                    image_refs = re.findall(pattern, content)
                    image_refs = list(dict.fromkeys(image_refs))
                    image_cnt = 0

                    for i, image_ref in enumerate(image_refs):
                        # Check if the image reference refers to a local file
                        image_sub_path = image_ref.split('?')[0]

                        # Check if the image reference refers to a local file
                        image_path = os.path.join(subdir, image_sub_path).replace('/', '\\')
                        if os.path.isfile(image_path):
                            #print(f"Image found for reference {image_ref} at the path: {image_path} in {md_file_path}")
                            image_cnt += 1
                            new_image_name = f"picture{image_cnt}{os.path.splitext(image_path)[1]}"

                            # Rename the image file
                            image_dir_path = os.path.dirname(image_path)
                            new_image_path = os.path.join(image_dir_path, new_image_name)
                            print(f"Renaming image from {image_path} to {new_image_path}")
                            os.rename(image_path, new_image_path)

                            # Update the image reference in the markdown file
                            content = content.replace(image_ref, f'images/{new_image_name}')
                            print(f"Updating image reference from {image_ref} to images/{new_image_name} in {md_file_path}")
                        else:
                            print(f"Image not found for reference {image_ref} at the path: {image_ref} in {md_file_path}")
                    
                    with open(md_file_path, 'w', encoding='utf-8') as file:
                        file.write(content)


    def remove_image_dirs(self):
        try:
            for subdir in self.sub_dirs:
                imagesDirs = os.path.join(subdir, 'images')
                if os.path.isdir(imagesDirs):
                    shutil.rmtree(imagesDirs)
                    print(f'{imagesDirs} was removed with all its content.')
        except OSError as e:
            print(f"Error:{imagesDirs} : {e.strerror}")


    def remove_md_files(self):
        for subdir in self.sub_dirs:
            for md_file in os.listdir(subdir):
                if md_file.endswith('.md'):
                    md_file_path = os.path.join(subdir, md_file)
                    os.remove(md_file_path)
                    print(f'{md_file_path} was removed.')

    def init_for_resources_image_dir_VS(self):
        for sub_content in os.listdir(self.root_dir):
            sub_content_path = os.path.join(self.root_dir, sub_content)
            if not os.path.isdir(sub_content_path) and not sub_content.endswith('.py') and not sub_content.endswith('.git') and not sub_content.endswith('LICENSE'):
                os.remove(sub_content_path)
        self.remove_md_files()

# Delete file after finishing
def delete_self():
    try:
        # Get the absolute path of the script
        script_path = os.path.abspath(__file__)
        # Check if the script is being run as a file
        if os.path.isfile(script_path):
            # Delete the script file
            os.remove(script_path)
            print("Script deleted successfully.")
        else:
            print("Cannot delete script: Not a file.")
    except Exception as e:
        print(f"Error deleting script: {e}")


fileModifier = FileModifier()
fileModifier.rename_images_and_update_references()