# -*- coding: utf-8 -*-
class SolutionBuilder(object):
    def __init__(self):
        self.logging = {}
        self.solution = None
    
    def add_solution(self, opt_solver=None):
        if opt_solver.logging["opt_status"] == "INFEASIBLE":
            self.logging = opt_solver.logging["status"]
            self.loggin["opt_status"] = self.logging["opt_status"]
        else:
            if not self.solution:
                self.solution = opt_solver.solution
                self.logging = opt_solver.logging
            else:
                solutions = self.solution
                sol_asset = solutions.get("asset", {})
                sol_grid = solutions.get("grid", {"data": {}})
                sol_net = solutions.get("net", {"data": {}})
                
                new_solution = opt_solver.solution
                new_solution_sol_asset = new_solution.get("asset", {})
                new_solution_sol_grid = new_solution.get("grid", {"data": {}})
                new_solution_sol_net = new_solution.get("net", {"data": {}})
                
                # add asset timeseries data
                for key, item in new_solution_sol_asset.items():
                    for sub_key, sub_item in item.items():
                        new_solution_sol_asset[key][sub_key] = {key: sub_item[key] for key in ["data"]}
                        new_asset_timeseries = new_solution_sol_asset[key][sub_key]["data"]["timeseries"]
                        asset_timeseries = sol_asset[key][sub_key]["data"]["timeseries"]
                        for timeseries_key, timeseries_value in new_asset_timeseries.items():
                            asset_timeseries[timeseries_key].update(timeseries_value)
                
                # add grid timeseries data
                for timeseries_key, timeseries_value in new_solution_sol_grid["data"]["timeseries"].items():
                    grid_timeseries = sol_grid["data"]["timeseries"]
                    grid_timeseries[timeseries_key].update(timeseries_value)
                
                # add network timeseries data
                for key, item in new_solution_sol_net["data"].items():
                    new_solution_net_timeseries = new_solution_sol_net["data"][key]["timeseries"]
                    net_timeseries = sol_net["data"][key]["timeseries"]
                    for timeseries_key, timeseries_value in new_solution_net_timeseries.items():
                        net_timeseries[timeseries_key].update(timeseries_value)