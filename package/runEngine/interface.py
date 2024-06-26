# -*- coding: utf-8 -*-
import pandas as pd
from dataclasses import dataclass, asdict
import os

class modData(object):
    def __init__(self, file_name: str = None):
        self._file_name = file_name

        self._read_file()
        
    def __str__(self):
        return "modData"
    
    @property
    def file_name(self):
        return self._file_name
    
    def _read_file(self):
        try:
            input_path = self._file_name
            file_name = os.fsdecode(input_path)
            workbook = pd.ExcelFile(file_name)
            
            # Load order data
            order_df = workbook.parse("Order")
            order_df = order_df.iloc[:,:2]
            order_df.columns = ["order_width", "number_ordered"]
            order_df.set_index("order_width", inplace=True)
            self._order_df = order_df
            
            # Load pattern data
            pattern_df = workbook.parse("Pattern")
            pattern_df = pattern_df.iloc[:,:2]
            pattern_df.columns = ["pattern_id", "pattern_cut"]
            pattern_df.set_index("pattern_id", inplace=True)
            self._pattern_df = pattern_df
            
            self.processData()
            
            return self._input
            
            
        except FileNotFoundError:
            raise Exception("No such file in directory.")
    
    def processData(self):
        order_dict = self._order_df.to_dict()
        pattern_dict = self._pattern_df.to_dict()
        pattern_dict = {index: modData.to_float(item) for index, item in pattern_dict["pattern_cut"].items()}
        
        cut_dict = {i: {} for i in order_dict["number_ordered"].keys()}
        for i in order_dict["number_ordered"].keys():
            for j in pattern_dict.keys():
                cut_dict[i][j] = sum(map(lambda x: x==i, pattern_dict[j]))
        
        input = DataCS(order=order_dict, pattern=pattern_dict, cut=cut_dict, masterWidth=35)
        
        self._input = input
    
    @staticmethod
    def to_float(list):
        list = list.split("-")
        list = [float(item) for item in list]
        
        return list


class modWriter(object):
    def __init__(self, data=None, solution=None, output=None):
        self._data = data
        self._solution = solution
        self._output = output
            
    def to_result(self, file_out: str = None):
       """Write the soluton to json file with the input data."""
       try:
           solution = self._solution
           dt_out = {
               "logging": solution.logging
           }

           # input data
           if solution.solution:
               
               dt_out = {
                   "logging": solution.logging,
                   "pattern_ordered": solution.solution["pattern"],
                   "waste": modWriter.get_waste(self._data.masterWidth, self._data.pattern, solution.solution["pattern"]) 
               }

           return dt_out

       except Exception as err:
           raise err
          
    
    @staticmethod
    def get_waste(width, pattern, order):
        return sum([order[i] * (width - sum(pattern[i])) for i in pattern.keys()])
     
@dataclass
class DataCS:
    order: dict
    pattern: dict
    cut: dict
    masterWidth: int