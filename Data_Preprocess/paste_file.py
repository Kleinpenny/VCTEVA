import shutil

# 源文件路径
source_path = '../DATA/game-changers/games/2022/val:d7bc6669-96e0-4800-a8ed-87a7de369f53.json'

# 目标文件夹路径
destination_path = '/home/yxpeng/Projects/VCTEVA/DATA/'

# 执行复制操作，将文件复制到目标路径
shutil.copy(source_path, destination_path)

print(f"File copied to {destination_path}")
