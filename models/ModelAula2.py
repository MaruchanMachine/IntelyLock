from .entities.Aula2 import Aula2


class ModelAula2():

    @classmethod
    def login(self, db, aula2):
        try:
            cursor = db.connection.cursor()
            sql2 = """use BurritoLoco2000$flask_ingresos"""
            cursor.execute(sql2)
            sql = """SELECT id, aula, password FROM aula2 WHERE aula = '{}'""".format('aula2')
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                aula2 = Aula2(row[0], row[1], Aula2.check_password(row[2], aula2.password))
                return aula2
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


