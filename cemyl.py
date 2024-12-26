import mysql
from mysql.connector import Error

# 数据库配置
db_config = {
    "host": "10.4.1.184",      # MySQL 服务器地址
    "user": "admin",           # 数据库用户名
    "password": "admin",       # 数据库密码
    "database": "renren_fast",  # 数据库名
    "port": 3307              # 指定 MySQL 端口
}

def test_db_connection():
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print("成功连接到数据库！")

            # 获取数据库服务器信息
            db_info = connection.get_server_info()
            print(f"数据库版本: {db_info}")

            # 创建一个游标对象，执行简单查询
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"当前连接的数据库是: {record[0]}")

    except Error as e:
        print(f"数据库连接错误: {e}")

    finally:
        # 关闭连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭。")


# 测试数据库连接
if __name__ == "__main__":
    test_db_connection()
