# This code is dropped from the project by low performance.
# It was intended to substitute Pandas because it was slow, but this module resulted ton be worse than Pandas.

from datetime import datetime
from numpy import nan
import colors
import pandas as pd

class Column:
    def __init__(self, name: str, data_type: type, key=False):
        self.name = name
        self.data_type = data_type
        self.data = []
        self.key = key

class Log:
    def __init__(self, name: str, columns: list[Column]):
        self.name = name
        self.data = []
        self.key_columns = []
        self.__add_columns(columns)

    def __add_columns(self, columns: list[Column]):
        for column in columns:
            self.data.append(column)
            if column.key:
                self.key_columns.append(column)
    
    def add_entry(self, data: list[str|int|float]):
        if len(data) != len(self.data):
            raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} You must provide the same quantity of data as columns.")

        for i in range(len(self.data)):
            if type(data[i]) == self.data[i].data_type :
                    self.data[i].data.append(data[i])
            elif type(data[i]) == None:
                self.data[i].data.append(nan)
            else:
                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} {data[i]} do not match column \"{self.data[i].name}\" type: {self.data[i].data_type}.")

    def update(self, where: str|Column|list[str|Column], find: str|int|float|list[str|int|float], change_column: str|Column, value: str|int|float):
        if type(where) == list and type(find) == list:
            if len(where) == len(find):
                search_term = "".join([str(find_value) for find_value in find])
                terms = []
                key_columns = self.key_columns.copy()
                change_indexes = []

                for search_column in where:
                    for column in key_columns:
                        search_column_name = search_column
                        if type(search_column) == list:
                            search_column_name = search_column.name
                        if column.name != search_column_name:
                            try:
                                key_columns.remove(column)
                            except:
                                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} Column {search_column_name} not found. Search column must be key or name is incorrect.")
                
                for i in range(len(key_columns[0].data)):
                    term = ""
                    for column in key_columns:
                        term += str(column.data[i])
                    terms.append(term)
                
                for j in range(len(terms)):
                    if terms[j] == search_term:
                        change_indexes.append(j)
                
                if len(change_indexes) == 0:
                    raise Exception(f"{colors.Bold.yellow}Warning:{colors.Text.end} Search terms not found.")

                for column in self.data:
                    if column == change_column or column.name == change_column:
                        for index in change_indexes:
                            column.data[index] = value

            else:
                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} You must provide the same quantity of arguments for where (columns) and find values. The index for each find value must correspond the index of each column.")
            
        elif type(where) != list and type(find) != list:
            for column in self.key_columns:
                if column == where or column.name == where:
                    for column_2 in self.data:
                        if column_2 == change_column or column_2.name == change_column:
                            column_2.data[column.index(value)] = value
                else:
                    raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} Search column (where) and find value must be both list or both a single value.")       
        else:
            raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} Search column (where) and find value must be both list or both a single value.")
            
    def to_dataframe(self):
        d = {}

        for column in self.data:
            d.update({column.name: column.data})

        return pd.DataFrame(data=d)
    
    def to_excel(self):
        df = self.to_dataframe()
        df.to_excel(f"{self.name}-{datetime.now()}.xlsx")