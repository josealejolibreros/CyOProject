from ortools.linear_solver import pywraplp

U=[5, 6, 3, 5,6, 8, 2, 7, 4;
4, 1, 5, 5, 6, 7, 2, 7, 3;
9, 2, 3, 5, 1, 8, 3, 4, 1;
8, 4, 1, 3, 7, 4, 2, 7, 3]

solver = pywraplp.Solver('EjemploLineal',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
cantidadParcelas=4
X=[]
C=[]
for i in range(1,cantidadParcelas):
	x=solver.NumVar(0, m, 'x_'+str(i))
	c=solver.NumVar(0, 1, 'C_'+str(i))
	X.append(x)
	C.append(c)

objective = solver.Objective()
