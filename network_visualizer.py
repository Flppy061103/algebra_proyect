import tkinter as tk
import time

matriz_C=[[0,1,1],[1,0,1],[1,1,0]]

def multiplicar_matrices(A,B):
    r=[[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j]+=A[i][k]*B[k][j]
    return r

def potencia_matriz(A,n):
    r=[[1 if i==j else 0 for j in range(3)]for i in range(3)]
    for _ in range(n):
        r=multiplicar_matrices(r,A)
    return r

pos_nodos={0:(300,120),1:(150,380),2:(450,380)}

class VisualizadorCaminos:
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("Visualización de Caminos y Matrices - UCI")
        self.ventana.attributes("-fullscreen",True)

        panel=tk.Frame(self.ventana,bg="white")
        panel.pack(fill="both",expand=True)

        panel_izq=tk.Frame(panel,bg="white")
        panel_izq.pack(side="left",fill="both",expand=True)

        self.lienzo=tk.Canvas(panel_izq,bg="white")
        self.lienzo.pack(fill="both",expand=True)

        self.circulos={}
        self.aristas={}
        self.dibujar_grafo()

        self.explicacion=tk.Label(panel_izq,text="",font=("Arial",20),bg="white",wraplength=600,justify="left")
        self.explicacion.pack(pady=5)

        self.info_caminos=tk.Label(panel_izq,text="Caminos generados: 0",font=("Arial",22,"bold"),bg="white")
        self.info_caminos.pack(pady=5)

        controles=tk.Frame(panel_izq,bg="lightgray")
        controles.pack(fill="x")

        tk.Label(controles,text="Nodo origen:",bg="lightgray",font=("Arial",18)).pack(side="left",padx=10)
        self.entrada_origen=tk.Entry(controles,width=5,font=("Arial",18))
        self.entrada_origen.pack(side="left")

        tk.Label(controles,text="n:",bg="lightgray",font=("Arial",18)).pack(side="left",padx=10)
        self.entrada_n=tk.Entry(controles,width=5,font=("Arial",18))
        self.entrada_n.pack(side="left")

        tk.Button(controles,text="Paso a paso",font=("Arial",18),command=self.boton_paso).pack(side="left",padx=20)
        tk.Button(controles,text="Automático",font=("Arial",18),command=self.iniciar_automatico).pack(side="left",padx=20)
        tk.Button(controles,text="Salir",font=("Arial",18),command=self.ventana.destroy).pack(side="right",padx=20)

        panel_der=tk.Frame(panel,bg="white")
        panel_der.pack(side="right",fill="y")

        tk.Label(panel_der,text="Matriz C",font=("Arial",18,"bold"),bg="white").pack(pady=5)
        self.tabla_C=tk.Frame(panel_der,bg="white")
        self.tabla_C.pack()
        self.mostrar_matriz(self.tabla_C,matriz_C)

        tk.Label(panel_der,text="Matriz Cⁿ",font=("Arial",18,"bold"),bg="white").pack(pady=5)
        self.tabla_Cn=tk.Frame(panel_der,bg="white")
        self.tabla_Cn.pack()
        self.mostrar_matriz(self.tabla_Cn,[[0,0,0],[0,0,0],[0,0,0]])

        self.caminos=[]
        self.ind_camino=0
        self.ind_paso=0
        self.lista=False

    def mostrar_matriz(self,contenedor,M):
        for w in contenedor.winfo_children():w.destroy()
        f=("Courier",16,"bold")
        tk.Label(contenedor,text="",font=f,bg="white").grid(row=0,column=0)
        for j in range(3):
            tk.Label(contenedor,text=f"Nodo {j}",font=f,bg="white").grid(row=0,column=j+1)
        for i in range(3):
            tk.Label(contenedor,text=f"Nodo {i}",font=f,bg="white").grid(row=i+1,column=0)
            for j in range(3):
                tk.Label(contenedor,text=str(M[i][j]),font=f,bg="white",padx=10,pady=5,borderwidth=2,relief="solid").grid(row=i+1,column=j+1)

    def dibujar_grafo(self):
        for i in range(3):
            for j in range(i+1,3):
                if matriz_C[i][j]==1:
                    x1,y1=pos_nodos[i]
                    x2,y2=pos_nodos[j]
                    l=self.lienzo.create_line(x1,y1,x2,y2,fill="gray",width=5)
                    self.aristas[(i,j)]=l
                    self.aristas[(j,i)]=l
        for i in range(3):
            x,y=pos_nodos[i]
            c=self.lienzo.create_oval(x-45,y-45,x+45,y+45,fill="lightgray")
            self.lienzo.create_text(x,y,text=str(i),font=("Arial",30))
            self.circulos[i]=c

    def iluminar_nodo(self,n):
        self.lienzo.itemconfig(self.circulos[n],fill="yellow")
        self.lienzo.update()
        time.sleep(0.7)
        self.lienzo.itemconfig(self.circulos[n],fill="lightgray")
        self.lienzo.update()

    def iluminar_arista(self,a,b):
        l=self.aristas[(a,b)]
        self.lienzo.itemconfig(l,fill="red",width=7)
        self.lienzo.update()
        time.sleep(0.7)
        self.lienzo.itemconfig(l,fill="gray",width=5)
        self.lienzo.update()

    def vecinos(self,n):
        return [j for j in range(3) if matriz_C[n][j]==1]

    def generar_caminos(self,o,n):
        c=[[o]]
        for _ in range(n):
            nuevos=[]
            for p in c:
                ult=p[-1]
                for v in self.vecinos(ult):
                    nuevos.append(p+[v])
            c=nuevos
        return c

    def explicar(self,t,tiempo=1.5):
        self.explicacion.config(text=t)
        self.ventana.update()
        time.sleep(tiempo)

    def preparar(self):
        try:
            o=int(self.entrada_origen.get())
            n=int(self.entrada_n.get())
        except:
            self.explicar("Por favor escribe un nodo válido y un número entero.")
            return False
        Cn=potencia_matriz(matriz_C,n)
        self.mostrar_matriz(self.tabla_Cn,Cn)
        self.caminos=self.generar_caminos(o,n)
        self.ind_camino=0
        self.ind_paso=0
        self.lista=True
        self.info_caminos.config(text=f"Caminos generados: {len(self.caminos)}")
        self.explicar(f"Se generaron {len(self.caminos)} caminos de longitud {n} desde el nodo {o}.",3)
        return True

    def iniciar_automatico(self):
        if not self.preparar():return
        total=len(self.caminos)
        for i,c in enumerate(self.caminos,1):
            txt=" → ".join(str(x) for x in c)
            self.explicar(f"Camino {i} de {total}. Este camino pasa por los nodos en este orden: {txt}.",3)
            for paso,(a,b) in enumerate(zip(c,c[1:]),1):
                self.explicar(f"Paso {paso}: avanzamos desde el nodo {a} hacia el nodo {b}.",2.5)
                self.iluminar_arista(a,b)
                self.iluminar_nodo(b)
        self.explicar("Se han mostrado todos los caminos generados.",3)

    def boton_paso(self):
        if not self.lista:
            self.preparar()
            return
        total=len(self.caminos)
        if self.ind_camino>=total:
            self.explicar("Ya se recorrieron todos los caminos.")
            return
        c=self.caminos[self.ind_camino]
        txt=" → ".join(str(x) for x in c)
        if self.ind_paso==0:
            self.explicar(f"Comenzamos el camino {self.ind_camino+1} de {total}. Este camino sigue este orden: {txt}.",3)
            self.ind_paso=1
            return
        if self.ind_paso<=len(c)-1:
            a=c[self.ind_paso-1]
            b=c[self.ind_paso]
            self.explicar(f"Paso {self.ind_paso}: avanzamos desde el nodo {a} hacia el nodo {b}.",2.5)
            self.iluminar_arista(a,b)
            self.iluminar_nodo(b)
            self.ind_paso+=1
            return
        self.explicar("Terminamos este camino. Pulsa de nuevo para continuar.")
        self.ind_camino+=1
        self.ind_paso=0

    def ejecutar(self):
        self.ventana.mainloop()

VisualizadorCaminos().ejecutar()
@Floppy