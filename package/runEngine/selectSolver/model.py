class Model(object):
    def __init__(self, solver_type=None):
        self.params = {
            "solver_type": solver_type,
            "mip_gap": 0.01,
            "time_limit": 60
            }
    
    def generate_model(self):
        solver_type = self.params["solver_type"]
        
        if solver_type == "CBC":
            from .solver_cbc import modelCBC # _OptModelCBC
            
            return modelCBC(params=self.params) # _OptModelCBC
        
        else:
            print("INVALID SOLVER")
