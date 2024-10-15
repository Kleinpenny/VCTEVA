import shutil

# 源文件路径
source_path = '../DATA/vct-international/games/2023/val:08482ebc-623b-44bf-844a-ac82b1694d42.json'

# 目标文件夹路径
destination_path = '/home/yxpeng/Projects/VCTEVA/DATA/'

# 执行复制操作，将文件复制到目标路径
shutil.copy(source_path, destination_path)

print(f"File copied to {destination_path}")
