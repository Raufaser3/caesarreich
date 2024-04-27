import os

while True:
    current_directory = os.getcwd()
    goal_directory = os.path.join(current_directory, "gfx/interface/goals")

    filename = input("Enter the filename (or 'exit' to quit): ")
    sprite_id = os.path.splitext(filename)[0]  # Remove the file extension

    if filename.lower() == 'exit':
        break
    
    matching_files = [f for f in os.listdir(goal_directory) if f == filename]
    
    if not matching_files:
        print(f"File '{filename}' not found in the 'gfx/interface/goals' directory.")
        continue
    
    interface_directory = os.path.join(current_directory, "interface")
    fx_goals_filepath = os.path.join(interface_directory, "FX_goals.gfx")
    
    with open(fx_goals_filepath, 'a') as fx_goals_file:
        # Step 6: Find the last closing bracket of the spriteTypes block
        last_bracket = None
        with open(fx_goals_filepath, 'r') as fx_goals_read:
            lines = fx_goals_read.readlines()
            for index, line in enumerate(reversed(lines)):
                if "}" in line:
                    last_bracket = len(lines) - index - 1
                    break
        
        if last_bracket is not None:
            
            new_filename = os.path.join("gfx/interface/goals", filename).replace("\\", "/")
            new_sprite_type = f'\n\tspriteType = {{\n\t\tname = "GFX_goal_{sprite_id}"\n\t\ttextureFile = "{new_filename}"\n\t}}'

            lines.insert(last_bracket, new_sprite_type + "\n")
            
            with open(fx_goals_filepath, 'w') as fx_goals_rewrite:
                fx_goals_rewrite.writelines(lines)
                
            print(f"New SpriteType entry added for '{filename}'")
        else:
            print("No closing bracket found for spriteTypes block in 'FX_goals.gfx'")

print("Exiting the script.")
