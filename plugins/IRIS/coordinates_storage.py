import sqlite3
import os
import logger


try:

    class Sqlitecreatetable():

        def __init__(self,theta,hypox,hypoy):
            self.db_path = os.path.join(os.getenv("AVO_ASSURE_HOME"), 'assets',
                'coordinates.db')
            # self.db_path='coordinates.db'
            self.theta=theta
            self.hypox=hypox
            self.hypoy=hypoy
            
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            
        def createtable(self):
            self.cursor.execute("DROP TABLE IF EXISTS COORDINATETRANSFORMATION")
            
            table ="""CREATE TABLE COORDINATETRANSFORMATION(THETA FLOAT, HYPOX FLOAT,
                    HYPOY FLOAT);"""
            
            self.cursor.execute(table)
            
            self.cursor.execute('''INSERT INTO COORDINATETRANSFORMATION VALUES (?, ?, ?)''',
                (self.theta, self.hypox, self.hypoy))
            
            # Commit the transaction
            self.conn.commit()

            # Close the connection
            #self.conn.close()

    class Sqliteloadtable():


        def __init__(self):
            
            #self.create_constructor=create_constructor
            
            #super().__init__(db_path,conn,cursor)
            
            self.db_path = os.path.join(os.getenv("AVO_ASSURE_HOME"), 'assets',
                'coordinates.db')
            
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

        def loadtable(self):

            data=self.cursor.execute('''SELECT * FROM COORDINATETRANSFORMATION''')

            result = self.cursor.fetchone()
            theta=result[0]
            hypox=result[1]
            hypoy=result[2]

            # for row in data:
            #     print(row)

            # Commit your changes in the database    
            #self.create_constructor.conn.commit()

            # Closing the connection
            self.conn.close()

            return theta,hypox,hypoy

            #print(self.var.db_path)

except Exception as e:
    logger.print_on_console('error in sqlite db',e)