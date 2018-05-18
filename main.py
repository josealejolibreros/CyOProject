from ortools.linear_solver import pywraplp


solver = pywraplp.Solver('EjemploLineal',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
cantidadParcelas=4
X=[]
C=[]
for i in range(1,cantidadParcelas):
	x=solver.NumVar(-solver.infinity(), solver.infinity(), 'x_'+str(i))
	c=solver.NumVar(-solver.infinity(), solver.infinity(), 'C_'+str(i))
	X.append(x)
	C.append(c)

