from ortools.linear_solver import pywraplp
<<<<<<< HEAD

=======
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import solver_parameters_pb2
import read_files 
import os
INFINITY = 9999999999
>>>>>>> Minor changes
PATH_TO_FILE = os.path.dirname(os.path.realpath(__file__)) + "\\test.txt"
#Input vars

def get_data():

    input_data_dict = read_files.read_file(PATH_TO_FILE)

    U = input_data_dict["U"]#[[5, 6, 3, 5,6, 8, 2, 7, 4], [4, 1, 5, 5, 6, 7, 2, 7, 3], [9, 2, 3, 5, 1, 8, 3, 4, 1],[ 8, 4, 1, 3, 7, 4, 2, 7, 3]]
    T = input_data_dict["T"]#[3, 2, 1, 3]

    m = input_data_dict["m"]#9
    cantidadParcelas = input_data_dict["P"]#4

    return U, T, m, cantidadParcelas

def model(U, TC, m, cantidadParcelas):
    parameters = pywrapcp.Solver.DefaultSolverParameters()
    solver = pywrapcp.Solver("Test", parameters)
    print(m, " ", cantidadParcelas)
    #Define the variables for the problem
    X=[[]] * cantidadParcelas
    C=[[0] * m] * cantidadParcelas

    for i in range(0, len(X)):
        X[i] = solver.IntVar(0, INFINITY, 'X_'+str(i+1))
        
        for j in range(0, m):
            C[i][j] = solver.BoolVar("C_" + str(i+1) + "_" + str(j+1))

    #Constraints
    for i in range(0, len(X)):
        solver.Add( X[i] + TC[i] - 1 <= m)
    
    for i in range(0, cantidadParcelas):
        for j in range(0, m):
            solver.Add( C[i][j] * j == X[i] )
    
    for j in range(0, m):
        for i in range(0, cantidadParcelas):
            solver.Add( C[i][j] <= 1 )

    other_parcelas = [] * cantidadParcelas
    for i in range(0, cantidadParcelas):
        solver.Add( C[i][j] >= INFINITY * sum( C[i][j] for j in range(0, m) if i is not j ))

    #Objective function
    obj_expr = solver.Objective()
      
    for i in range(0,cantidadParcelas):
        coefficient = 0
        for j in range(0, m):
            coefficient+=U[i][j]
        objective.SetCoefficient(C[i],coefficient)
<<<<<<< HEAD
    #https://developers.google.com/optimization/mip/integer_opt_cp
=======

    obj_expr.SetMaximization()

    vars = []
    for i in range(0, cantidadParcelas):
        for j in range(0, m):
            vars.append(C[i][j])
        vars.append(X[i])
    decision_builder = solver.Phase(vars, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    collector = solver.LastSolutionCollector()
    for v in vars:
        collector.Add(v)

    collector.AddObjective(obj_expr)
    solver.Solve(decision_builder, [obj_expr, collector])

    if collector.SolutionCount() > 0:
        best_solution = collector.SolutionCount() - 1
        print("Objective value:", collector.ObjectiveValue(best_solution))
        print()
        for x in X:
            print('x= ', collector.Value(best_solution, x))

    #https://developers.google.com/optimization/mip/integer_opt_cp
    '''
    solver = pywraplp.Solver('EjemploLineal',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    X=[[]] * cantidadParcelas
    C=[[]] * cantidadParcelas
    
    #Define the variables for the problem
    for i in range(0, len(X)):
        X[i] = solver.IntVar(0.0, solver.infinity(), 'X_'+str(i+1))
        C[i] = solver.BoolVar('C_'+str(i+1))

    #Objective
    objective = solver.Objective()
    objective.SetMaximization()

    #Constraints
    constraints = [0] * cantidadParcelas
    for i in range(0, cantidadParcelas):
        pass
        #constraints[i] = 

    

    X=[]
    C=[]

    for i in range(0,cantidadParcelas):
        x=solver.IntVar(-solver.infinity(),solver.infinity(), 'x_'+str(i+1))
        c=solver.BoolVar('C_'+str(i+1))
        X.append(x)
        C.append(c)

    #Restrictions

    for i in range(0,cantidadParcelas):
        restriction=solver.Constraint(0, m+T[i])
        restriction.SetCoefficient(X[i],1)


    #Objective function
    objective = solver.Objective()

    
    for i in range(0,cantidadParcelas):
        coefficient=0
    for j in range(int(X[i].solution_value()),int(X[i].solution_value())+T[i]+1):
        coefficient+=U[i][j]
    objective.SetCoefficient(C[i],coefficient)
    '''
    return solver


def solve(solver):
    solver.Solve();
    
    for i in range(0,cantidadParcelas):
        print('X',str(i),' =',round(X[i].solution_value()))

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


def main():
    U, T, m, P = get_data()
    solver = model(U, T, m, P)
    solve(solver)

if __name__ == "__main__":
    main()


>>>>>>> Minor changes
