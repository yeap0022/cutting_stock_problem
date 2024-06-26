try:
    from ortools.linear_solver import pywraplp
except ImportError:
    pass

from functools import partial
from .abs_solver import SolverABC
from time import time

class modelCBC(SolverABC):
    def __init__(self, params):
        self._p = pywraplp.MPSolverParameters()
        
        super().__init__(params)
        
    def createModel(self): # create_model
        self._m = pywraplp.Solver("", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        
    def optimizeModel(self): # optimize_model
        solution_time, obj_val, opt_status = 0.0, None, None
        
        time_s = time()
        status = self._m.Solve(self._p)
        time_e = time() - time_s
        
        status = self._status_dict[status]
        
        solution_time = time_e
        count_sol = 1
        
        if status == "OPTIMAL":
            opt_status = "OPTIMAL"
            obj_val = self.GetObjVal()
        elif status == "TIME_LIMIT":
            if count_sol > 0:
                opt_status = "FEASIBLE"
                obj_val = self.GetObjVal()
            else:
                opt_status = "TIME_LIMIT_INFEASIBLE"
        elif status == "NOT_SOLVED":
            opt_status = "NOT_SOLVED"
        else:
            opt_status = status
            
        return obj_val, opt_status, solution_time
    
    @property
    def NumVars(self): # num_vars
        return self._m.NumVariables()
    
    @property
    def NumConstr(self): # num_cons
        return self._m.NumConstraints()
    
    @property
    def SolverType(self):
        return "CBC"
    
    def GetObjVal(self): # _get_obj_val
        return self._m.Objective().Value()
    
    def GetVarVal(self, x): # get_var_val
        return x.solution_value()
    
    def SetMIPGap(self, mip_gap): # _set_mipgap
        self._p.SetDoubleParam(self._p.RELATIVE_MIP_GAP, mip_gap)

    def SetTimeLimit(self, time_limit): # _set_time_limit
        self._m.SetTimeLimit(int(time_limit*1e3))
        
    @property
    def Num_var(self): # add_C_var
        return self._m.NumVar
    
    @property
    def Bool_var(self): # add_B_var
        return self._m.BoolVar
    
    @property
    def Int_var(self): # add_I_var
        return self._m.IntVar
    
    @property
    def Minimize(self): # set_objective
        return self._m.Minimize
    
    @property
    def Constr(self): # add_constr
        return self._m.Add
    
    @property
    def _status_dict(self):
        d = {
            0: "OPTIMAL",
            1: "TIME_LIMIT", # feasible, but stopped by limit
            2: "INFEASIBLE",
            4: "ABNORMAL",
            6: "NOT_SOLVED",
        }
        return d