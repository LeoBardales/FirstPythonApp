from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT u.UserId as UserId , u.Email as Email, u.Password as Password,u.Activo as Activo,u.IdUserType as IdUserType, u.Nombre as Nombre FROM users as u inner join estudiantes as e on u.UserId=e.UserId WHERE u.Email = '{}' or e.NCuenta='{}'".format(user.username,user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row['UserId'], row['Email'], User.check_password(row['Password'], user.password),row['Activo'],row['IdUserType'],0, row['Nombre'])
                return user
            else:
                cursor = db.connection.cursor()
                sql = "SELECT *FROM users WHERE Email = '{}' ".format(user.username)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    user = User(row['UserId'], row['Email'], User.check_password(row['Password'], user.password),row['Activo'],row['IdUserType'],0, row['Nombre'])
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT UserId, Email,Activo,IdUserType, Nombre FROM users WHERE UserId = {}".format(id,)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                tipouser=row['IdUserType']
                if int(tipouser) == 1 or int(tipouser) == 3:
                    return User(row['UserId'], row['Email'], None,row['Activo'],row['IdUserType'],0, row['Nombre'])
                else:
                    cursor1 = db.connection.cursor()
                    sql = "SELECT EstudiantesId FROM estudiantes WHERE UserId = {}".format(id,)
                    cursor1.execute(sql)
                    row1 = cursor1.fetchone()
                    return User(row['UserId'], row['Email'], None,row['Activo'],row['IdUserType'],row1['EstudiantesId'], row['Nombre'])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
