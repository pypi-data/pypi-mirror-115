import mysql.connector as mysql


class DataBase:
    def __init__(self, host='192.168.50.220', port=8457, user='Tanquoc', passwd='t@nqu0c1', Db='DBS01'):
        self.host = host
        self.Mydb = mysql.connect(
            host=self.host,
            port=port,
            user=user,
            passwd=passwd,
            database=Db
        )

    def Closed(self):
        self.Mydb.close()

    def CreateTable(self, tablestring):
        curs = self.Mydb.cursor()
        try:
            curs.execute(tablestring)
            print('Tạo Table thành công')
            curs.close()
        except Exception as vala:
            print('Tạo bảng Không thành Công', str(vala))
            curs.close()
            return None

    def GetData(self, query, Method):
        mycs = self.Mydb.cursor()
        try:
            mycs.execute(query, Method)
            mydta = mycs.fetchall()
            mycs.close()
            return mydta
        except Exception as e:
            print(str(e))
            mycs.close()
            return None
        pass

    def InsertData(self, query, lstValue):
        Mycs = self.Mydb.cursor()
        try:
            Mycs.execute(query, lstValue)
            self.Mydb.commit()
            print(Mycs.rowcount, 'Duoc insert vao bang')
            Mycs.close()
            return True
        except Exception as e:
            print(str(e))
            Mycs.close()
            return None
        pass

    def UpdateData(self, query, lstParameter):
        cs = self.Mydb.cursor()
        try:
            cs.execute(query, lstParameter)
            self.Mydb.commit()
            print('Update Finshed')
            # Disconnecting from the database
            cs.close()
        except Exception as e:
            print(str(e))
            cs.close()
            return None

    def Delete(self):

        pass
