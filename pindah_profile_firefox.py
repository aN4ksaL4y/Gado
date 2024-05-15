import os
import subprocess
import shutil
import time

# ini penting nya
dir_profile_kini = '~/.mozilla/firefox'
dir_profile_lama = '/media/pyjri/H/firefox'


def read_profile_name(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        profile_name = file.read().splitlines()
    
    if not profile_name:
        raise ValueError("Error: Profile name is empty.")
    
    return profile_name

def create_firefox_profile(profile_name):
    print(f"Creating new Firefox profile: {profile_name}")
    subprocess.run(['firefox', '-CreateProfile', profile_name], check=True)

def find_profile_directory(profile_name):
    base_dir = os.path.expanduser(dir_profile_kini)
    # print(os.listdir(base_dir))
    for dirname in os.listdir(base_dir):
        # print(dirname)
        if dirname.endswith(f'.{profile_name}'):
            print(os.path.join(base_dir, dirname))
            return os.path.join(base_dir, dirname)
    return None

def find_old_profile_directory(profile_name):
    base_dir = os.path.expanduser(dir_profile_lama)
    # print(os.listdir(base_dir))
    for dirname in os.listdir(base_dir):
        # print(dirname)
        if dirname.endswith(f'.{profile_name}'):
            print(os.path.join(base_dir, dirname))
            return os.path.join(base_dir, dirname)
    return None

def copy_profile_contents(old_profile_dir, new_profile_dir):
    print("Copying old profile directory contents to the new profile directory")
    for item in os.listdir(old_profile_dir):
        src = os.path.join(old_profile_dir, item)
        dest = os.path.join(new_profile_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)

def main():
    profile_name_file = 'profile_name.txt'
    
    try:
        profile_names = read_profile_name(profile_name_file)
        for profile in profile_names:
            print('time sleep 1')
            time.sleep(1)
            find_profile_directory(profile)

            create_firefox_profile(profile)
            
            new_profile_dir = find_profile_directory(profile)
            if not new_profile_dir:
                raise FileNotFoundError("Error: Failed to create the new profile directory.")
            
            old_profile_dir = find_old_profile_directory(profile)
            if not old_profile_dir:
                print(f"Error: Old profile directory matching pattern {profile} does not exist.")
                
            
            
            copy_profile_contents(old_profile_dir, new_profile_dir)
            
            print("Profile creation and copying complete.")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
