import pandas as pd
from django.db import connection
from upload.managers.exception import InterruptException
import os

# print(os.getcwd())
# print(os.listdir(os.getcwd())



class UploadManager:
    """ An upload manager class which interacts with the database"""

    def __init__(self, id, file_name="Records.csv"):
        

        self.id = id
        self.file_name = file_name
        self.table_name = id
        self.lines = 0
        self.paused = False
        self.terminated = False
        self.completion = 0
        self.head = ""
        self.total_rows = 0
        super().__init__()

    

    def create(self):
        """Method to create a table and save to the database.

        Raises:
            Conflict: If a table with same name already exists.
        """
        def create_head(c):
            query = f'CREATE TABLE {self.table_name} (\
            Sid SERIAL PRIMARY KEY, \
            Region varchar(255), \
            Country varchar(255), \
            "Item Type" varchar(255), \
            "Sales Channel" varchar(255), \
            "Order Priority" varchar(255), \
            "Order ID" varchar(255), \
            "Units Sold" FLOAT,\
            "Unit Price" FLOAT,\
            "Unit Cost" FLOAT,\
            "Total Revenue" FLOAT,\
            "Total Cost" FLOAT,\
            "Total Profit" FLOAT\
            );'
            c.execute(query)
            df = pd.read_csv(self.file_name, skiprows=self.lines)
            self.head = df.columns.to_list()
        
        try:
            c = connection.cursor()
            create_head(c)
            tmp = ""
            for i in self.head:
                if len(tmp) != 0:
                    tmp += ","
                if len(str(i).split(" ")) == 1:
                    tmp += str(i)
                else:
                    tmp += '"' + str(i) + '"'
            self.head = tmp
            print(tmp)
            print(len(tmp))
        finally:
            c.close()


    def begin(self):
        """
        Method to begin uploading rows of csv file into database
        """
        c = connection.cursor()

        self.paused = False
        self.terminated = False

        df = pd.read_csv(self.file_name, skiprows=self.lines)
        rows = [list(row) for row in df.values]
        #print(rows)
        
        if self.lines == 0:
            self.create()
            self.total_rows = len(df)

        query = f"select column_name\
            from information_schema.columns\
            where table_schema = 'public' and table_name = 'new';"
        print(query)
        data = c.execute(query)
        print(data)

        for row in rows:
            try:
                tmp = ""
                for i in row:
                    if len(tmp) != 0:
                        tmp += ","
                    tmp += "'" + str(i) + "'"
                row = tmp
                query = f"INSERT INTO {self.table_name}({self.head}) VALUES({row});"
                c.execute(query)
                self.lines += 1
                self.completion = self.lines / self.total_rows * 100
                status = self.status()
                if status:
                    raise InterruptException
            except InterruptException:
                break

    def pause(self):
        """
        Method to pause upload of rows from csv file into database. 
        """
        self.paused = True

    def resume(self):
        """
        Method to resume upload of rows from csv file into database. 
        """
        if self.terminated:
            return
        self.paused = False
        self.begin()

    def status(self):
        """
        Method to check pause/terminate status.  
        """
        return self.paused or self.terminated

    def terminate(self):
        """
            Method to Rollback all the entries till now in the database. 
        """
        c = connection.cursor()
        self.terminated = True
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        c.execute(query)

    def get_progress(self):
        """
            Method to get percentage completion of upload.
        """
        return self.completion

    def table_exists(self):
        c = connection.cursor()
        try:
            query = f"SELECT MAX(SId) from {self.table_name}"
            c.execute(query)
            return True
        except:
            return False
            
