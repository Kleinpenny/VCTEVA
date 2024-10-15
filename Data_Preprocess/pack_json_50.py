import os
import zipfile
import random

# 文件所在目录
folder_path = '/home/yxpeng/Projects/VCTEVA/DATA/'

# 要打包的文件列表，包括指定文件和同目录下其他两个文件
files_to_zip = [
    'val:27d62958-08be-448b-9e93-0dee481d1909.json',
    'val:d7bc6669-96e0-4800-a8ed-87a7de369f53.json',  # 替换为实际的其他两个文件名
    'val:f402a314-dcd3-4645-8a8d-8da5d8b03cc6.json'   # 替换为实际的其他两个文件名
]

# 打包后的 ZIP 文件名
zip_filename = '/home/yxpeng/Projects/VCTEVA/DATA/selected_files.zip'

# 创建 ZIP 文件并将所有文件打包
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for file in files_to_zip:
        # 将文件路径加入到 ZIP 文件中
        zipf.write(os.path.join(folder_path, file), file)

print(f"Files have been zipped into {zip_filename}")
