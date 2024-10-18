import shutil

# 源文件路径
source_path = "../DATA/all_players.json"

# 目标文件夹路径
destination_path = '../DATA/game-changers/'

# 执行复制操作，将文件复制到目标路径
shutil.copy(source_path, destination_path)

print(f"File copied to {destination_path}")
