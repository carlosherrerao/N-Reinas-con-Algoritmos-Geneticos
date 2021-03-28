import random
import copy

def imprimir(matriz):
    ganador = ""
    for i in range(len(matriz)):
        if matriz[i][1]==0 and matriz[i][0].count(1)==8:
            ganador = "------- "
        print(str(list(matriz[i][0]))+""+str(matriz[i][1])+" "+  ganador +""+"\n")


def sortSecond(val):
  return val[1] 

def decodificar(lista):
    matriz = []
    matriz.append(lista[0:5])
    matriz.append(lista[5:10])
    matriz.append(lista[10:15])
    matriz.append(lista[15:20])
    matriz.append(lista[20:25])
    return matriz

def contar_Atacados(matriz):
    m= copy.deepcopy(matriz)  
    suma= 0
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j]==1:
                m[i][j]=0
        
                for k in range(len(m)):
                    for l in range(len(m[0])):
                        if k == i and l !=j:
                            if m[k][l] == 1:
                                suma = suma+1
                                m[k][l] = 0
                        if l == j and k != i:
                            if m[k][l] == 1:
                                suma = suma+1
                                m[k][l] = 0
                        if ((k+l == i+j) or (k-l == i-j)):
                            if m[k][l] == 1:
                                suma = suma+1
                                m[k][l] = 0

    return suma 

def evalNQueens(individual):
  size = len(individual)
  diagonal_izquierda_derecha=[0]*(2*size-1)
  diagonal_derecha_izquierda=[0]*(2*size-1)
  
  for i in range (size):
    diagonal_izquierda_derecha[i+individual[i]] += 1
    diagonal_derecha_izquierda[size-1-i+individual[i]] +=1
  suma = 0
  for i in range(2*size-1):
    if diagonal_izquierda_derecha[i]>1:
      suma += diagonal_izquierda_derecha[i] -1
    if diagonal_derecha_izquierda[i]>1:
      suma += diagonal_derecha_izquierda[i] -1
  return suma

def generar_Poblacion(no_individuos):
    individuos =  []
    for i in range(no_individuos):
        #individuo
        individuo = [random.randint(0,1)for _ in range(25)]
        #evaluar
        aptitud = contar_Atacados(decodificar(individuo))
        individuos.append([individuo,aptitud])
        
    return individuos

def seleccion_Torneo(Matriz,no_participantes,no_individuos):
    participantes=[]
  
    #seleccionar aleatoriamente participantes
    for i in range(no_participantes):
        participantes.append(Matriz[random.randint(0,(no_individuos)-1)])
 
    seleccionado = participantes[0]
    numero_reinas = seleccionado[0].count(1)
    i=1
    while i <len(participantes):
        if participantes[i][1]<seleccionado[1] and abs(8-numero_reinas)>abs(8-participantes[i][0].count(1)):
            seleccionado=participantes[i]
        i=i+1
    return seleccionado[0]
def seleccion_Torneo2(Matriz,no_participantes,no_individuos):
    participantes=[]
  
    #seleccionar aleatoriamente participantes
    for i in range(no_participantes):
        participantes.append(Matriz[random.randint(0,(no_individuos)-1)])
 
    seleccionado = participantes[0]
    numero_reinas = seleccionado[0].count(1)
    i=1
    while i <len(participantes):
        n_r_p_i=participantes[i][0].count(1)
        if participantes[i][1]<seleccionado[1] and (n_r_p_i>= numero_reinas and n_r_p_i<=8):
            seleccionado=participantes[i]
        i=i+1
    return seleccionado[0]
def mas_mejor(Matriz):
    mejor = Matriz[0]
    i=0
    while i <len(Matriz):

        if Matriz[i][0].count(1)>mejor[0].count(1) and Matriz[i][1]==mejor[1]:
            mejor =Matriz[i]
        else:
            i=len(Matriz)
        i=i+1
    return mejor

def cruze2punto(p1,p2,nobits):
    numeroaleatorio=random.randint(0,nobits-1)
    numeroaleatorio2=random.randint(numeroaleatorio,nobits-1)
    Hijo=p1[0:numeroaleatorio]+p2[numeroaleatorio:numeroaleatorio2]+p1[numeroaleatorio2:nobits]
    return Hijo

def Mutacion(p1,noBits):

    numeroaleatorio=random.randint(0,(noBits)-1)

    contador=0
      
    for j in range (len(p1)):
        if contador==numeroaleatorio:
          if p1[j]==0:
            p1[j]=1
          else:
            p1[j]=0
        contador=contador+1
    return p1
 
no_Individuos=100
numero_Iteraciones=20
no_participantes= 40
#200 10 20
#Generar y evaluar poblacion
Poblacion_fx=generar_Poblacion(no_Individuos)
imprimir(Poblacion_fx)

iteracion=0

while iteracion < numero_Iteraciones:
    print("ITERACION---------- "+str(iteracion))
    nuevaGeneracion_fx=[]
    for N in range(int(no_Individuos/2)):
        #seleccion padre 1
        padre1 = seleccion_Torneo2(Poblacion_fx,no_participantes,no_Individuos)
        #seleccion padre 2
        padre2 = seleccion_Torneo2(Poblacion_fx,no_participantes,no_Individuos)
        #Cruze
        Hijo1 = cruze2punto(padre1, padre2, 25)
        Hijo2 = cruze2punto(padre1, padre2, 25)
        #Mutacion
        Hijo1 = Mutacion(Hijo1, 25)
        Hijo2 = Mutacion(Hijo2, 25)
        aptitud_Hijo1 = contar_Atacados(decodificar(Hijo1))
        aptitud_Hijo2 = contar_Atacados(decodificar(Hijo2))
        nuevaGeneracion_fx.append([Hijo1,aptitud_Hijo1])
        nuevaGeneracion_fx.append([Hijo2,aptitud_Hijo2])

    #recombinar  
    Poblacion_fx = Poblacion_fx+nuevaGeneracion_fx
    Poblacion_fx.sort(key = sortSecond,reverse=False)  
    Poblacion_fx=Poblacion_fx[0:no_Individuos]
    iteracion=iteracion+1
  
    mejor= mas_mejor(Poblacion_fx)
    if mejor[1]==0 and mejor[0].count(1)==8:
        iteracion=numero_Iteraciones

print("individuo mas optimo = "+str(mejor[0]))
print("aptitud del mas optimo = "+str(mejor[1]))
print("reinas = "+str(mejor[0].count(1)))


