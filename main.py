from ortools.linear_solver import pywraplp

import read_files 
import os
INFINITY = 9999999999

PATH_TO_FILE = os.path.dirname(os.path.realpath(__file__)) + "\\test.txt"
#Input vars

def get_data():

    input_data_dict = read_files.read_file(PATH_TO_FILE)

    U = input_data_dict["U"]#[[5, 6, 3, 5,6, 8, 2, 7, 4], [4, 1, 5, 5, 6, 7, 2, 7, 3], [9, 2, 3, 5, 1, 8, 3, 4, 1],[ 8, 4, 1, 3, 7, 4, 2, 7, 3]]
    TC = input_data_dict["TC"]#[3, 2, 1, 3]

    m = input_data_dict["m"]#9
    cantidadParcelas = input_data_dict["P"]#4

    return U, TC, m, cantidadParcelas

def model(U, TC, m, cantidadParcelas):
    solver = pywraplp.Solver("Test", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    
    #Define the variables for the problem
    X = [[]] * cantidadParcelas
    C = [[0] * m] * cantidadParcelas
    W = [[]] * cantidadParcelas

    for i in range(cantidadParcelas):
        X[i] = solver.IntVar(0.0, solver.infinity(), 'X_'+str(i+1))
        W[i] = solver.BoolVar('W_'+str(i+1))

    for i in range(cantidadParcelas):
        for j in range(m):
            C[i][j] = solver.BoolVar('C_'+str(i+1)+'_'+str(j+1))
            
            
    #Objective SUM(SUM(U*C))
    objective = solver.Objective()
    for i in range(0,cantidadParcelas):
        for j in range(0,m):
            objective.SetCoefficient(C[i][j],U[i][j])

    objective.SetMaximization()

    #Constraints

    #Xi + TCi <= Xj-Wj OR Xj + TCj <= Xi - Wi ; i!=j
    #Wi + Wj = 1
    for i in range(cantidadParcelas):
        
        for j in range(cantidadParcelas):
            if(i != j):
                constraint1 = solver.Constraint(-solver.infinity(), X[j].solution_value() - W[j].solution_value())
                constraint1.SetCoefficient(X[i], 1)
                constraint1.SetCoefficient(TC[i], 1)
                
                constraint1 = solver.Constraint(-solver.infinity(), X[i].solution_value() - W[i].solution_value())
                constraint1.SetCoefficient(X[j], 1)
                constraint1.SetCoefficient(TC[j], 1)

                constraint3 = solver.Constraint(0, 1)
                constraint3.SetCoefficient(W[i], 1)
                constraint3.SetCoefficient(W[j], 1)
                


    #SUM(ROWS) = 1
    for i in range(cantidadParcelas):
        constraint = solver.Constraint(0, 1)
        for j in range(0, m):
            constraint.SetCoefficient(C[i][j], 1)

    #(Xi = j*C_ij)
    for i in range(cantidadParcelas):
        constraint = solver.Constraint(0, solver.infinity())
        for j in range(m):
            constraint.SetCoefficient(C[i][j], j)


    result_status = solver.Solve()

    #assert result_status == pywraplp.Solver.OPTIMAL

    # The solution looks legit (when using solvers other than
    # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    assert solver.VerifySolution(1e-7, True)
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    # The objective value of the solution.
    print('Optimal objective value = %d' % solver.Objective().Value())
    print()
    # The value of each variable in the solution.
    variable_list = []

    for i in range(cantidadParcelas):
        variable_list.append(X[i])
    for i in range(cantidadParcelas):
        variable_list.append(W[i])

    for i in range(cantidadParcelas):
        for j in range(m):
            variable_list.append(C[i][j])

    for variable in variable_list:
        print('%s = %d' % (variable.name(), variable.solution_value()))


def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


def main():
    U, T, m, P = get_data()
    model(U, T, m, P)

if __name__ == "__main__":
    main()
