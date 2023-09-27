from .entities.Aula1 import Aula1


class ModelAula1():

    @classmethod
    def login(self, db, aula1):
        try:
            cursor = db.connection.cursor()
            sql2 = """use BurritoLoco2000$flask_ingresos"""
            cursor.execute(sql2)
            sql = """SELECT id, aula, password FROM aula1 WHERE aula = '{}'""".format('aula1')
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                aula1 = Aula1(row[0], row[1], Aula1.check_password(row[2], aula1.password))
                return aula1
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


