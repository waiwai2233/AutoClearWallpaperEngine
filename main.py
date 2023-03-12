# Auto clear Wallpaper Engine
import os
import shutil
import errno
import stat

def byte_to_gb(byte):
    return byte / 1024**3

def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
        print("done")
    else:
        print("not done")
        raise

# main code starts here

# set the path to where all the wallpapers are stored
# eg r"D:\SteamLibrary\steamapps\workshop\content\431960"
wallpaper_path = r""

# Change working directory to wallpaper
os.chdir(wallpaper_path)

df_before = shutil.disk_usage(wallpaper_path).used

# store number of files removed
cnt = 0

# Loop all the sub-directories to search for directories without .json file
for dir in os.listdir(wallpaper_path):
    # Check whether its child folder contains .json file
    child_path = os.path.join(wallpaper_path, dir)
    child_content = os.listdir(child_path)
    contain_json = False
    for file in child_content:
        if file.endswith(".json"):
            contain_json = True
            break
    
    if not contain_json:
        # Remove all the content in the sub-folder and delete the folder
        try:
            shutil.rmtree(child_path, ignore_errors=False, onerror=handleRemoveReadonly)
            cnt += 1
            print("{} has been removed successfully.".format(child_path))
        except Exception as e:     
            print("An error occured when removing file: {}".format(child_path))
            print("Error: {}".format(e))

df_after = shutil.disk_usage(wallpaper_path).used
print("Disk usage before erasing: {:.2f} Gb.".format(byte_to_gb(df_before)))
print("Disk usage after erasing: {:.2f} Gb.".format(byte_to_gb(df_after)))
print("{:.2f} Gb has been erased.".format(byte_to_gb(df_before - df_after)))
print("{} files has been erased.".format(cnt))