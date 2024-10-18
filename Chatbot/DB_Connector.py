import json
import mysql.connector
import pandas as pd
from mysql.connector import Error

def sql_connector(query):

    # 连接数据库
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="vct",
            password="Leon1234",
            database="VCTEVA",
        )
        if connection.is_connected():
            print("Connected to MySQL server")

        cursor = connection.cursor()

        # 执行 SQL 查询
        cursor.execute(query)

        # 获取列名
        column_names = [desc[0] for desc in cursor.description]

        # 获取所有查询结果
        result = cursor.fetchall()

        # 将结果转换为 DataFrame
        df = pd.DataFrame(result, columns=column_names)

        # 打印 DataFrame
        return df

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
