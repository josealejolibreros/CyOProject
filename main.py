from ortools.linear_solver import pywraplp


#Input vars
U=[[5, 6, 3, 5,6, 8, 2, 7, 4], [4, 1, 5, 5, 6, 7, 2, 7, 3], [9, 2, 3, 5, 1, 8, 3, 4, 1],[ 8, 4, 1, 3, 7, 4, 2, 7, 3]]
T=[3, 2, 1, 3]

m= 9
cantidadParcelas=4

solver = pywraplp.Solver('EjemploLineal',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

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

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))





for i in range(0,cantidadParcelas):
	coefficient=0
	for j in range(int(X[i].solution_value()),int(X[i].solution_value())+T[i]+1):
		coefficient+=U[i][j]
	objective.SetCoefficient(C[i],coefficient)


solver.Solve()

for i in range(0,cantidadParcelas):
	print('X',str(i),' =',round(X[i].solution_value()))

