import os
import re
import shutil
import sys

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
                    # Check if the file is a non-English .md file
                    if file_name.endswith('.md') and not file_name.endswith('-quiz.md'):
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
        for sub_dir in self.sub_dirs:
            for md_file in os.listdir(sub_dir):
                # Select only markdown files
                if md_file.endswith('.md'):
                    md_file_path = os.path.join(sub_dir, md_file)

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
                        image_path = os.path.join(sub_dir, image_sub_path).replace('/', '\\')
                        if os.path.isfile(image_path):
                            #print(f"Image found for reference {image_ref} at the path: {image_path} in {md_file_path}")
                            image_cnt += 1
                            base_dir = os.path.basename(sub_dir).replace('-', '_')
                            new_image_name = f"{base_dir}_{image_cnt:02}{os.path.splitext(image_path)[1]}".lower().replace('+', 'p')
                            new_image_path = os.path.join(sub_dir, new_image_name)

                            # Copy file only if it differs from the original file
                            if not new_image_path == image_path:
                                # Copy the images to the root directory of .md file
                                os.rename(image_path, new_image_path)
                                #shutil.copy2(image_path, new_image_path)
                                print(f"Copied image from {image_path} to {new_image_path}")

                                # Update the image reference in the markdown file
                                content = content.replace(image_ref, f'{new_image_name}')
                                print(f"Updating image reference from {image_ref} to {new_image_name} in {md_file_path}")
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


    def remove_target_files(self, is_md):
        for sub_dir in self.sub_dirs:
            for file in os.listdir(sub_dir):
                file_path = os.path.join(sub_dir, file)
                if (file.endswith('.md') and is_md) or (not file.endswith('.md') and not is_md):
                    os.remove(file_path)
                    print(f'{file_path} was removed.')

    def remove_files_in_root_dir(self):
        for sub_content in os.listdir(self.root_dir):
            sub_content_path = os.path.join(self.root_dir, sub_content)
            if not os.path.isdir(sub_content_path) and not sub_content.endswith('.py') and not sub_content.endswith('.git') and not sub_content.endswith('LICENSE') and not sub_content.endswith('.md'):
                os.remove(sub_content_path)

# Delete file after finishing
# def delete_self():
#     try:
#         # Get the absolute path of the script
#         script_path = os.path.abspath(__file__)
#         # Check if the script is being run as a file
#         if os.path.isfile(script_path):
#             # Delete the script file
#             os.remove(script_path)
#             print("Script deleted successfully.")
#         else:
#             print("Cannot delete script: Not a file.")
#     except Exception as e:
#         print(f"Error deleting script: {e}")

# Main function

# Instantiate the FileModifier class
fileModifier = FileModifier()

if len(sys.argv) < 2:
    fileModifier.rename_images_and_update_references()
    print("No argument provided. Please read README.md for more information.")
    sys.exit()

# Initialize the git repository as raw resource (.md files are included)
if sys.argv[1].lower() in ['true', '1', 't', 'y', 'yes']:
    fileModifier.delete_non_english_files()
    fileModifier.remove_image_dirs()
    fileModifier.remove_target_files(False)
# Initialize the git repository as image resource (image files are included)
elif sys.argv[1].lower() in ['false', '0', 'f', 'n', 'no']:
    fileModifier.remove_target_files(True)
    fileModifier.remove_files_in_root_dir()