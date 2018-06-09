from pulp import *
import numpy
import math

U=[[5, 1, 1, 1, 1],
[1, 1, 1, 5, 1],
[1, 1, 5, 1, 1]]

T=[2,2,1]

m=5
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
W =LpVariable.dicts('W', (keysParcelas,["0","1"]), 0, 1, cat='Integer')

print(X)

# Objective function
objaux=0

aux=U[0][0] * C["1"]["1"] 

for j in range(2,cantidadParcelas+1):
	aux += U[0][j-1] * C["1"][str(j)]

for i in range(2,cantidadParcelas+1):
	for j in range(1,m+1):
		aux += U[i-1][j-1] * C[str(i)][str(j)]

print(my_lp_problem.objective)

my_lp_problem += aux,"Z"


#Restricciones 

#restriccion (duracion)
"""
for i in range(1,cantidadParcelas+1):
	my_lp_problem += (-M*(X[str(i)]+T[i-1]-1)) <= (lpSum(T)-T[i-1]) *  W[str(i)]["0"]
	my_lp_problem += (M*(X[str(i)]+T[i-1]-1)) >= (lpSum(T)-T[i-1]) * W[str(i)]["1"]
"""	

#Restriccion (que cada fila la suma sea 1)
for i in range(1,cantidadParcelas+1):
	my_lp_problem +=lpSum(C[str(i)]) == 1


#Resticcion (que cada columna la suma sea 1)
for j in range(1,m+1):
    aux = 0
    for i in range(1,cantidadParcelas+1):
        aux += C[str(i)][str(j)]
    my_lp_problem += lpSum(aux) <= 1

#Restriccion (la suma de todos los unos da igual al numero de parcelas)
aux = 0
for j in range(1,m+1):
    for i in range(1,cantidadParcelas+1):
        aux += C[str(i)][str(j)]
my_lp_problem += lpSum(aux) == cantidadParcelas

#Restriccion 3  
# ((Xi=j)<=>(C_ij=1)) = 
# (((Xi=j)=>(C_ij=1))^((C_ij=1)=>(Xi=j))) = 
# ((¬(Xi=j)v(C_ij=1))^(¬(C_ij=1)v(Xi=j)))

# Xi==j => boolAux1 = 1
# Xi!=j => boolAux1 = 0 
# Cij_==1 => boolAux2 = 1
# Cij_!=1 => boolAux2 = 0

# (boolAux1 <=> boolAux2) = 
# (boolAux1 => bollAux2) ^ (boolAux2 => bollAux1)
# (¬boolAux1 v bollAux2) ^ (¬boolAux2 v bollAux1)

# and: X1,X2;Y1 = y1>=X1+X2-1; Y1<=X1; Y1<=X2; 0<=Y1<=1
# or: X1,X2;Y1 = Y1<=X1+X2; Y1>=X1; Y1>=X2; 0<=Y1<=1
# not: X1;Y1 = Y1 = 1-X1

# 


for i in range(1,cantidadParcelas+1):
	for j in range(1,m+1):
	    my_lp_problem += X[str(i)] == j*C[str(i)][str(j)]

#Restriction 4 (W_i1 + W_i2 = 1)
"""
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