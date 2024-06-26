# -*- coding: utf-8 -*-
import pandas as pd

class modOptimizer(object):

    def __init__(self):
        self.logging = {}
        self.solution = None
        
    def solveOpt(self, builder):
        model = builder.getModel()
        self.logging.update({"num_cons": model.NumConstr})
        self.logging.update({"num_vars": model.NumVars})
        self.logging.update({"solver_type": model.SolverType})
        
        # REAL OPTIMIZATION
        obj_val, opt_status, solution_time = model.optimizeModel()
        
        if obj_val is not None:
            self.logging.update({
                "obj_value": obj_val,
                "opt_status": opt_status,
                "solution_time": solution_time
                })
        else:
            self.logging.update({
                "obj_value": None,
                "opt_status": opt_status,
                "solution_time": solution_time
                })
            
        return self
    
    def getSolution(self, builder=None):
        var_list = builder.getVarList()        
        status = self.logging["opt_status"]        
        
        builder.out.update({
            key: {} for key in var_list
            })

        
        if status == "OPTIMAL" or status == "FEASIBLE":
            for key, item in builder.var.items():
                if type(item) == dict:
                    out = {sub_key: builder.getModel().GetVarVal(sub_item) for sub_key, sub_item in item.items()}
                    builder.out[key] = out
                else:
                    out = builder.getModel().GetVarVal(item)
                    builder.out[key] = out
        
        elif status in ["TIME_LIMIT_INFEASIBLE", "INFEASIBLE", "UNBOUNDED"]:
            builder.out = {}
        else:
            raise Exception("Model status is strange. check OptSolver.")
        
        self.solution = builder.out