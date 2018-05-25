from ortools.linear_solver import pywraplp


U=[[1, 2, 3],
[3, 2, 1],
[1, 3, 2]]
T=[1,1,1]

m= 3
cantidadParcelas=3
M=2000;

solver = pywraplp.Solver('EjemploLineal',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

#X=[]

#C=[]

X = [solver.NumVar(0.0,solver.infinity(),'X_'+str(i)) for i in range(cantidadParcelas)]
C = [[solver.BoolVar('C_'+str(i)+'_'+str(j)) for i in range(m)] for j in range(cantidadParcelas)]
W = [[solver.BoolVar('W_'+str(i)+'_'+str(j)) for i in range(2)] for j in range(cantidadParcelas)]






#Restriccion profesor 1 (menor que  mayor que)
for i in range(m):
	sum_times=0
	for n in range(i):
		sum_times=sum_times+T[n]

	number = (sum_times-X[i].solution_value()+1)*W[i][0].solution_value()

	restriction1_1=solver.Constraint(-solver.infinity(),number)
	restriction1_1.SetCoefficient(X[i],1)
	restriction1_2=solver.Constraint(number,solver.infinity())
	restriction1_2.SetCoefficient(X[i],1)


#Restriccion 2 (que cada fila la suma sea 1)
for i in range(1,cantidadParcelas):
	restriction2_1=solver.Constraint(-solver.infinity(),1)
	restriction2_2=solver.Constraint(1,solver.infinity())
	for j in range(1,m):
		restriction2_1.SetCoefficient(C[i][j],1)
		restriction2_2.SetCoefficient(C[i][j],1)

#Restriccion 3 (Xi = j*C_ij)
for i in range(1,cantidadParcelas):
	
	for j in range(1,m):
		restriction3_1=solver.Constraint(-solver.infinity(),j*C[i][j].solution_value())
		restriction3_1.SetCoefficient(X[i],1)
		restriction3_2=solver.Constraint(j*C[i][j].solution_value(),solver.infinity())
		restriction3_2.SetCoefficient(X[i],1)

#Restriction 4 (W_i1 + W_i2 = 1)
for i in range(1,cantidadParcelas):
	restriction4_1=solver.Constraint(-solver.infinity(),1)
	restriction4_1.SetCoefficient(W[i][1],1)
	restriction4_1.SetCoefficient(W[i][0],1)

	restriction4_2=solver.Constraint(1,solver.infinity())
	restriction4_2.SetCoefficient(W[i][1],1)
	restriction4_2.SetCoefficient(W[i][0],1)


objective = solver.Objective()


for i in range(0,cantidadParcelas):
	for j in range(0,m):
		objective.SetCoefficient(C[i][j],U[i][j])

objective.SetMaximization()


for i in range(0,cantidadParcelas):
	for j in range(0,m):
		print(str(X[i].solution_value())+'  ')