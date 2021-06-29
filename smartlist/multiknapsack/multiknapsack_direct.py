from mip import Model, xsum, maximize, BINARY
import time
import sys
from collections import Counter
print(sys.version)

NIVELNECESIDAD = 1
NIVELVULNERABILIDAD = 1
NIVELPARTICIPACION = 1
NIVELSTARVING = 1


class Multiknapsack():
    pedidos_ids = []
    beneficios = []
    pesos = []
    precios = []
    cantidades = []
    pesomax = 0
    presupuesto = 0
    cantmax = 0
    chosen = []
    m = Model("knapsack")
    @classmethod
    def set_limits(self, pesomax,presupuesto,cantmax):
        self.pesomax = pesomax
        self.presupuesto = presupuesto
        self.cantmax = cantmax
    @classmethod
    def set_pedidos(self,pedidos_ids,pesos,precios,cantidades):
        self.pedidos_ids = pedidos_ids
        self.pesos = pesos
        self.precios = precios
        self.cantidades = cantidades
        print("INFO PEDIDOS")
        print(self.pesos)
        print(self.precios)
        print(self.cantidades)




    @classmethod
    def calculate_and_set_beneficios(self,necesidades,participaciones,vulnerabilidades,starvings):
        print("yes")
        for i in range(len(necesidades)):
            print("MIS ATRIBUTOS")
            print(necesidades)
            print(participaciones)
            print(vulnerabilidades)
            print(starvings)
            print("benef calculado")

            beneficio = self.beneficio(necesidades[i],participaciones[i],vulnerabilidades[i],starvings[i])
            print(beneficio)
            self.beneficios.append(beneficio)
            print("beneficios")
            print(self.beneficios)

    @classmethod
    def break_down_cantidades(self):
        for i in range(len(self.pedidos_ids)):
            #breakdown
            cantidad = self.cantidades[i]
            if cantidad > 1:
                restante = (cantidad -1)
                #dividimos peso y precio
                peso_unit = float(self.pesos[i]/cantidad)
                precio_unit = int(self.precios[i] / cantidad)
                beneficio = self.beneficios[i]
                #agregamos nuevos pedidos unitarios
                for j in range(restante):
                    new_id = self.pedidos_ids[i]
                    self.pedidos_ids.append(new_id)
                    self.pesos.append(peso_unit)
                    self.precios.append(precio_unit)
                    self.cantidades.append(1)
                    #beneficio tambien
                    self.beneficios.append(beneficio)

                #seteamos nuevas stats de pedido original
                self.pesos[i] = peso_unit
                self.precios[i] = precio_unit
                self.cantidades[i] = 1

    @classmethod
    def beneficio(self, necesidad, vulnerabilidad, participacion, starving):
        return NIVELNECESIDAD * necesidad + NIVELVULNERABILIDAD * vulnerabilidad + NIVELPARTICIPACION * participacion + NIVELSTARVING * starving

    @classmethod
    def get_result(self):
        print("mejor grupo")
        print(self.chosen)
        return self.chosen

    @classmethod
    def calculate_best_group(self):
        I = range(len(self.pesos))
        x = [self.m.add_var(var_type=BINARY) for i in I]
        self.m.objective = maximize(xsum(self.beneficios[i] * x[i] for i in I))
        self.m += xsum(self.pesos[i] * x[i] for i in I) <= float(self.pesomax)
        self.m += xsum(self.precios[i] * x[i] for i in I) <= int(self.presupuesto)
        self.m += xsum(self.cantidades[i] * x[i] for i in I) <= int(self.cantmax)
        self.m.optimize()
        selected = [i for i in I if x[i].x >= 0.99]
        ids_selected = []
        for index in selected:
            ids_selected.append(self.pedidos_ids[index])
        self.chosen = ids_selected







