# import mysql.connector
#
#
#
# class Database:
#     def __init__(self, dbname:str = "default.db") -> None:
#         self.dbname = dbname
#
#     db = mysql.connector.connect(
#         host="hostname",
#         user="username",
#         passwd="password",
#         database="databasename"
#     )
#     c = db.cursor()
#
#
#     def init_table(self) -> None:
#
#         c.execute('''CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             passwd TEXT NOT NULL,
#             email TEXT NOT NULL)''')
#
#
#     def __enter__(self):
#         self.init_table()
#         self.conn = mysql.connect(self.dbname)
#         self.conn.row_factory = mysql.Row
#         self.cursor = self.conn.cursor()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.conn:
#             self.conn.commit()
#             self.conn.close()
#
#     def get_clicker(self) -> list:
#         self.cursor.execute("SELECT * FROM clicker")
#         return self.cursor.fetchall()
#
#     def insert_clicker(self, clicker: dict) -> None:
#         self.cursor.execute("INSERT INTO clicker (category, description, value) VALUES (?, ?, ?)",
#                             (clicker['category'], clicker['description'], clicker['value']))
#     def remove_expense(self,clicker_id: str) -> None:
#         self.cursor.execute(f"DELETE FROM clicker WHERE id = {clicker_id}")
#
