import os
import shutil
import sys
from datetime import datetime


#
#
#
#
#
def main(src_dir, dest_dir):
    for foldername, _, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.lower().endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mov', '.mp4', '.avi')
            ):
                filepath = os.path.join(foldername, filename)
                timestamp = os.path.getmtime(filepath)
                dt_object = datetime.fromtimestamp(timestamp)
                city = foldername.split('/')[-1]
                day = dt_object.strftime('%Y-%m-%d')
                dest_folder = os.path.join(dest_dir, city, day)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                shutil.copy2(filepath, dest_folder)


#
#
#
#
#
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py [source directory] [destination directory]")
    else:
        main(sys.argv[1], sys.argv[2])
