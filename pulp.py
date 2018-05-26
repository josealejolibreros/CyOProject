from pulp import *
import numpy
import math

U=[[1, 2, 3],
[3, 2, 1],
[1, 3, 2]]
T=[1,1,1]

m= 3
cantidadParcelas=3
M=3000000000000000;

my_lp_problem = LpProblem("My LP Problem", LpMaximize)

keysParcelas=[]
for i in range(1,cantidadParcelas+1):
    keysParcelas.append(str(i))
keysMeses=[]
for i in range(1,m+1):
    keysMeses.append(str(i))

#X = LpVariable.matrix("X", list(range(cantidadParcelas)), 0, LpInteger)
X =LpVariable.dicts('X', keysParcelas, lowBound=1, cat='Integer')
#C = LpVariable.matrix("C", numpy.zeros(cantidadParcelas, m), 0, 1, LpInteger)
C =LpVariable.dicts('C', (keysParcelas,keysMeses), 0, 1, cat='Integer')
W =LpVariable.dicts('W', (keysParcelas,["0","1"]), 0, 1, cat='Integer')

print(X)

# Objective function
objaux=0

#for j in range(1,cantidadParcelas+1):
#	objaux += lpDot(list(map(int,C[str(j)])) , U[j-1])
    #objaux += lpDot(C[str(j)] , U[str(j)])
	
#my_lp_problem+= objaux,"Z"

#my_lp_problem += lpSum([lpDot(C[str(j)] , U[j-1]) for j in range(1,cantidadParcelas+1)]), "Z"

aux=U[0][0] * C["1"]["1"] 

for j in range(2,cantidadParcelas+1):
	aux += U[0][j-1] * C["1"][str(j)]

for i in range(2,cantidadParcelas+1):
	for j in range(1,m+1):
		aux += U[i-1][j-1] * C[str(i)][str(j)]

print(my_lp_problem.objective)

my_lp_problem += aux,"Z"


#my_lp_problem += lpSum([pattVars[i]*Pattern.cost for i in Patterns])
# Constraints


#Duracion



for i in range(1,cantidadParcelas+1):
	my_lp_problem += (-M*(X[str(i)]+T[i-1]-1)) <= (lpSum(T)-T[i-1]) *  W[str(i)]["0"]
	my_lp_problem += (M*(X[str(i)]+T[i-1]-1)) >= (lpSum(T)-T[i-1]) * W[str(i)]["1"]
	
	#sum_times=0
	#for n in range(m):
		#if n==i:
		#	n+=1
			
		#else:
		#	sum_times=sum_times+T[n]
		#	number = (sum_times-X[i]+1)*W[i][0]
			
			
			
			
	#comentado ls	
	#my_lp_problem += X[i] <= number
	
	
	#restriction1_1=solver.Constraint(-solver.infinity(),number)
	#restriction1_1.SetCoefficient(X[i],1)
	
	#comentado ls
	#my_lp_problem += number >= X[i]
	
	#restriction1_2=solver.Constraint(number,solver.infinity())
	#restriction1_2.SetCoefficient(X[i],1)


#Restriccion 2 (que cada fila la suma sea 1)
for i in range(1,cantidadParcelas+1):
	#restriction2_1=solver.Constraint(-solver.infinity(),1)
	#restriction2_2=solver.Constraint(1,solver.infinity())
	my_lp_problem +=lpSum(C[str(i)]) == 1
	#my_lp_problem +=lpSum(C[i]) >= 1
	
	
	'''
#columnas suma igual a uno

    

for j in range (1,m+1):
	#columnaux = C["0"][str(j)]
	columnaux=0
	for i in range(1,cantidadParcelas+1):
		#restriction2_1=solver.Constraint(-solver.infinity(),1)
		#restriction2_2=solver.Constraint(1,solver.infinity())
		columnaux += C[str(i)][str(j)]
		
	my_lp_problem += columnaux == 1
		#my_lp_problem +=lpSum(C[str(j)]) == 1
	

'''

#Restriccion 3 (Xi = j*C_ij)
for i in range(1,cantidadParcelas+1):
	for j in range(1,m+1):
	    my_lp_problem += X[str(i)] == j* C[str(i)][str(j)]
	    #my_lp_problem += X[i] >= j* C[i][j]
        
#Restriction 4 (W_i1 + W_i2 = 1)
for i in range(1,cantidadParcelas+1):
    my_lp_problem += W[str(i)]["0"] + W[str(i)]["1"] == 1
    #my_lp_problem += W[i][1] + W[i][0] >= 1
    

'''
#restriccion temporal: forzar que X_i y C_ij sea mayor a cero
for i in range(1,cantidadParcelas+1):
	my_lp_problem += X[str(i)] >= 1
	
for i in range(1,cantidadParcelas+1):
	for j in range(1,m+1):
		my_lp_problem += C[str(i)][str(j)] >= 0

'''

# Constraints
#my_lp_problem += 2 * y <= 25 - x
#my_lp_problem += 4 * y >= 2 * x - 8
#my_lp_problem += y <= 2 * x - 5

print(my_lp_problem)

my_lp_problem.solve()
print(pulp.LpStatus[my_lp_problem.status])

for variable in my_lp_problem.variables():
    print (variable.name + ' '+ str(variable.varValue))
    
