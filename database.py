import sqlite3
import pandas as pd
import os

"""
autocommit mode not on by default.
by default, a BEGIN statement is issued, which disables autocommit.
"""
class Database:
	def __init__(self, sink_db_filename, init_case=False):
		# self.parent_dir = parent_dir
		# self.db_name = "database.db"
		# self.database_path = os.path.join(parent_dir, self.db_name)
		self.database_path = sink_db_filename
		self.init_case = init_case

		try:
			self.conn = sqlite3.connect(self.database_path)
			self.cursor = self.conn.cursor()
		except sqlite3.Error as error:
			self.cursor.close()
			self.conn.close()
			raise error

		self.initiate_database()

	def get_conn(self):
		return self.conn

	def get_cur(self):
		return self.cursor

	def commit_and_close_cursor(self):
		self.conn.commit()
		self.cursor.close()

	def save_and_close(self):
		self.commit_and_close_cursor()
		self.conn.close()

	def rollback_and_close(self):
		self.conn.rollback()
		self.cursor.close()
		self.conn.close()

	def initiate_database(self):
		create_table_query = '''CREATE TABLE IF NOT EXISTS annotations 
											(bbox_id INTEGER PRIMARY KEY,
											row_start INTEGER NOT NULL,
											row_end INTEGER NOT NULL,
											col_start INTEGER NOT NULL,
											col_end INTEGER NOT NULL,
											z_start INTEGER,
											z_end INTEGER)'''
		try:
			if self.init_case:
				self.cursor.execute("DROP TABLE IF EXISTS annotations")
			self.cursor.execute(create_table_query)
		except sqlite3.Error as error:
			self.rollback_and_close()
			raise error
		else:
			self.conn.commit()

	def add_or_update_annotation(self, annotation):
		bbox_id = annotation[0]
		check_query = "SELECT * FROM annotations WHERE bbox_id =:bbox_id"
		try:
			self.cursor.execute(check_query, {"bbox_id": bbox_id})
			results = self.cursor.fetchall()
			if results:
				self.update_annotation(annotation)
			else:
				self.add_annotation(annotation)
		except sqlite3.Error as error:
			self.rollback_and_close()
			raise error

	def add_annotation(self, annotation):
		# bbox_id, row_start, row_end, col_start, col_end, z_start, z_end = annotation
		add_annotation_query = "INSERT INTO annotations VALUES (?,?,?,?,?,?,?)"
		try:
			self.cursor.execute(add_annotation_query, annotation)
		except sqlite3.Error as error:
			self.rollback_and_close()
			raise error
		else:
			self.conn.commit()

	def update_annotation(self, annotation):
		bbox_id, row_start, row_end, col_start, col_end, z_start, z_end = annotation
		# annotation = (row_start, row_end, col_start, col_end, z_start, z_end, bbox_id)
		update_annotation_query = '''UPDATE annotations SET 
									row_start = :row_start,
									row_end = :row_end,
									col_start = :col_start,
									col_end = :col_end,
									z_start = :z_start,
									z_end = :z_end
									WHERE bbox_id = :bbox_id'''
		annotation = {"row_start": row_start, "row_end": row_end, 
						"col_start": col_start, "col_end": col_end,
						"z_start": z_start, "z_end": z_end, "bbox_id": bbox_id}
		try:
			self.cursor.execute(update_annotation_query, annotation)
		except sqlite3.Error as error:
			self.rollback_and_close()
			raise error
		else:
			self.conn.commit()

	def delete_annotation(self, bbox_id):
		delete_annotation_query = "DELETE FROM annotations WHERE bbox_id = :bbox_id"
		try:
			self.cursor.execute(delete_annotation_query, {"bbox_id": bbox_id})
		except sqlite3.Error as error:
			self.rollback_and_close()
			raise error
		else:
			self.conn.commit()

	def export_as_csv(self, destination_path):
		df = pd.read_sql_table('annotations', self.conn)
		df.to_csv(r'' + destination_path, index=False)