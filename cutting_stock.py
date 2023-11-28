# -*- coding: utf-8 -*-
"""

@author: yewming.yeap
"""

from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('CBC')
    
    infinity = solver.infinity()
    
    ## input
    width = [10, 15, 20]
    master_width = 35
    pattern = {0:{}, 1:{}, 2:{}, 3:{}}
    pattern[0] = [10, 10, 10]
    pattern[1] = [10, 10, 15]
    pattern[2] = [15, 15]
    pattern[3] = [15, 20]
    order = [75, 35, 15]
    
    width_s = len(width)
    pattern_s = len(pattern)
    
    cut = {0: {}, 1:{}, 2:{}}
    for i in range(width_s):
        for j in range(pattern_s):
            cut[i][j] = sum(map(lambda x: x==width[i], pattern[j]))
    
    # decision variable
    x = {}
    
    for i in range(pattern_s):
        x[i] = solver.IntVar(0.0, infinity,'x[%d]' % i)
    
    waste = solver.IntVar(0.0, infinity,'waste')
    
    # constraint
    # constraint 1.1
    for i in range(width_s):
        solver.Add(solver.Sum([cut[i][j]*x[j] for j in range(pattern_s)]) >= order[i])
    
    # constraint 1.2
    solver.Add(waste >= solver.Sum([x[i]*(master_width-sum(pattern[i])) for i in range(pattern_s)]))
    
    # objective
    solver.Minimize(solver.Sum([x[i] for i in range(pattern_s)]))
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Problem solved in %f milliseconds' % solver.wall_time(), end='\n')
    
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        for i in range(pattern_s):
            print("Number of Pattern ID %d used: " %(i+1), x[i].solution_value())
        print('Waste paper created: ', waste.solution_value())
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()
