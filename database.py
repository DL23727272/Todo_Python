import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(50) NOT NULL,
            due_date VARCHAR(50),
            completed BOOLEAN NOT NULL
        )
        '''
        self.cursor.execute(create_table_query)
        self.con.commit()

    def create_task(self, task, due_date=None):
        insert_task_query = "INSERT INTO tasks(task, due_date, completed) VALUES(%s, %s, %s)"
        self.cursor.execute(insert_task_query, (task, due_date, 0))
        self.con.commit()

        # Retrieve the last inserted ID
        last_inserted_id = self.cursor.lastrowid

        # Retrieve the created task using the last inserted ID
        created_task_query = "SELECT id, task, due_date FROM tasks WHERE id = %s"
        self.cursor.execute(created_task_query, (last_inserted_id,))
        created_task = self.cursor.fetchall()

        return created_task[-1]

    def get_tasks(self):
        complete_tasks_query = "SELECT id, task, due_date FROM tasks WHERE completed = 1"
        incomplete_tasks_query = "SELECT id, task, due_date FROM tasks WHERE completed = 0"

        self.cursor.execute(complete_tasks_query)
        complete_tasks = self.cursor.fetchall()

        self.cursor.execute(incomplete_tasks_query)
        incomplete_tasks = self.cursor.fetchall()

        return incomplete_tasks, complete_tasks

    def mark_task_as_complete(self, taskid):
        update_query = "UPDATE tasks SET completed = 1 WHERE id = %s"
        self.cursor.execute(update_query, (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        update_query = "UPDATE tasks SET completed = 0 WHERE id = %s"
        self.cursor.execute(update_query, (taskid,))
        self.con.commit()

        task_text_query = "SELECT task FROM tasks WHERE id = %s"
        self.cursor.execute(task_text_query, (taskid,))
        task_text = self.cursor.fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        delete_query = "DELETE FROM tasks WHERE id = %s"
        self.cursor.execute(delete_query, (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
