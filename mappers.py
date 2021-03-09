import sqlite3
from models import Student

connection = sqlite3.connect('db/site.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class StudentMapper:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.table_name = 'student'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.conn.commit()
        except Exception as error:
            raise DbCommitException(error.args)

    def update(self, obj):
        statement = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.conn.commit()
        except Exception as error:
            raise DbUpdateException(error.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.conn.commit()
        except Exception as error:
            raise DbDeleteException(error.args)


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)