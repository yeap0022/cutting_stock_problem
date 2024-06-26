from abc import ABC, abstractmethod

class SolverABC(ABC): # object
    @abstractmethod
    def __init__(self, params=None):
        self._solver_type = params["solver_type"]
        self._m = None
        
        self.createModel()
        
        self.set_params(params)
        
    
    def __str__(self):
        return "Model"
    
    def set_params(self, params):
        self.SetMIPGap(params["mip_gap"])
        self.SetTimeLimit(params["time_limit"])
        
    @property
    def solver_type(self):
        return self._solver_type
    
    @abstractmethod
    def createModel(self): # create_model
        pass
    
    @abstractmethod
    def optimizeModel(self): # optimize_model
        pass
    
    @abstractmethod
    def GetObjVal(self): # _get_obj_val
        pass
    
    @abstractmethod
    def GetVarVal(self, x): # get_var_val
        pass
    
    @abstractmethod
    def SetMIPGap(self, mip_gap): # _set_mipgap
        pass
    
    @abstractmethod
    def SetTimeLimit(self, time_limit): # _set_time_limit
        pass
    
    @property
    @abstractmethod
    def NumVars(self): # num_vars
        pass
    
    @property
    @abstractmethod
    def NumConstr(self): # num_cons
        pass
    
    @property
    @abstractmethod
    def Num_var(self): # add_C_var
        pass
    
    @property
    @abstractmethod
    def Bool_var(self): # add_B_var
        pass
    
    @property
    @abstractmethod
    def Int_var(self): # add_I_var
        pass
    
    @property
    @abstractmethod
    def Minimize(self): # set_objective
        pass
    
    @property
    @abstractmethod
    def Constr(self): # add_constr
        pass
    
    @property
    @abstractmethod
    def _status_dict(self):
        pass