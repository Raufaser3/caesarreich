import os
import re
import shutil

# Function to get the 3-letter prefix (TAG) from the filename
def get_tag(filename):
    match = re.match(r'^([A-Z]{3})_', filename)
    if match:
        return match.group(1)
    return None

# Function to move files to TAG folders
def move_files(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            tag = get_tag(filename)
            if tag:
                tag_folder = os.path.join(directory, '..', tag)  # Move files one level up
                if not os.path.exists(tag_folder):
                    os.makedirs(tag_folder)
                shutil.move(os.path.join(directory, filename), os.path.join(tag_folder, filename))

# Function to update texture file paths in FX_ideas.gfx
def update_texture_paths(gfx_file, directory):
    with open(gfx_file, 'r') as file:
        data = file.readlines()

    for i in range(len(data)):
        if 'texturefile =' in data[i]:
            original_path = re.search(r'"([^"]*)"', data[i]).group(1)
            tag = get_tag(os.path.basename(original_path))
            if tag:
                new_path = original_path.replace(f'gfx/interface/ideas/ideas/', f'gfx/interface/ideas/{tag}/')
                data[i] = data[i].replace(original_path, new_path)

    with open(gfx_file, 'w') as file:
        file.writelines(data)

if __name__ == "__main__":
    # Get the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))
    ideas_directory = os.path.join(current_directory, "gfx/interface/ideas/ideas")
    gfx_file = os.path.join(current_directory, "interface/FX_ideas.gfx")

    # Step 1: Move files to TAG folders
    move_files(ideas_directory)

    # Step 2: Update texture file paths in FX_ideas.gfx
    update_texture_paths(gfx_file, ideas_directory)

    print("Script execution completed.")
