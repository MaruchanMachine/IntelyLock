from .entities.Aula3 import Aula3


class ModelAula3():

    @classmethod
    def login(self, db, aula3):
        try:
            cursor = db.connection.cursor()
            sql2 = """use BurritoLoco2000$flask_ingresos"""
            cursor.execute(sql2)
            sql = """SELECT id, aula, password FROM aula3 WHERE aula = '{}'""".format('aula3')
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                aula3 = Aula3(row[0], row[1], Aula3.check_password(row[2], aula3.password))
                return aula3
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


