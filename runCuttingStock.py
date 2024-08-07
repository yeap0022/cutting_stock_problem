import argparse
import package.runEngine as runEngine
import json

def main_execution(file_in: str = None, file_out: str = None):
    # get config params
    # mod_data = runEngine.modData(file_name=file_in)._read_file() # opt_data runEngine.OptData
    
    # create optimization solver
    mod_solver = runEngine.modOptimizer() # opt_solver runEngine.Optimizer()
    
    mod_output = None # doe_output
    
    # 1. read data
    mod_data = runEngine.modData(file_name=file_in).readFile() # opt_data runEngine.OptData
    
    # 2. create model instance
    model = runEngine.Model(solver_type="CBC").generateModel() # opt_model runEngine.OptModel
    
    # 3. create problem instance: add constraints and objective function
    mod_builder = runEngine.modBuilder(obj_data=mod_data, output=None, obj_mod=model).build() # opt_builder runEngine.OptBuilder
    
    # 4. solve optimization
    mod_solver.solveOpt(mod_builder).getSolution(mod_builder) # opt_solver opt_builder
    
    # 5. output to file
    dt_out = runEngine.modWriter(data=mod_data, solution=mod_solver, output=mod_output).outResult(file_out=file_out)
    
    return dt_out


if __name__ == "__main__":
    input_file = "./input/order.xlsx"
    output_file = "./output/result.json"
    
    result = main_execution(file_in=input_file, file_out=output_file)
    
    if result is not None:
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, )
            f.close()
    