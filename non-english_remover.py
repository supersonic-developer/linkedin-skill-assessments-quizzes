import os
import re
import shutil

class FileModifier:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.subdirs = self.ListSubDirs()

    def delete_non_english_files(self):
        # Iterate through all the subdirectories in the root directory
        for subdir in self.subdirs:
            # Iterate through all files in the subdirectory
            for file_name in os.listdir(subdir):
                file_path = os.path.join(subdir, file_name)
                if os.path.isfile(file_path):
                    # Check if the file is a non-English quiz file
                    if file_name.endswith('.md') and '-quiz-' in file_name:
                        print(f"Deleting non-English file: {file_path}")
                        os.remove(file_path)

    def ListSubDirs(self):
        subdirs = []
        # Iterate through all the subdirectories in the root directory
        for subdir in os.listdir(self.root_dir):
            subdir_path = os.path.join(self.root_dir, subdir)
            if os.path.isdir(subdir_path):
                subdirs.append(subdir_path)
        return subdirs

    def rename_images_and_update_references(self):
        for subdir in self.subdirs:
            images_path = os.path.join(subdir, 'images')
            if os.path.isdir(images_path):
                imageCnt = 0
                # Rename image files
                for image_file in os.listdir(images_path):
                    image_file_path = os.path.join(images_path, image_file)
                    if os.path.isfile(image_file_path):
                        imageCnt += 1
                        new_image_name = f"picture{imageCnt}{os.path.splitext(image_file_path)[1]}"
                        new_image_path = os.path.join(images_path, new_image_name)
                        os.rename(image_file_path, new_image_path)
                        print(f"Renamed {image_file_path} to {new_image_path}")

                        # Update references in markdown files
                        for md_file in os.listdir(subdir):
                            if md_file.endswith('.md'):
                                md_file_path = os.path.join(subdir, md_file)
                                self.update_image_references(md_file_path, image_file, new_image_name)

    def update_image_references(self, md_file_path, old_image_name, new_image_name):
        with open(md_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = re.sub(r'(!\[.*?\]\(images/)'+ old_image_name,
                                r'\1' + new_image_name,
                                content)

        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"Updated references in {md_file_path}: {old_image_name} -> {new_image_name}")

    def RemoveImagesDirs(self):
        try:
            for subdir in self.subdirs:
                imagesDirs = os.path.join(subdir, 'images')
                if os.path.isdir(imagesDirs):
                    shutil.rmtree(imagesDirs)
                    print(f'{imagesDirs} was removed with all its content.')
        except OSError as e:
            print(f"Error:{imagesDirs} : {e.strerror}")

    def RemoveMarkDownFiles(self):
        for subdir in self.subdirs:
            for md_file in os.listdir(subdir):
                if md_file.endswith('.md'):
                    md_file_path = os.path.join(subdir, md_file)
                    os.remove(md_file_path)
                    print(f'{md_file_path} was removed.')


fileModifier = FileModifier()
fileModifier.RemoveMarkDownFiles()