# -*- coding: utf-8 -*-
import pandas as pd
import timeit
from .miscFunc import INF


class modBuilder(object):
    def __init__(self, obj_data, output, obj_mod):
        self.data = obj_data
        self.model = obj_mod
        
        self.patternList = list(obj_data.pattern.keys())
        self.orderList = list(obj_data.order["number_ordered"].keys())
        
        self.var = type("Variable", (dict,), {})()
        # self.var.update({
        #     i: {} for i in patternList
        #     })
        
        self.obj = type("Objective", (dict,), {})()
        # self.obj.update({
        #     "waste": {}
        #     })

        self.out = type("Output", (dict,), {})()
        self._run_time = 0
    
    def build(self):
        time_s = timeit.default_timer()
        
        self._add_var()
        self._add_con()
        self._add_obj()
        self._set_obj()
        
        time_e = timeit.default_timer()
        self._run_time = round(time_e - time_s, 4)
        
        return self
    
    def _add_var(self):
        model = self.model
        
        self.var = dict({
            "pattern": {
                i: model.Int_var(lb=0, ub=INF, name="") for i in self.patternList}})
    
    def _add_con(self):
        model = self.model
        data = self.data
        v = self.var
        
        for i in self.orderList:
            model.Constr(sum([data.cut[i][j] * v["pattern"][j] for j in self.patternList]) >= data.order["number_ordered"][i])
                    
    def _add_obj(self):
        v = self.var
        
        self.obj = dict({
            "quantity": sum([v["pattern"][i] for i in self.patternList]),
            })
    
    def _set_obj(self):
        cost = 0
        
        for key, item in self.obj.items():
            cost += item
        
        self.model.Minimize(cost)
    
    def getModel(self):
        return self.model
    
    def getVarList(self):
        return list(self.var.keys())