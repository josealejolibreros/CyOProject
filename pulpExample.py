from pulp import *
import numpy
import math

U=[[5, 1, 1, 1, 1],
[1, 1, 1, 5, 1],
[1, 1, 5, 1, 1]]

T=[2,2,1]

m= 5
cantidadParcelas=3
M=3000000000000000

my_lp_problem = LpProblem("My LP Problem", LpMaximize)

keysParcelas=[]
for i in range(1,cantidadParcelas+1):
    keysParcelas.append(str(i))

keysMeses=[]
for i in range(1,m+1):
    keysMeses.append(str(i))


X =LpVariable.dicts('X', keysParcelas, 1, m, cat='Integer')
C =LpVariable.dicts('C', (keysParcelas,keysMeses), 0, 1, cat='Integer')

# Objective function
objaux=0

aux=U[0][0] * C["1"]["1"] 

for j in range(2,cantidadParcelas+1):
	aux += U[0][j-1] * C["1"][str(j)]

for i in range(2,cantidadParcelas+1):
	for j in range(1,m+1):
		aux += U[i-1][j-1] * C[str(i)][str(j)]

my_lp_problem += aux,"Z"

#

#Restriccion la suma de las filas debe ser uno (una cosecha por parcela)
i = 1
while i <= cantidadParcelas:
	my_lp_problem += lpSum(C[str(i)]) == 1
	i += 1

#restriccion la suma de las columnas, debe ser menor o igual a uno (una cosecha a la vez)
j = 1
while j <= m:
    aux = 0
    i = 1
    while i <= cantidadParcelas:
        aux += C[str(i)][str(j)]
        i += 1
    my_lp_problem += lpSum(aux) <= 1
    j += 1

#
i = 1
while i <= cantidadParcelas:
	my_lp_problem += lpSum(C[str(i)]) == 1
	i += 1

#restriccion las suma de todos los unos (1) debe ser igual al numero de parcelas

aux = 0
j = 1
while j <= m:
    i = 1
    while i <= cantidadParcelas:
        aux += C[str(i)][str(j)]
        i += 1
    j += 1

my_lp_problem += lpSum(aux) == cantidadParcelas


"""
for j in range(1,m+1):
    aux = 0
    for i in range(1,cantidadParcelas+1):
	    aux += C[str(i)][str(j)]
    my_lp_problem += lpSum(aux) <= 1
"""
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
"""
#Restriccion 3 (Xi = j*C_ij)
for i in range(1,cantidadParcelas+1):
	for j in range(1,m+1):
	    my_lp_problem += X[str(i)] == j* C[str(i)][str(j)]
	    #my_lp_problem += X[i] >= j* C[i][j]
        
#Restriction 4 (W_i1 + W_i2 = 1)
for i in range(1,cantidadParcelas+1):
    my_lp_problem += W[str(i)]["0"] + W[str(i)]["1"] == 1
    #my_lp_problem += W[i][1] + W[i][0] >= 1
"""
'''
#restriccion temporal: forzar que X_i y C_ij sea mayor a cero
for i in range(1,cantidadParcelas+1):
	my_lp_problem += X[str(i)] >= 1
	
for i in range(1,cantidadParcelas+1):
	for j in range(1,m+1):
		my_lp_problem += C[str(i)][str(j)] >= 0

'''


print(my_lp_problem)

my_lp_problem.solve()
print(pulp.LpStatus[my_lp_problem.status])

for variable in my_lp_problem.variables():
    print (variable.name + ' '+ str(variable.varValue))

