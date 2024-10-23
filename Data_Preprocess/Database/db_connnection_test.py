connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vcteva_2024",
        database="VCTEVA",
        )
        cursor = connection.cursor()
        cursor.execute(response)
        column_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        result_df = pd.DataFrame(result, columns=column_names)
        cursor.close()
        connection.close()
        #可执行的SQL语句: 
        print(response)