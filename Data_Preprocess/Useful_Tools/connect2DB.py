import mysql.connector

# 数据库连接配置
config = {
    'host': 'database-1.c3muuumcmadk.eu-central-1.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',        # 替换为您的用户名
    'password': 'vcteva_2024',    # 替换为您的密码
    'database': 'database-1'     # 替换为您的数据库名
}

try:
    # 建立数据库连接
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print('成功连接到数据库')
        cursor = connection.cursor()
        
        # 执行 SQL 查询
        cursor.execute('SELECT * FROM your_table')  # 替换为您的表名
        results = cursor.fetchall()
        for row in results:
            print(row)
        
        # 关闭游标和连接
        cursor.close()
        connection.close()
except mysql.connector.Error as err:
    print(f"连接失败：{err}")