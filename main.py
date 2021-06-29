# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.colorpicker import Color
from kivy.graphics import Rectangle
from kivy.uix.checkbox import CheckBox
from kivy.config import Config
from kivy.event import EventDispatcher
from KivyCalendar import DatePicker
from datetime import date
import datetime
from dbmanagement.post_api import PostAPI
from multiknapsack.multiknapsack_direct import Multiknapsack
from collections import Counter
import numpy as np
import threading
import concurrent.futures
import time
import kivy.app
import plyer
from functools import partial
from kivy.clock import Clock

Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')
Config.write()

post_api = PostAPI

#para guardar variables dentro de la app al crear usuario
class NewUserState(EventDispatcher):
    user_name = StringProperty("nada")
    group_name = StringProperty("nadagrupo")
    birthday = datetime.datetime.now()
    password = StringProperty("nada")
    diseases = []
    conditions = []
    available_conditions = []
    available_diseases = []
    group_code = StringProperty("nada")
    def reset(self):
        self.user_name = StringProperty("nada")
        self.birthday = datetime.datetime.now()
        self.password = StringProperty("nada")
        self.diseases = []
        self.conditions = []
        self.group_code = StringProperty("nada")
    def set_user_name(self,name):
        self.user_name = name
    def set_group_name(self,name):
        self.group_name = name
    def set_birthday(self,birthday):
        self.birthday = birthday
    def set_password (self,password ):
        self.password  = password
    def set_group_code (self,group_code ):
        self.group_code  = group_code
    def set_diseases(self,diseases):
        self.diseases = diseases
        print(diseases)
    def set_conditions(self,conditions):
        self.conditions = conditions
        print(conditions)
    def download_conditions(self):
        self.available_conditions = post_api.get_all_conditions()
    def download_diseases(self):
        self.available_diseases = post_api.get_all_factores()
    def get_user_name(self):
        return self.user_name
    def get_group_name(self):
        return self.group_name
    def get_birthday(self):
        return self.birthday
    def get_password (self):
        return self.password
    def get_group_code (self):
        return self.group_code
    def get_diseases(self):
        return self.diseases
    def get_conditions(self):
        return self.conditions
    def get_available_conditions(self):
        return self.available_conditions
    def get_available_diseases(self):
        return self.available_diseases




#PARA CONSERVAR LOS DAtos relacionados a un usuario ya logueado
class UserState(EventDispatcher):
    user_info = [1, "Gian", "Tryagain03", "1990-05-16", 5, 1,
                 1.0,0.25,0.5,0]  # ID, NOMBRE, CLAVE, FECHANACIMIENTO, GRUPOID, ADMIN, PARTICIPACION, VULNERABILIDAD, STARVING,MOROSIDAD
    group_info = [5, "Melee", "nfnmufornf",1]  # ID, NOMBRE, CLVAE, OWNERID

    #para cuando editamos condiciones y factores de riesgo
    diseases = []
    conditions = []
    available_conditions = []
    available_diseases = []
    checked_conditions = []
    checked_diseases = []
    users_in_group = []
    def reset(self):
        self.user_info = []
        self.group_info = []
        self.diseases = []
        self.conditions = []
        self.users_in_group = []
    def set_user_info(self,info):
        self.user_info = info
    def set_group_info(self,info):
        self.group_info = info
    def get_user_info(self):
        return self.user_info
    def get_group_info(self):
        return self.group_info
    def get_users_in_group(self):
        return self.users_in_group
    def set_diseases(self,diseases):
        self.diseases = diseases
        print(diseases)
    def set_conditions(self,conditions):
        self.conditions = conditions
        print(conditions)
    def download_users_in_group(self):
        self.users_in_group = post_api.get_users_in_my_group_by_group_id(self.user_info[4])
    def download_conditions(self):
        self.available_conditions = post_api.get_all_conditions()
    def download_diseases(self):
        self.available_diseases = post_api.get_all_factores()
    def get_available_conditions(self):
        return self.available_conditions
    def get_available_diseases(self):
        return self.available_diseases
    def download_checked_conditions(self):
        self.checked_conditions= post_api.get_user_conditions(self.user_info[0])

    def download_checked_diseases(self):
        self.checked_diseases= post_api.get_user_diseases(self.user_info[0])

    def get_checked_conditions(self):
        return self.checked_conditions
    def get_checked_diseases(self):
        return self.checked_diseases
    def edit_conditions(self):
        #borro y agrego nuevas
        print("MI INFO Y NUEVAS CONDICIONES")
        print(self.user_info[0])
        print(self.conditions)
        post_api.edit_user_conditions(self.user_info[0],self.conditions)

    def edit_diseases(self):
        #borro y agrego nuevas
        post_api.edit_user_diseases(self.user_info[0],self.diseases)
    def update_vulnerabilidad(self):
        birthday = self.user_info[3]
        self.download_checked_conditions()
        self.download_checked_diseases()
        conditions = self.checked_conditions
        diseases = self.checked_diseases
        new_vulnerabilidad = calcular_vulnerabilidad(birthday,conditions,diseases)
        post_api.update_user_vulnerabilidad(self.user_info[0],new_vulnerabilidad)





#PARA CONSERVAR LOS DATOS DE UN ANUNCIO QUE SE VA CREANDO
class AnuncioNuevoState(EventDispatcher):
    tiendas_disponibles = []
    tiendas = []
    dinero = NumericProperty(0)
    peso = NumericProperty(0)
    cantidad = NumericProperty(0)

    def reset(self):
        self.tiendas = []
        self.dinero = 0
        self.peso = 0
        self.cantidad = 0
    def set_tiendas(self,tiendas):
        self.tiendas = tiendas
    def set_dinero(self,dinero):
        self.dinero = dinero
    def set_peso(self,peso):
        self.peso = peso
    def set_cantidad(self,cantidad):
        self.cantidad = cantidad
    def get_tiendas(self):
        return self.tiendas
    def get_dinero(self):
        return self.dinero
    def get_peso(self):
        return self.peso
    def get_cantidad(self):
        return self.cantidad
    def download_tiendas_disponibles(self):
        self.tiendas_disponibles = post_api.get_all_tiendas()
    def get_tiendas_disponibles(self):
        return self.tiendas_disponibles


#PARA CONSERVAR LOS DATOS DE LOS ANUNCIOS QUE SE VAN GENERANDO DENTRO DEL GRUPO
class AnuncioLoaderState(EventDispatcher):
    mi_anuncio = [] # ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, HORA, MINUTOS, [TIENDAS]
    anuncios  = [] # ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, NOMBRECOMPRADOR, HORA, MINUTOS, [TIENDAS]
    def reset(self):
        self.mi_anuncio =[]
        self.anuncios = []


    def set_mi_anuncio(self,mi_anuncio):
        self.mi_anuncio = mi_anuncio
    def set_anuncios(self,anuncios):
        self.anuncios = anuncios
    def get_mi_anuncio(self):
        return self.mi_anuncio
    def get_anuncios(self):
        return self.anuncios
    def end_mi_anuncio(self):
        post_api.termino_anuncio_by_id(self.mi_anuncio[0])
    def delete_mi_anuncio(self):
        print("MATAMOS ANUNCIO")
        post_api.delete_anuncio_x_tiendas_by_id(self.mi_anuncio[0])
        post_api.delete_anuncio_forced_by_id(self.mi_anuncio[0])


        self.mi_anuncio = []

    def reload(self, userdata):
        self.reset()
        print("MY ID")
        print(userdata.get_user_info()[0])
        result = post_api.get_anuncio_by_compradorid(userdata.get_user_info()[0])
        if result == "ERROR: NO ANUNCIO" or result == "ERROR: NO TIENDAS":
            pass
        else:
            (anuncio_info, tiendas)= result
            self.mi_anuncio = anuncio_info
            self.mi_anuncio.append(tiendas)
        otros_anuncios= post_api.get_anuncios_by_grupoid(userdata.get_user_info()[4],userdata.get_user_info()[0])
        if otros_anuncios == "ERROR: NO ANUNCIO" or result == "ERROR: NO TIENDAS":
            pass
        else:
            for a in otros_anuncios:
                anuncio_info = a[0]
                tiendas = a[1]
                anuncio = anuncio_info
                anuncio.append(tiendas)
                self.anuncios.append(anuncio)

#PARA CONSERVAR LOS DATOS DE MIS PEDIDOS
class MisPedidosLoaderState(EventDispatcher):
    mis_pedidos = [] # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, COMPRADORNOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA, ANUNCIOID,PRECIOFINAL,ELIMINADO,CANTIDADFINAL

    def reset(self):
        self.mis_pedidos = []

    def set_mis_pedidos(self,mis_pedidos):
        self.mis_pedidos = mis_pedidos
    def get_mis_pedidos(self):
        return self.mis_pedidos

    def reload(self, userdata):
        self.reset()
        result = post_api.get_mis_pedidos_with_comprador(userdata.get_user_info()[0])
        if result == "ERROR: NO PEDIDOS":
            pass
        else:
            self.mis_pedidos = result

#PARA CONSERVAR LOS DATOS DE PEDIDOS QUE YO DEBO COMPRAR
class PedidosAComprarLoaderState(EventDispatcher):
    pedidos = [] # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO, PRODUCTOPESO, ENLISTA,ANUNCIOID

    def reset(self):
        self.pedidos = []

    def set_pedidos(self,pedidos):
        self.pedidos = pedidos
    def get_pedidos(self):
        return self.pedidos
    def get_pedidos_on_lista(self):
        pedidos_lista = []
        for p in self.pedidos:
            print("HERE")
            print(p[13])
            if p[13] == "true":
                print("YES")
                pedidos_lista.append(p)
        return pedidos_lista

    #RECARGA PARA PEDIDOS EN TERMINAR OFERTA
    def reload(self, userdata):
        self.reset()
        result = post_api.get_mis_pedidos_with_solicitante_terminaroferta(userdata.get_user_info()[0])
        if result == "ERROR: NO PEDIDOS":
            print("no pedidos")
            pass
        else:
            print("HAY PEDIDOS")
            print(result)
            self.pedidos = result
    # RECARGA PARA PEDIDOS EN PEDIDOS POR COMPRAR
    def reload_pedidos_por_comprar(self, userdata):
        self.reset()
        result = post_api.get_mis_pedidos_with_solicitante_porcomprar(userdata.get_user_info()[0])
        if result == "ERROR: NO PEDIDOS":
            print("no pedidos")
            pass
        else:
            print("HAY PEDIDOS")
            print(result)
            self.pedidos = result


#LOADER CORRESONDIENTE A COBROS/PEDIDOS COMPRADOS
class CobrosLoaderState(EventDispatcher):
    pedidos = [] # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO, PRODUCTOPESO, ENLISTA, PRECIOFINAL

    def reset(self):
        self.pedidos = []
    def set_pedidos(self,pedidos):
        self.pedidos = pedidos
    def get_pedidos(self):
        return self.pedidos
    def get_pedidos_on_lista(self):
        pedidos_lista = []
        for p in self.pedidos:
            pedidos_lista.append(p)
        return pedidos_lista



    #RECARGA PARA COBROS/PEDIDOS EN MENU DE COBROS
    def reload(self, userdata):
        self.reset()
        result = post_api.get_cobros_by_comprador_id(userdata.get_user_info()[0])
        if result == "ERROR: NO PEDIDOS":
            print("no pedidos")
            pass
        else:
            print("HAY PEDIDOS")
            print(result)
            self.pedidos = result

    def borrar_cobros(self,cobrosids):
        #reutilizamos codigo
        post_api.delete_pedidos_by_list_id(cobrosids)

#LOADER DE LAS COMPRAS QUE ESTOY TERMINANDO EN LA VENTANA TERMINARCOMPRAS1
#ASUMIMOS QUE ESTOS PEDIDOS TIENEN LA TIENDAID Y EL ANUNCIOID EN COMUN
class PedidosTerminadosLoaderState(EventDispatcher):
    pedidos_on_lista_selected = []  # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO, PRODUCTOPESO, ENLISTA
    pedidos_on_lista_unselected = []

    pedidos_en_espera = []# ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO, PRODUCTOPESO, ENLISTA, ANUNCIOID

    tiendaid = ""
    anuncioid= ""

    def reset(self):
        self.pedidos_on_lista_selected = []
        self.pedidos_on_lista_unselected = []
        self.pedidos_en_espera = []
        self.tiendaid = ""
        self.anuncioid = ""

    def set_pedidos(self,pedidos1,pedidos2):
        print("PEDIDOS SETEADOS")
        print(pedidos1)
        print(pedidos2)
        self.pedidos_on_lista_selected = pedidos1
        self.pedidos_on_lista_unselected = pedidos2
        #aprovechamos de setear las otras variables
        pedido = ""
        if len(self.pedidos_on_lista_selected) > 0:
            pedido = self.pedidos_on_lista_selected[0]
        if len(self.pedidos_on_lista_unselected) > 0:
            pedido = self.pedidos_on_lista_unselected[0]

        self.tiendaid = int(pedido[5])
        self.anuncioid = int(pedido[14])

    def set_pedidos_selected(self,pedidos):
        self.pedidos_on_lista_selected = pedidos
    def set_pedidos_unselected(self,pedidos):
        self.pedidos_on_lista_unselected = pedidos

    def get_pedidos_selected(self):
        return self.pedidos_on_lista_selected
    def get_pedidos_unselected(self):
        return self.pedidos_on_lista_unselected
    def get_pedidos_en_espera(self):
        return self.pedidos_en_espera

    #recibo lista de precios nuevos para actualizar pedidos a comprados [id, precio] y generar cobros con precio nuevo
    def update_pedidos_selected_with_new_price(self,pedidos_selected,newprices,myid):
        ans= post_api.update_pedidos_comprados_with_id_and_new_price(pedidos_selected,newprices)
        print(ans)

    def update_pedidos_selected_revival(self,pedidos_selected):

        print("ACTUALIZAMOS LOS SIGUIENTE PEDIDO")
        # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA,anuncioid
        print(pedidos_selected)
        ids_pedidos = column(pedidos_selected,0)
        new_prices_unit = column(pedidos_selected, 11)
        new_cants = column(pedidos_selected, 4)
        print(ids_pedidos)
        ans= post_api.update_pedidos_comprados_with_id(ids_pedidos,new_prices_unit,new_cants)
        print(ans)

    #METODO PARA CAMBIAR MOROSIDAD Y PARTICIPACION ASOCIADA A USUARIOS EN PEDIDOS SELECCIONADOS
    def update_usuarios_of_pedidos(self,pedidos_selected):
        first = True
        solicitantes_ids_penalizados = []

        for p in pedidos_selected:
            #actualizamos el ususario comprador una unica vez
            if first:
                first = False
                compradorid = int(p[6])
                print("RESETEAMOS A COMPRADOR")
                print(compradorid)
                post_api.reset_user_morosidad_and_participacion(compradorid)
            #actualizamos a solicitantes
            solicitanteid = int(p[7])
            if solicitanteid not in solicitantes_ids_penalizados:
                print("añadimo morosidad")
                print(solicitanteid)
                solicitante = post_api.add_morosidad_to_user(solicitanteid)
                # ACABAMOS DE BAJAR A NIVEL ESTÁNDAR
                if int(solicitante[9]) >= 5 and int(solicitante[9]) < 10:
                    post_api.set_standard_participacion_to_user(solicitanteid)
                elif int(solicitante[9]) >= 10:

                    edadsolicitante = get_edad(solicitante[3])
                    # ACABAMOS DE BAJAR A NIVEL BAJO SI USUARIO NO ES MEDANAMENTE VULNERABLE
                    if float(solicitante[7]) < 0.5:
                        post_api.set_low_participacion_to_user(solicitanteid)
                solicitantes_ids_penalizados.append(solicitanteid)





    #actualizo/borro pedidos no seleccionados de la tienda visitada
    def delete_pedidos_unselected(self):
        print("BORRAMOS PEDIDOS")
        print(self.pedidos_on_lista_unselected)
        post_api.eliminar_pedidos_by_list_id(column(self.pedidos_on_lista_unselected,0))

    def delete_pedidos_en_espera(self):
        print("tienda id")
        print(self.tiendaid)
        print("anuncioid")
        print(self.anuncioid)
        post_api.eliminar_pedidos_en_espera_by_tienda_and_anuncio(self.tiendaid,self.anuncioid)
    def delete_anuncio_if_all_bought(self):
        print("TODO COMPRADO")
        #ahora si debemos eliminar a los que estan en estado eliminado
        if post_api.check_pedidos_on_list_by_anuncio_id(self.anuncioid) == False:

            print("NO MAS PEDIDOS EN LISTA")
            #calculos de starving
            post_api.refresh_starving_of_solicitantes(self.anuncioid)


            #borramos anuncio, su relacion con las tiendas, y los pedidos que quedaron en espera y/o eliminados
            post_api.delete_anuncio_x_tiendas_by_id(self.anuncioid)
            post_api.delete_anuncio_by_id(self.anuncioid)
            post_api.delete_pedidos_en_espera_by_anuncio_id(self.anuncioid)
            post_api.delete_pedidos_eliminados_by_anuncio_id(self.anuncioid)

    def load_pedidos_en_espera_by_anuncioid_not_in_tiendaid(self):

        result = post_api.get_pedidos_en_espera_by_anuncioid_not_in_tiendaid(self.anuncioid,self.tiendaid)
        if result == "ERROR: NO PEDIDOS":
            print("no pedidos")
            pass
        else:
            self.pedidos_en_espera = result





    def reload(self, userdata):
        self.reset()
        result = post_api.get_mis_pedidos_with_solicitante(userdata.get_user_info()[0])
        if result == "ERROR: NO PEDIDOS":
            print("no pedidos")
            pass
        else:
            print("HAY PEDIDOS")
            print(result)
            self.pedidos = result


#ANUNCIO ESCOGIDO PARA ENCARGAR PRODUCTOS
class AnuncioSelectedState(EventDispatcher):
    anuncio = [22,1,10000,10.0,10,2,10,37,[[2, 'Jumbo', 'supermercado', 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Logo_Jumbo_Cencosud.png'], [9, 'Salcobrand', 'farmacia', 'https://www.mallsyoutletsvivo.cl/vivo-coquimbo/wp-content/uploads/sites/2/2018/06/salcobrand-600x600.png']] ]  # ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, NOMBRECOMPRADOR, HORA, MINUTOS, [TIENDAS]
    tiendas_seleccionadas = [[2, 'Jumbo', 'supermercado', 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Logo_Jumbo_Cencosud.png'], [9, 'Salcobrand', 'farmacia', 'https://www.mallsyoutletsvivo.cl/vivo-coquimbo/wp-content/uploads/sites/2/2018/06/salcobrand-600x600.png']] #ID, NOMBRE, TIPO, LOGO
    carro= [] #[PRODUCTO], CANTIDAD,PRECIO_TOTAL,[USUARIO SOLICITANTE]

    def reset(self):
        self.anuncio =[]
        self.tiendas_seleccionadas = []
        self.carro = []
        self.comprador = []
    def set_anuncio(self,anuncio):
        self.anuncio = anuncio
    def get_anuncio(self):
        return self.anuncio
    def set_tiendas_seleccionadas(self,tiendas_seleccionadas):
        self.tiendas_seleccionadas = tiendas_seleccionadas
    def get_tiendas_seleccionadas(self):
        return self.tiendas_seleccionadas
    def set_carro(self,carro):
        self.carro= carro
    def empty_carro(self):
        self.carro= []
    def get_carro(self):
        return self.carro
    def delete_pedido_from_carro(self,pedido):

        self.carro.remove(pedido)
    def add_to_carro(self,producto, cantidad,precio_total,solicitante):
        #checkeamos si producto ya se encuentra en carro
        productos_carro = column(self.carro,0)
        if producto in productos_carro:
            print("ya tenemos producto ASIQUE SUMAMOS")
            for item in self.carro:
                if item[0] == producto:
                    index = self.carro.index(item)
                    newcantidad = cantidad + item[1]
                    newpreciototal = int((item[2]/item[1])*newcantidad)
                    self.carro[index] = [producto,newcantidad,newpreciototal,solicitante]
                    print("SUMAMOS")
        else:
            self.carro.append([producto,cantidad,precio_total,solicitante])
    #def delete_from_carro(self):
    def carro_has_products(self):
        return len(self.carro)>0
    def get_cantidad_total(self):
        i= 0
        for p in self.carro:
            i = i+ int(p[1])
        return i

class KnapsackLoader(EventDispatcher):
    model = Multiknapsack()
    pedidos = [] # lista de :ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA
    #OJO QUE LOS PESOS Y PRECIOS SON UNITARIOS
    anuncio = []# ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, HORA, MINUTOS, [TIENDAS]
    productos_of_pedidos = []
    usuarios_of_pedidos = []
    def set_anuncio(self,anuncio):
        self.anuncio = anuncio
    def set_pedidos(self,pedidos):
        self.pedidos = pedidos
    def download_data_from_pedidos(self):
        listid_productos = []
        listid_usuarios = []
        for p in self.pedidos:
            listid_productos.append(p[3])
            listid_usuarios.append(p[7])
        print("orden productos")
        print(listid_productos)
        print("usuarios pididendo")
        print(listid_usuarios)
        list_products = post_api.get_multiple_productos_by_id(listid_productos)
        list_users = post_api.get_multiple_usuarios_by_id(listid_usuarios)
        print("extraemos")
        print(list_products)
        #HACEMOS SORTING
        list_products_ordered = []
        list_users_ordered = []

        for i in range(len(listid_productos)):
            for p in list_products:
                print(p)
                if p[0] == listid_productos[i]:
                    list_products_ordered.append(p)
            for u in list_users:
                if u[0] == listid_usuarios[i]:
                    list_users_ordered.append(u)
        print(list_products_ordered)
        print(list_users_ordered)

        self.productos_of_pedidos = list_products_ordered
        self.usuarios_of_pedidos = list_users_ordered



    def calculate_best_group(self):
        self.model.set_limits(float(self.anuncio[3]),int(self.anuncio[2]),int(self.anuncio[4]))
        pesos = column(self.pedidos,12)
        precios = column(self.pedidos,11)
        cantidades = column(self.pedidos,4)
        #multiplicamos por respectivas cantidades
        for i in range(len(precios)):
            precios[i] = precios[i] * cantidades[i]
            pesos[i] = pesos[i] * cantidades[i]
        self.model.set_pedidos(column(self.pedidos,0),pesos,precios,cantidades)
        print("QUE HAY ACA")
        print(self.productos_of_pedidos)
        print(self.usuarios_of_pedidos)

        necesidades = column(self.productos_of_pedidos,6)
        participaciones = column(self.usuarios_of_pedidos,6)
        vulnerabilidades = column(self.usuarios_of_pedidos,7)

        starvings = column(self.usuarios_of_pedidos,8)
        print("STARVINGS VIEJOS")
        print(starvings)
        #PASAMOS LOS STARVINGS POR UNA COLA DE PRIORIDAD PARA MODIFICAR SU VALOR EN EL KNAPSACK
        starvings = edit_starvings_by_queue(starvings)
        print("STARVINGS NUEVOS")
        print(starvings)

        self.model.calculate_and_set_beneficios(necesidades,participaciones,vulnerabilidades,starvings)
        self.model.break_down_cantidades()
        self.model.calculate_best_group()
        return self.model.get_result()
    def update_pedidos(self,idspedidosselect):
        ids_pedidos_updated_normal = [] #ids
        ids_pedidos_updated_altered = []  # ids.cantidad
        ids_pedidos_rest_updated = [] #ids, cantidad (resto)

        ids_distinct = list(dict.fromkeys(idspedidosselect))
        for id_pedido in ids_distinct:
            cantidad_elegida = Counter(idspedidosselect).get(id_pedido)

            #conseguimos cantidad original
            cantidad_original = 0
            for p in self.pedidos:
                if p[0] == id_pedido:
                    print("cantidad original")
                    print(p[4])
                    cantidad_original = p[4]
            resto = cantidad_original - cantidad_elegida
            if cantidad_elegida == cantidad_original:
                ids_pedidos_updated_normal.append(id_pedido)
            else: #se cambio la cantidad
                ids_pedidos_updated_altered.append([id_pedido,cantidad_elegida])
                ids_pedidos_rest_updated.append([id_pedido,resto])

        if len(ids_pedidos_updated_normal) > 0:
            post_api.update_pedidos_enlista_with_multiple_ids(ids_pedidos_updated_normal)

        if len(ids_pedidos_updated_altered) >0:
            post_api.update_pedidos_enlista_with_multiple_ids_and_new_cantidad(ids_pedidos_updated_altered)
            post_api.add_rejected_cantidad_to_wait_list(ids_pedidos_rest_updated)
        #dejamos a los pedidos no seleccionados en ESPERA
        ids_rejected = []
        for id in column(self.pedidos,0):
            if id not in ids_distinct:
                print("completamente rechazado")
                ids_rejected.append(id)
        post_api.update_pedidos_rejected(ids_rejected)

class KnapsackLoaderRest(EventDispatcher):
    model = Multiknapsack()
    pedidos_rest = []
    pedidos_selected = []  # lista de :ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA
    anuncio = []  # ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, HORA, MINUTOS, [TIENDAS]
    anuncioid = ""
    productos_of_pedidos_rest = []
    usuarios_of_pedidos_rest = []
    precio_limit = 0
    peso_limit = 0
    cantidad_limit = 0
    def set_pedidos_rest(self,pedidos_rest):
        self.pedidos_rest = pedidos_rest
        #aprovechamos de conseguir el anuncio id
        if len(self.pedidos_rest) > 0:
            self.anuncioid = self.pedidos_rest[0][14]
    def set_pedidos_selected(self,pedidos_selected):
        self.pedidos_selected = pedidos_selected
    def download_data_from_pedidos(self):
        listid_productos = []
        listid_usuarios = []
        for p in self.pedidos_rest:
            listid_productos.append(p[3])
            listid_usuarios.append(p[7])
        print("orden productos")
        print(listid_productos)
        print("usuarios pididendo")
        print(listid_usuarios)
        list_products = post_api.get_multiple_productos_by_id(listid_productos)
        list_users = post_api.get_multiple_usuarios_by_id(listid_usuarios)
        print("extraemos")
        print(list_products)
        #HACEMOS SORTING
        list_products_ordered = []
        list_users_ordered = []

        for i in range(len(listid_productos)):
            for p in list_products:
                print(p)
                if p[0] == listid_productos[i]:
                    list_products_ordered.append(p)
            for u in list_users:
                if u[0] == listid_usuarios[i]:
                    list_users_ordered.append(u)
        print(list_products_ordered)
        print(list_users_ordered)

        self.productos_of_pedidos_rest = list_products_ordered
        self.usuarios_of_pedidos_rest = list_users_ordered
    def download_anunciodata(self):
        self.anuncio = post_api.get_anuncio_by_id(self.anuncioid)
        print("nuestro anuncio")
        print(self.anuncio)
    def calculate_and_set_limits(self):
        precio_actual = 0
        peso_actual = 0
        cantidad_actual = 0
        for p in self.pedidos_selected:
            print("STATS QUE USAMOS PARA LOS PEDIDOS QUE YA ESTAN LISTOS")
            precio_actual = precio_actual + int(p[11])*int(p[4])
            peso_actual = peso_actual + float(p[12])*int(p[4])
            cantidad_actual = cantidad_actual + int(p[4])
        self.precio_limit = int(self.anuncio[2]) - precio_actual
        self.peso_limit = float(self.anuncio[3]) - peso_actual
        self.cantidad_limit = int(self.anuncio[4]) - cantidad_actual

    def calculate_best_group(self):
        self.model.set_limits(self.peso_limit,self.precio_limit,self.cantidad_limit)
        pesos = column(self.pedidos_rest,12)
        precios = column(self.pedidos_rest,11)
        cantidades = column(self.pedidos_rest,4)
        #multiplicamos por respectivas cantidades
        for i in range(len(precios)):
            precios[i] = precios[i] * cantidades[i]
            pesos[i] = pesos[i] * cantidades[i]
        self.model.set_pedidos(column(self.pedidos_rest,0),pesos,precios,cantidades)
        print(self.productos_of_pedidos_rest)
        print(self.usuarios_of_pedidos_rest)

        necesidades = column(self.productos_of_pedidos_rest,6)
        participaciones = column(self.usuarios_of_pedidos_rest,6)
        vulnerabilidades = column(self.usuarios_of_pedidos_rest,7)
        starvings = column(self.usuarios_of_pedidos_rest,8)
        starvings = edit_starvings_by_queue(starvings)
        self.model.calculate_and_set_beneficios(necesidades,participaciones,vulnerabilidades,starvings)
        self.model.break_down_cantidades()
        self.model.calculate_best_group()
        return self.model.get_result()


    #actualizamos pedidos que estaban en lista de reserva a la lista
    def update_pedidos(self,idspedidosselect):
        ids_pedidos_updated_normal = [] #ids
        ids_pedidos_updated_altered = []  # ids.cantidad
        ids_pedidos_rest_updated = [] #ids, cantidad (resto)
        ids_distinct = list(dict.fromkeys(idspedidosselect))
        for id_pedido in ids_distinct:
            cantidad_elegida = Counter(idspedidosselect).get(id_pedido)
            #conseguimos cantidad original
            cantidad_original = 0
            for p in self.pedidos_rest:
                if p[0] == id_pedido:
                    print("cantidad original")
                    print(p[4])
                    cantidad_original = p[4]
            resto = cantidad_original - cantidad_elegida
            if cantidad_elegida == cantidad_original:
                ids_pedidos_updated_normal.append(id_pedido)
            else: #se cambio la cantidad
                ids_pedidos_updated_altered.append([id_pedido,cantidad_elegida])
                ids_pedidos_rest_updated.append([id_pedido,resto])

        if len(ids_pedidos_updated_normal) > 0:
            post_api.update_pedidos_enlista_with_multiple_ids(ids_pedidos_updated_normal)

        if len(ids_pedidos_updated_altered) >0:
            post_api.update_pedidos_enlista_with_multiple_ids_and_new_cantidad(ids_pedidos_updated_altered)
            post_api.add_rejected_cantidad_to_wait_list(ids_pedidos_rest_updated)
        #dejamos a los pedidos no seleccionados en ESPERA
        ids_rejected = []
        for id in column(self.pedidos_rest,0):
            if id not in ids_distinct:
                print("completamente rechazado")
                ids_rejected.append(id)
        post_api.update_pedidos_rejected(ids_rejected)



#lo que se encarga de cambiar las pantallas
class WindowManager(ScreenManager):
    newuserdata = ObjectProperty(NewUserState())
    userdata = ObjectProperty(UserState())
    newanuncio = ObjectProperty(AnuncioNuevoState())
    comprasdata = ObjectProperty(AnuncioLoaderState())
    mispedidosdata = ObjectProperty(MisPedidosLoaderState())
    pedidosacomprardata = ObjectProperty(PedidosAComprarLoaderState())
    pedidosterminadosdata = ObjectProperty(PedidosTerminadosLoaderState())
    cobrosdata = ObjectProperty(CobrosLoaderState())
    encargodata = ObjectProperty(AnuncioSelectedState())
    knapsackloader = ObjectProperty(KnapsackLoader())
    knapsackloaderrest = ObjectProperty(KnapsackLoaderRest())


class LoginWindow(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)
    main = ObjectProperty(None)

    def try_login(self):
        loading_function(self.try_login_real)


    def try_login_real(self,pop):
        user_name = self.user.text
        password = self.password.text

        user_info = post_api.login(user_name, password)

        print(user_info)
        if user_info == "ERROR: USUARIO NO EXISTE":
            self.reset()
            self.invalidData()
        else:
            # logeo con éxito
            self.reset()
            self.manager.userdata.set_user_info(user_info)
            self.login(user_info)
        pop.dismiss()


    def login(self,user_info):
        group_id = user_info[4]
        group_info = post_api.get_group_via_id(group_id)
        self.manager.userdata.set_group_info(group_info)
        sm.transition = SlideTransition(direction="left")
        sm.current = "menucompras"

    def reset(self):
        self.user.text = ""
        self.password.text = ""

    def invalidData(self):
        pop = LoginFailedPopup()

        pop.open()

class NewUser1Window(Screen):
    pass

class NewUser2Window(Screen):
    pass

class NewUser3Window(Screen):
    newuser_name = ObjectProperty(None)
    newuser_day = ObjectProperty(None)
    newuser_month = ObjectProperty(None)
    newuser_year = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.newuser_name.text = ""
        date = current_date()
        self.newuser_day.text = date[0]
        self.newuser_month.text = date[1]
        self.newuser_year.text = date[2]
    def submit_new_user_data(self):
        if len(self.newuser_name.text) > 3 and len(self.newuser_name.text) < 20 and self.newuser_day.text.isdigit() and self.newuser_month.text.isdigit() and self.newuser_year.text.isdigit() :
            if len(self.newuser_name.text) > 3 \
                    and int(self.newuser_day.text) > 0 and int(self.newuser_day.text) < 32 \
                    and int(self.newuser_month.text) > 0 and int(self.newuser_month.text) < 13 \
                    and int(self.newuser_year.text) > 1900 and int(self.newuser_year.text) < 2010:
                self.gather_go()
            else:
                self.reset()
                self.invalidNewUserData()
        else:
            self.reset()
            self.invalidNewUserData()
    def reset(self):
        self.newuser_name.text = ""
        date = current_date()
        self.newuser_day.text = date[0]
        self.newuser_month.text = date[1]
        self.newuser_year.text = date[2]
    def gather_go(self):
        self.manager.newuserdata.set_user_name(self.newuser_name.text)
        #date
        self.manager.newuserdata.set_birthday(datetime.datetime(int(self.newuser_year.text),int(self.newuser_month.text),int(self.newuser_day.text)).strftime('%Y-%m-%d'))
        self.reset()
        sm.transition = SlideTransition(direction="left")
        sm.current = "newuser3_5"


    def invalidNewUserData(self):
        pop = NewUserIncorrectDateOrName()
        pop.open()

class NewUser3_5Window(Screen):
    newuser_psw= ObjectProperty(None)
    def submit_new_user_data(self):
        if len(self.newuser_psw.text) > 7 and len(self.newuser_psw.text) < 31 :

            self.gather_go()
        else:
            self.reset()
            self.invalidNewUserData()
    def reset(self):
        self.newuser_psw.text = ""
    def gather_go(self):
        self.manager.newuserdata.set_password(self.newuser_psw.text)
        self.reset()
        sm.current = "newuser4"
    def invalidNewUserData(self):
        pop = NewUserIncorrectPassword()
        pop.open()

class NewUser4Window(Screen):
    def next(self):
        loading_function(self.next_real)
    def next_real(self,pop):
        sm.transition = SlideTransition(direction="left")
        sm.current = "newuser5"
        pop.dismiss()


#FORMULARIO LESIONES
class NewUser5Window(Screen):
    conditions = []
    conditions_layout = ObjectProperty(None)
    checklayoutlist = []

    def on_pre_enter(self, *args):
        self.manager.newuserdata.download_conditions()
        self.conditions = self.manager.newuserdata.get_available_conditions()
        self.load_conditions()


    def load_conditions(self):
        self.checklayoutlist = []
        self.conditions_layout.clear_widgets()
        tita = TableLabelTituloA()
        tita.set_text("[b]Condición/Lesión[/b]")
        self.conditions_layout.add_widget(tita)
        titb = TableLabelTituloB()
        titb.set_text("[b]¿Padece?[/b]")
        self.conditions_layout.add_widget(titb)
        for c in self.conditions:
            self.conditions_layout.add_widget(TableLabel(text=str(c[1])))
            check = TableCheck()
            check.set_name(str(c[0]))
            self.conditions_layout.add_widget(check)
            self.checklayoutlist.append(check)


    def check_boxes(self):
        conditions_elegidas = []
        for i in self.checklayoutlist:
            if i.active:
                #geteamos la condicion completa
                for c in self.conditions:
                    if int(c[0]) == int(i.text):
                        conditions_elegidas.append(c)

        #SETEAMOS INFO COMPLETA CON NIVELES
        self.manager.newuserdata.set_conditions(conditions_elegidas)

    def reset(self):
        for i in self.checklayoutlist:
            i.active = False
    def submit_info(self):
        self.check_boxes()
        self.reset()
        sm.current = "newuser6"


class NewUser6Window(Screen):
    def next(self):
        loading_function(self.next_real)
    def next_real(self,pop):
        sm.transition = SlideTransition(direction="left")
        sm.current = "newuser7"
        pop.dismiss()

#FORMULARIO FACTORES DE RIESGO
class NewUser7Window(Screen):
    factores = []
    factores_layout = ObjectProperty(None)
    checklayoutlist = []

    def on_pre_enter(self, *args):
        self.manager.newuserdata.download_diseases()
        self.factores = self.manager.newuserdata.get_available_diseases()
        self.load_factores()

    def load_factores(self):
        self.checklayoutlist = []
        self.factores_layout.clear_widgets()
        tita = TableLabelTituloA()
        tita.set_text("[b]Factor de Riesgo[/b]")
        self.factores_layout.add_widget(tita)
        titb = TableLabelTituloB()
        titb.set_text("[b]¿Padece?[/b]")
        self.factores_layout.add_widget(titb)
        for f in self.factores:
            self.factores_layout.add_widget(TableLabel(text=str(f[1])))
            check = TableCheck()
            check.set_name(str(f[0]))
            self.factores_layout.add_widget(check)
            self.checklayoutlist.append(check)


    def check_boxes(self):
        factores_elegidos = []
        for i in self.checklayoutlist:
            if i.active:
                # geteamos el factor completo
                print("hay factor")
                for f in self.factores:
                    if int(f[0]) == int(i.text):
                        factores_elegidos.append(f)
        # SETEAMOS INFO COMPLETA CON NIVELES
        self.manager.newuserdata.set_diseases(factores_elegidos)

    def reset(self):
        for i in self.checklayoutlist:
            i.active = False

    def submit_info(self):
        self.check_boxes()
        self.reset()
        sm.current = "newuser8"

class NewUser8Window(Screen):
    pass

class NewUserJoin1Window(Screen):
    group_code = ObjectProperty(None)
    def submit_user(self):
        loading_function(self.submit_user_real)

    def submit_user_real(self, pop):
        #checkeamos si codigo existe obteniendo su id
        print(self.group_code.text)
        group_id= post_api.get_group_via_code(self.group_code.text)
        if group_id == "ERROR: NO CODE":
            self.reset()
            self.invalidGroupCode()
        else:
            self.create_and_upload_user_old_group(group_id)
        pop.dismiss()


    def create_and_upload_user_old_group(self,group_id):
        user_name = self.manager.newuserdata.get_user_name()
        password = self.manager.newuserdata.get_password()
        birthday = self.manager.newuserdata.get_birthday()
        #aqui nos importa el id
        diseasesid = column(self.manager.newuserdata.get_diseases(),0)
        conditionsid = column(self.manager.newuserdata.get_conditions(),0)
        conditions = self.manager.newuserdata.get_conditions()
        diseases = self.manager.newuserdata.get_diseases()
        #CALCULAR VULNERABILIDAD
        vulnerabilidad = calcular_vulnerabilidad(birthday,conditions,diseases)


        #CREACION USUARIO
        newuser_id = post_api.add_user_query(user_name, password, birthday, diseasesid, conditionsid, group_id,False,vulnerabilidad)
        self.reset()
        sm.current = "newuserjoin2"


    def reset(self):
        self.group_code.text = ""
    def invalidGroupCode(self):
        pop = GroupNotFoundPopup()
        pop.open()



class NewUserJoin2Window(Screen):
    pass

class NewUserCreate1Window(Screen):
    group_name = ObjectProperty(None)
    def submit_group(self):
        loading_function(self.submit_group_real)

    def submit_group_real(self, pop):
        if len(self.group_name.text) > 3 and len(self.group_name.text) < 20:
            self.create_and_upload_user()
        else:
            self.reset()
            self.invalidNewGroupData()
        pop.dismiss()

    def reset(self):
        self.group_name.text = ""

    def create_and_upload_user(self):
        user_name = self.manager.newuserdata.get_user_name()
        password = self.manager.newuserdata.get_password()
        birthday = self.manager.newuserdata.get_birthday()
        group_name = self.group_name.text

        # aqui nos importa el id
        diseasesid = column(self.manager.newuserdata.get_diseases(), 0)
        conditionsid = column(self.manager.newuserdata.get_conditions(), 0)
        conditions = self.manager.newuserdata.get_conditions()
        diseases = self.manager.newuserdata.get_diseases()

        # CALCULAR VULNERABILIDAD
        vulnerabilidad = calcular_vulnerabilidad(birthday, conditions, diseases)

        #RETORNA EL CODIGO DE GRUPO PARA USAR EN SIGUIENTE VENTANA
        group_code= post_api.create_user_and_group(user_name,password,birthday,diseasesid,conditionsid,group_name,vulnerabilidad)
        self.manager.newuserdata.set_group_code(group_code)

        self.reset()
        sm.current = "newusercreate2"

    def invalidNewGroupData(self):
        pop = GroupNameFailedPopup()

        pop.open()


class NewUserCreate2Window(Screen):
    group_code = ObjectProperty(None)
    def on_pre_enter(self, *args):
        self.group_code.text = self.manager.newuserdata.get_group_code()


class TestSuccess(Screen):
    pass

class MenuComprasWindow(Screen):
    pedidos_grid = ObjectProperty(None)
    button_anuncio = ObjectProperty(None)

    def on_pre_enter(self, *args):
        #show_notification(self)
        loading_function(self.on_pre_enter_real)

    def on_pre_enter_real(self, pop):
        self.pedidos_grid.clear_widgets()
        self.button_anuncio.disabled = False
        self.children[0].add_widget(TopScreenLayout())
        self.manager.comprasdata.reload(self.manager.userdata)
        mi_anuncio = self.manager.comprasdata.get_mi_anuncio() # ID, GRUPOID, PRESUPUESTO, PESOMAX, CANTMAX, COMPRADORID, HORA, MINUTOS, [TIENDAS]
        otros_anuncios= self.manager.comprasdata.get_anuncios()
        print("MI ANUNCIO")
        print(mi_anuncio)
        print(otros_anuncios)

        #DEBEMOS RESETEAR LOS OTROS STATEMANAGERS
        self.manager.newanuncio.reset()
        self.manager.encargodata.reset()
        pop.dismiss()


        #QUIZAS HAYA QUE COMPROBARLO DE OTRA FORMA
        if mi_anuncio == [] and otros_anuncios == []:
            self.load_no_anuncio()
        else:
            self.load_mi_anuncio(mi_anuncio)
            self.load_otros_anuncios(otros_anuncios)


    def load_mi_anuncio(self,mi_anuncio):
        if mi_anuncio != []:
            layout = MiPedidoLayout()
            nombre_comprador = self.manager.userdata.get_user_info()[1]
            hora = mi_anuncio[6]
            minutos = mi_anuncio[7]
            tiendas = mi_anuncio[8]
            for t in tiendas:
                tlabel = TiendaLabel()
                tlabel.set_name(t[1])
                layout.set_tienda(tlabel)
            #TIENE QUE DECIR "MI ANUNCIO"
            #layout.set_name_comprador(nombre_comprador)
            layout.set_time(hora,minutos)
            layout.set_info(mi_anuncio)
            self.pedidos_grid.add_widget(layout)
            # self.pedidos_grid.addwidget()
            #SI TENEMOS UN ANUNCIO, BLOQUEAMOS EL BOTON DE ANUNCIO DE COMPRA
            self.button_anuncio.disabled = True


    def load_otros_anuncios(self,otros_anuncios):
        if otros_anuncios != []:
            for a in otros_anuncios:
                layout = PedidoLayout()
                #atomizar esto
                nombre_comprador = a[6]
                hora = a[7]
                minutos = a[8]
                tiendas = a[9]
                for t in tiendas:
                    tlabel = TiendaLabel()
                    tlabel.set_name(t[1])
                    layout.set_tienda(tlabel)
                layout.set_name_comprador(nombre_comprador)
                layout.set_time(hora, minutos)
                layout.set_info(a)
                self.pedidos_grid.add_widget(layout)

    def load_no_anuncio(self):
        label = NoAnuncios()
        self.pedidos_grid.add_widget(label)


#MIS PEDIDOS
class MenuPedidosAWindow(Screen):
    pedidos_grid = ObjectProperty(None)
    mis_pedidos = []
    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)
    def on_pre_enter_real(self,pop):
        self.pedidos_grid.clear_widgets()
        self.children[0].add_widget(TopScreenLayout())
        solicitanteid = self.manager.userdata.get_user_info()[0]
        self.manager.mispedidosdata.reload(self.manager.userdata)
        mis_pedidos = self.manager.mispedidosdata.get_mis_pedidos()# ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, COMPRADORNOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA, ANUNCIOID,PRECIOFINAL,ELIMINADO,CANTIDADFINAL
        if mis_pedidos == []:
            self.load_no_pedidos()
        else:
            self.mis_pedidos = mis_pedidos
            self.load_mis_pedidos()
        pop.dismiss()


    def load_mis_pedidos(self):
        mis_pedidos = self.mis_pedidos
        compradores = column(mis_pedidos,6)
        compradores = list(dict.fromkeys(compradores))
        #hacer un for por comprador, para eso primero obetenemos los ditintos compradores
        for c in compradores:
            grouplayout = MisPedidosGroupLayout()
            p_total = 0
            comprador_nombre = ""
            #buscamos pedidos que pertenezcan a etse comprador
            for p in mis_pedidos:
                if str(p[6]) == str(c):
                    pedidolayout = MisPedidosPedidoLayout(pedido=p)
                    grouplayout.add_widget(pedidolayout)
                    if int(p[15]) > 0:
                        p_total = p_total + int(p[15])
                    else:
                        p_total = p_total+ int(p[11])*int(p[4])
                    comprador_nombre = str(p[8])



            grouplayout.set_comprador(comprador_nombre)
            grouplayout.set_precio_total(p_total)
            self.pedidos_grid.add_widget(grouplayout)

    def load_no_pedidos(self):
        label = NoMisPedidos()
        self.pedidos_grid.add_widget(label)
    def show_help(self):
        popup = MisPedidosHelpPopup()
        popup.open()




class MenuPedidosBWindow(Screen):
    pedidos_grid = ObjectProperty(None)
    pedidos = []
    pedidos_layouts= []
    pedidos_seleccionados = []
    pedidos_no_seleccionados = []
    pedidos_waiting = []
    popupswarning = []
    ids_productos_checkeadas = []
    new_precios_de_checkeadas = []
    new_cants_de_checkeadas = []
    ids_productos_no_checkeadas = []
    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)
    def on_pre_enter_real(self,pop):
        self.pedidos = []
        self.pedidos_layouts = []
        self.pedidos_seleccionados = []
        self.pedidos_no_seleccionados = []
        self.pedidos_waiting = []
        self.pedidos_grid.clear_widgets()
        self.children[0].add_widget(TopScreenLayout())
        self.manager.pedidosacomprardata.reload_pedidos_por_comprar(self.manager.userdata)
        pedidos = self.manager.pedidosacomprardata.get_pedidos_on_lista()  # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA
        if pedidos == []:
            self.load_no_pedidos()
        else:
            self.pedidos = pedidos
            self.load_pedidos()
        pop.dismiss()
    def load_pedidos(self):
        pedidos = self.pedidos
        tiendas = column(pedidos, 5)
        tiendas = list(dict.fromkeys(tiendas))
        # hacer un for por tienda, para eso primero obetenemos los ditintos tiendas
        for t in tiendas:
            grouplayout = PedidosPorComprarGroupLayout(caller=self)
            grouplayout.clear_pedidos()
            #grouplayout.clear_widgets()
            p_total = 0
            t_nombre = ""
            # buscamos pedidos que pertenezcan a esta tienda
            # conseguimos los ids de cada producto por tienda
            productos_ids = []
            for p in pedidos:
                if str(p[5]) == str(t):
                    print("PEDIDO EN TIENDA")
                    print(p)
                    productos_ids.append(int(p[3]))
            productos_ids = list(dict.fromkeys(productos_ids))
            pseudopedidos_list = []
            for prod_id in productos_ids:
                cantidad = 0
                nombre = "test"
                p_unit = 0
                id = 0
                #conseguimos la info agrupada
                for p in pedidos:
                    if str(p[3]) == str(prod_id):
                        id = int(p[3])
                        nombre = str(p[10])
                        cantidad = cantidad + int(p[4])
                        p_unit = int(p[11])
                        p_total = p_total + (int(p[4])*int(p[11]))
                        #peso_tot = peso_tot + int(12)*int(p[4])
                        t_nombre = str(p[9])
                pseudopedido = [id,nombre,cantidad,p_unit]
                pseudopedidos_list.append(pseudopedido)
            agroupedlayout = PedidosPorComprarAgroupedPedidosLayout(pedidos=pseudopedidos_list)
            agroupedlayout.set_tienda_id(t)
            self.pedidos_layouts.append(agroupedlayout)
            grouplayout.add_widget(agroupedlayout)
            statelayout = PedidosPorComprarTerminarTiendaLayout()

            grouplayout.set_tienda(t_nombre)
            grouplayout.set_tienda_id(t)
            grouplayout.set_precio_total(p_total)
            grouplayout.add_widget(statelayout)
            statelayout.set_button_info(grouplayout)
            self.pedidos_grid.add_widget(grouplayout)
    def load_no_pedidos(self):
        label = NoPedidosPorComprar()
        self.pedidos_grid.add_widget(label)

    #checkeamos que productos fueron checkeados y los que no (entrega dos listas de ids)
    #ta,bien recopilamos info de los inputs
    # OJO, SOLO DEBEMOS CHECKEAR BOXES DE UNA TIENDA NOMAS, NO DE TODO EL MENU
    def check_boxes(self,tiendaid):
        for agroupedlayout in self.pedidos_layouts:
            if str(agroupedlayout.get_tienda_id()) == str(tiendaid):
                peds = agroupedlayout.get_pedidos()
                new_precios_widgets = agroupedlayout.get_pedidos_precio_widgets()
                new_cants_widgets = agroupedlayout.get_pedidos_cantidad_widgets()
                checks = agroupedlayout.get_checks()

                print("LISTAS DE INFO")
                print(new_precios_widgets)
                print(new_cants_widgets)
                print(checks)
                for index, c in enumerate(checks):
                    if c.active:
                        print("hay uno checkeado")
                        # checkear aqui si se ingresa bien o mal precios
                        self.ids_productos_checkeadas.append(c.get_id())
                        self.new_precios_de_checkeadas.append(new_precios_widgets[index])
                        self.new_cants_de_checkeadas.append(new_cants_widgets[index])

                    else:
                        print("hay uno no checkeado")
                        self.ids_productos_no_checkeadas.append(c.get_id())
    def terminar_compras(self,tiendaid):
        pedidos_selected = []
        pedidos_unselected = []
        less_bought = False
        self.ids_productos_checkeadas = []
        self.new_precios_de_checkeadas = []
        self.new_cants_de_checkeadas = []
        self.ids_productos_no_checkeadas = []
        #OJO, SOLO DEBEMOS CHECKEAR BOXES DE UNA TIENDA NOMAS, NO DE TODO EL MENU
        self.check_boxes(tiendaid)
        print("ids de checkeados")
        print(self.ids_productos_checkeadas)
        for index,id in enumerate(self.ids_productos_checkeadas):
            cantidad_comprada = int(self.new_cants_de_checkeadas[index].get_text())
            precio_unit_final = int(self.new_precios_de_checkeadas[index].get_text())
            print("cantidad que compre")
            print(cantidad_comprada)
            for p in self.pedidos:
                print("NUESTROS PEDIDOS")
                print(str(p[3]))
                print(str(id))
                if str(p[3]) == str(id) and p not in pedidos_selected:
                    print("CONSEGUIMOS PEDIDO REAL")
                    #clonamos
                    newp = p.copy()
                    #HAY QUE SABER QUE HACER SI CANTIDAD ES DISTINTA
                    if cantidad_comprada > int(newp[4]):
                        newp[11] = precio_unit_final
                        pedidos_selected.append(newp)
                        cantidad_comprada = cantidad_comprada-int(newp[4])
                        print("aun nos QUEDA CANTIODAD")
                    elif cantidad_comprada == int(newp[4]):
                        newp[11] = precio_unit_final
                        pedidos_selected.append(newp)
                        cantidad_comprada = cantidad_comprada - int(newp[4])
                        print("SE NOS ACABO LA CANTIDAD")
                    elif cantidad_comprada < int(newp[4]) and cantidad_comprada > 0:
                        #WARNING
                        #modificamos cantidad original de pedido
                        cant_ori = int(newp[4])
                        newp[11] = precio_unit_final
                        newp[4] = cantidad_comprada
                        pedidos_selected.append(newp)
                        cantidad_comprada = cantidad_comprada - cant_ori
                        print("HAY QUE RELLENAR LO QUE QUEDA NOMAS")
                    else:
                        pedidos_unselected.append(newp)
                        print("FFFFFFFFFFFFFFF")
            if cantidad_comprada > 0:
                print("ERROR: NO PUYEDE HABER MAS DE LO QUE YA HAY")
                print(cantidad_comprada)
                return None
            elif cantidad_comprada <0:
                less_bought = True
                print("SE COMPRO MENOS")


        #los que no estan en selected simplemnete son unselected
        for index,id in enumerate(self.ids_productos_no_checkeadas):
            for p in self.pedidos:
                if str(p[3]) == str(id) and p not in pedidos_selected and p not in pedidos_unselected:
                    pedidos_unselected.append(p)

        #si bajamos la cantidad de un pseudopedido, hay que preguntar si corremos algoritmo de nuevo

        self.pedidos_seleccionados = pedidos_selected
        self.pedidos_no_seleccionados = pedidos_unselected
        print("PEDIDOS SELECTED")
        print(self.pedidos_seleccionados)
        print("PEDIDOS NO SELECTED")
        print(self.pedidos_no_seleccionados)
        self.manager.pedidosterminadosdata.reset()
        self.manager.pedidosterminadosdata.set_pedidos(self.pedidos_seleccionados, self.pedidos_no_seleccionados)
        self.terminar_compras_2(less_bought)

    def terminar_compras_2(self,less_bought):
        # analizamos los pedidos que no señeccionamos
        if len(self.pedidos_no_seleccionados) > 0:
            popup = TerminarCompraPedidoFallidoGeneralPopup(caller=self)
            popup.open()
        elif less_bought == True:
            popup = TerminarCompraPedidoFallidoGeneralPopup(caller=self)
            popup.open()
        # si no hay no seleccionados, vamos directo a seleccionados
        else:
            self.agregamos_cobros()
    def check_waiting(self):
        self.manager.pedidosterminadosdata.load_pedidos_en_espera_by_anuncioid_not_in_tiendaid()

        self.pedidos_waiting = self.manager.pedidosterminadosdata.get_pedidos_en_espera()
        print("PEDIDOS EN ESPERA")
        print(self.pedidos_waiting)
        if self.pedidos_waiting == []:
            self.agregamos_cobros()
        else:
            popup = AddWaitingPopup(caller=self)
            popup.open()

    def calcular_pedidos_espera(self):
        loading_function(self.calcular_pedidos_espera_real)


    def calcular_pedidos_espera_real(self,pop):
        pedidos_waiting = self.pedidos_waiting
        self.manager.knapsackloaderrest.set_pedidos_rest(pedidos_waiting)
        self.manager.knapsackloaderrest.set_pedidos_selected(self.pedidos_seleccionados)
        self.manager.knapsackloaderrest.download_data_from_pedidos()
        self.manager.knapsackloaderrest.download_anunciodata()
        self.manager.knapsackloaderrest.calculate_and_set_limits()
        idspedidosselect = self.manager.knapsackloaderrest.calculate_best_group()
        self.manager.knapsackloaderrest.update_pedidos(idspedidosselect)
        self.agregamos_cobros()
        pop.dismiss()




    def agregamos_cobros(self):
        # revisamos nuevos precios y cantidades en pedidos
        newprices = []
        newcants = []
        pedidos_selected = []
        #tengo en self.pedidos sleccionados la nueva info


        print("PEDIDOS SELECCIONADOS")
        print(pedidos_selected)
        print(newprices)
        my_id = self.manager.userdata.get_user_info()[0]
        if len(self.pedidos_seleccionados) > 0:
            self.manager.pedidosterminadosdata.update_pedidos_selected_revival(self.pedidos_seleccionados)

            self.manager.pedidosterminadosdata.update_usuarios_of_pedidos(self.pedidos_seleccionados)
        #REVISAR METODOS
        self.manager.pedidosterminadosdata.delete_pedidos_unselected()
        self.manager.pedidosterminadosdata.delete_pedidos_en_espera()
        self.manager.pedidosterminadosdata.delete_anuncio_if_all_bought()
        self.cobros_agregados()

    def go_to_cobros(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menupedidos_c"


    def cobros_agregados(self):
        pop = TerminarCompraSucessPopup(caller=self)
        pop.open()


#cobros=pedidos
class MenuPedidosCWindow(Screen):
    pedidos_grid = ObjectProperty(None)
    pedidos = []
    pedidos_layouts = []

    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)

    def on_pre_enter_real(self, pop):
        self.pedidos = []
        self.pedidos_layouts = []
        self.pedidos_grid.clear_widgets()
        self.children[0].add_widget(TopScreenLayout())
        self.manager.cobrosdata.reload(self.manager.userdata)
        pedidos = self.manager.cobrosdata.get_pedidos_on_lista()  # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA, PRECIOFINAL,ANUNCIOID,CANTIDADFINAL
        if pedidos == []:
            self.load_no_pedidos()
        else:
            self.pedidos = pedidos
            self.load_pedidos()
        pop.dismiss()

    def load_pedidos(self):
        pedidos = self.pedidos
        solicitantes_ids = column(pedidos, 7)
        solicitantes_ids = list(dict.fromkeys(solicitantes_ids))
        # hacer un for por tienda, para eso primero obetenemos los ditintos tiendas
        for s in solicitantes_ids:
            grouplayout = CobrosGroupLayout(caller=self)
            grouplayout.clear_pedidos()
            # grouplayout.clear_widgets()
            p_total = 0
            s_nombre = ""
            # buscamos pedidos que pertenezcan a ese solicitante
            for p in pedidos:
                if str(p[7]) == str(s):
                    pedidolayout = CobrosPedidoLayout(pedido=p)
                    self.pedidos_layouts.append(pedidolayout)
                    grouplayout.add_widget(pedidolayout)
                    grouplayout.add_pedido(pedidolayout,p[0])
                    p_total = p_total + int(p[14])
                    s_nombre = str(p[8])
            statelayout = CobrosTerminarSolicitanteLayout()
            grouplayout.set_solicitante(s_nombre)
            grouplayout.set_precio_total(p_total)
            grouplayout.add_widget(statelayout)
            statelayout.set_button_info(grouplayout)
            self.pedidos_grid.add_widget(grouplayout)
            print("COBROS DE ESTE GRUPO")
            print(grouplayout.cobros_ids)

    def load_no_pedidos(self):
        label = NoCobros()
        self.pedidos_grid.add_widget(label)

    def end_cobros(self,cobros_ids):
        popup = TerminarCobroWarningPopup(caller=self,cobros_ids =cobros_ids)
        popup.open()


    def end_cobros_confirmed(self,cobros_ids):
        self.manager.cobrosdata.borrar_cobros(cobros_ids)
        pop = TerminarCobroSucessPopup(caller=self)
        pop.open()

    def go_to_productos(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menupedidos_b"



    #def back_to_menu(self,instance):
    #    sm.transition = SlideTransition(direction="right")
    #    sm.current = "menupedidos_b"


class MenuGrupoWindow(Screen):
    group_code = ObjectProperty(None)
    group_name = ObjectProperty(None)
    usuarios = []
    usuarios_layout = ObjectProperty(None)
    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)

    def on_pre_enter_real(self,pop):
        self.manager.userdata.download_users_in_group()
        self.usuarios = self.manager.userdata.get_users_in_group()
        self.children[0].add_widget(TopScreenLayout())
        self.group_name.text = sm.userdata.get_group_info()[1]
        self.group_code.text = self.manager.userdata.get_group_info()[2]
        self.load_usuarios()
        pop.dismiss()

    def load_usuarios(self):
        self.usuarios_layout.clear_widgets()
        tita = TableLabelTituloUsuario()
        tita.set_text("[b]Nombre[/b]")
        self.usuarios_layout.add_widget(tita)
        titb = TableLabelTituloUsuario()
        titb.set_text("[b]Rol[/b]")
        self.usuarios_layout.add_widget(titb)
        for u in self.usuarios:
            self.usuarios_layout.add_widget(TableLabelUsuario(text=str(u[1])))
            if u[5] == "true":
                cargo = "admin"
            else:
                cargo = "miembro"
            self.usuarios_layout.add_widget(TableLabelUsuario(text=cargo))



class MenuOpcionesWindow(Screen):
    def on_pre_enter(self, *args):
        self.children[0].add_widget(TopScreenLayout())

    def cerrar_sesion(self):
        popup = CerrarSesionWarningPopup(caller=self)
        popup.open()
    def cerrar_sesion_true(self):
        self.manager.userdata.reset()
        sm.transition = SlideTransition(direction="right")
        sm.current = "login"



#FORMULARIO LESIONES EN EDITAR USUARIO
class OpcionesCondicionesWindow(Screen):
    conditions = []
    conditions_layout = ObjectProperty(None)
    checklayoutlist = []

    def on_pre_enter(self, *args):
        self.manager.userdata.download_conditions()
        self.conditions = self.manager.userdata.get_available_conditions()
        self.load_conditions()
        self.initial_check()

    def load_conditions(self):
        self.checklayoutlist = []
        self.conditions_layout.clear_widgets()
        tita = TableLabelTituloA()
        tita.set_text("[b]Restricción/Lesión[/b]")
        self.conditions_layout.add_widget(tita)
        titb = TableLabelTituloB()
        titb.set_text("[b]¿Padece?[/b]")
        self.conditions_layout.add_widget(titb)
        for c in self.conditions:
            self.conditions_layout.add_widget(TableLabel(text=str(c[1])))
            check = TableCheck()
            check.set_name(str(c[0]))
            self.conditions_layout.add_widget(check)
            self.checklayoutlist.append(check)

    def initial_check(self):
        self.manager.userdata.download_checked_conditions()
        #self.manager.userdata.download_checked_diseases() #para usarlo despues
        conditions_already_checked = self.manager.userdata.get_checked_conditions()
        for c in conditions_already_checked:
            id = c[0]
            for i in self.checklayoutlist:
                if int(id) == int(i.text):
                    i.active = True

    def check_boxes(self):
        conditions_elegidas = []
        for i in self.checklayoutlist:
            if i.active:
                #geteamos la condicion completa
                for c in self.conditions:
                    if int(c[0]) == int(i.text):
                        conditions_elegidas.append(c)

        #SETEAMOS INFO COMPLETA CON NIVELES
        self.manager.userdata.set_conditions(conditions_elegidas)
        self.manager.userdata.edit_conditions()
        #actualizamos vulnerabilidad
        self.manager.userdata.update_vulnerabilidad()

    def reset(self):
        for i in self.checklayoutlist:
            i.active = False
    def submit_info(self):
        self.check_boxes()
        self.reset()
        sm.transition = SlideTransition(direction="right")
        sm.current = "menuopciones"

#FORMULARIO FACTORES EN EDITAR USUARIO
class OpcionesFactoresWindow(Screen):
    factores = []
    factores_layout = ObjectProperty(None)
    checklayoutlist = []

    def on_pre_enter(self, *args):
        self.manager.userdata.download_diseases()
        self.factores = self.manager.userdata.get_available_diseases()
        self.load_factores()
        self.initial_check()

    def load_factores(self):
        self.checklayoutlist = []
        self.factores_layout.clear_widgets()
        tita = TableLabelTituloA()
        tita.set_text("[b]Factor de Riesgo[/b]")
        self.factores_layout.add_widget(tita)
        titb = TableLabelTituloB()
        titb.set_text("[b]¿Padece?[/b]")
        self.factores_layout.add_widget(titb)
        for f in self.factores:
            self.factores_layout.add_widget(TableLabel(text=str(f[1])))
            check = TableCheck()
            check.set_name(str(f[0]))
            self.factores_layout.add_widget(check)
            self.checklayoutlist.append(check)

    def initial_check(self):
        self.manager.userdata.download_checked_diseases()
        #self.manager.userdata.download_checked_diseases() #para usarlo despues
        factores_already_checked = self.manager.userdata.get_checked_diseases()
        for f in factores_already_checked:
            id = f[0]
            for i in self.checklayoutlist:
                if int(id) == int(i.text):
                    i.active = True

    def check_boxes(self):
        factores_elegidas = []
        for i in self.checklayoutlist:
            if i.active:
                #geteamos la condicion completa
                for f in self.factores:
                    if int(f[0]) == int(i.text):
                        factores_elegidas.append(f)

        #SETEAMOS INFO COMPLETA CON NIVELES
        self.manager.userdata.set_diseases(factores_elegidas)
        self.manager.userdata.edit_diseases()
        #actualizamos vulnerabilidad
        self.manager.userdata.update_vulnerabilidad()

    def reset(self):
        for i in self.checklayoutlist:
            i.active = False
    def submit_info(self):
        self.check_boxes()
        self.reset()
        sm.transition = SlideTransition(direction="right")
        sm.current = "menuopciones"



#PROCESO ANUNCIO

class Anuncio1Window(Screen):
    tiendas_layout = ObjectProperty(None)
    tiendas = []
    layoutlist = []

    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)

    def on_pre_enter_real(self, pop):
        self.children[0].add_widget(TopScreenLayout())
        self.manager.newanuncio.download_tiendas_disponibles()
        self.tiendas = self.manager.newanuncio.get_tiendas_disponibles()
        self.load_tiendas()
        pop.dismiss()


    def load_tiendas(self):
        self.layoutlist = []
        self.tiendas_layout.clear_widgets()
        supers = TiendaGrupoLabel()
        supers.set_text("Supermercados")
        self.tiendas_layout.add_widget(supers)
        supergroup = TiendaGrupoLayout()
        for t in self.tiendas:
            if str(t[2]) == "supermercado":
                tlayout = TiendaLayout(tienda=t)
                self.layoutlist.append(tlayout)
                supergroup.add_widget(tlayout)
        self.tiendas_layout.add_widget(supergroup)
        farms = TiendaGrupoLabel()
        farms.set_text("Farmacias")
        self.tiendas_layout.add_widget(farms)
        farmgroup = TiendaGrupoLayout()
        for t in self.tiendas:
            if str(t[2]) == "farmacia":
                tlayout = TiendaLayout(tienda=t)
                self.layoutlist.append(tlayout)
                farmgroup.add_widget(tlayout)
        self.tiendas_layout.add_widget(farmgroup)
        otros = TiendaGrupoLabel()
        otros.set_text("Otros")
        self.tiendas_layout.add_widget(otros)
        otrosgroup = TiendaGrupoLayout()
        for t in self.tiendas:
            if str(t[2]) == "ferretería":
                tlayout = TiendaLayout(tienda=t)
                self.layoutlist.append(tlayout)
                otrosgroup.add_widget(tlayout)
        self.tiendas_layout.add_widget(otrosgroup)

    def check_boxes(self):
        tiendasid = []
        for l in self.layoutlist:
            id  = l.check_box()
            if id != False:
                tiendasid.append(id)
        if tiendasid != []:
            self.manager.newanuncio.set_tiendas(tiendasid)
    def gather_go(self):
        self.check_boxes()
        if self.manager.newanuncio.get_tiendas() != []:
            sm.transition = SlideTransition(direction="left")
            sm.current = "anuncio2"
        else:
            self.invalidData()
    def invalidData(self):
        pop = NewAnuncioNoTiendasPopup()
        pop.open()

class Anuncio2Window(Screen):

    dinero = ObjectProperty(None)
    peso = ObjectProperty(None)
    cantidad = ObjectProperty(None)
    def on_pre_enter(self, *args):
        self.children[0].add_widget(TopScreenLayout())
    def add_dinero(self):
        if self.dinero.text.isdigit():
            newdinero = int(self.dinero.text) + 100
            self.dinero.text = str(newdinero)
    def minus_dinero(self):
        if self.dinero.text.isdigit():
            if int(self.dinero.text) >= 100:
                newdinero = int(self.dinero.text) - 100
                self.dinero.text = str(newdinero)
    def add_peso(self):
        if self.peso.text.isdigit() or isfloat(self.peso.text):
            newpeso = round(float(self.peso.text),1) + 0.1
            self.peso.text = str(round(float(newpeso),1))
    def minus_peso(self):
        if self.peso.text.isdigit() or isfloat(self.peso.text):
            if round(float(self.peso.text),1) >= 0.1:
                newpeso = round(float(self.peso.text),1) - 0.1
                self.peso.text = str(round(float(newpeso),1))
    def add_cantidad(self):
        if self.cantidad.text.isdigit():
            newcantidad = int(self.cantidad.text) + 1
            self.cantidad.text = str(newcantidad)
    def minus_cantidad(self):
        if self.cantidad.text.isdigit():
            if int(self.cantidad.text) >= 1:
                newcantidad = int(self.cantidad.text) - 1
                self.cantidad.text = str(newcantidad)

    def check_compra(self):
        loading_function(self.check_compra_real)

    def check_compra_real(self,pop):
        print("RESTRICCIONES")
        print(self.dinero.text)
        print(self.peso.text)
        print(self.cantidad.text)
        if self.dinero.text.isdigit() and (self.peso.text.isdigit() or isfloat(self.peso.text)) and self.cantidad.text.isdigit():
            if int(self.dinero.text) >= 100 and float(self.peso.text) >= 0.1 and int(self.cantidad.text) >= 1:
                self.confirmar_compra()
            else:
                self.anuncio_failed()
        else:
            self.anuncio_failed()

        pop.dismiss()


    def confirmar_compra(self):
        group_id = self.manager.userdata.get_group_info()[0]
        presupuesto = int(self.dinero.text)
        pesomax = round(float(self.peso.text),1)
        cantmax = int(self.cantidad.text)
        comprador_id = self.manager.userdata.get_user_info()[0]
        tiempo = datetime.datetime.now()
        hora = tiempo.hour
        minutos = tiempo.minute
        #id de tiendas harcodeado
        tiendas = self.manager.newanuncio.get_tiendas()
        post_api.add_anuncio(group_id, presupuesto,pesomax,cantmax,comprador_id,hora,minutos,tiendas)
        self.anuncio_success()
    def back_to_menu(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menucompras"

    def anuncio_success(self):
        pop = NewAnuncioSucessPopup(caller=self)
        pop.open()

    def anuncio_failed(self):
        pop = NewAnuncioInvalidResPopup()
        pop.open()

#PROCESO PEDIDO
class Encargo1Window(Screen):
    tiendas_grid = ObjectProperty(None)
    anuncio = []
    t_checkboxes = []

    def on_pre_enter(self, *args):
        self.children[0].add_widget(TopScreenLayout())
        self.reset()
        self.anuncio = self.manager.encargodata.get_anuncio()
        self.load_tiendas()
    def load_tiendas(self):
        tiendas = self.anuncio[9]
        i = 1
        for t in tiendas:
            id = t[0]
            nombre = t[1] #fetcheamos nombre
            if i%2:
                check = TiendaForEncargoCheckBox1()
                label = TiendaForEncargoLabel1()
            else:
                check = TiendaForEncargoCheckBox2()
                label = TiendaForEncargoLabel2()

            label.set_name(nombre)
            check.set_name(str(id))
            self.t_checkboxes.append(check)
            self.tiendas_grid.add_widget(check)
            self.tiendas_grid.add_widget(label)
            i = i+1
    def reset(self):
        self.tiendas_grid.clear_widgets()
        self.anuncio= []
        self.t_checkboxes =[]


    def check_boxes(self):
        ids_tiendas_seleccionadas = []
        print(self.t_checkboxes)
        for i in self.t_checkboxes:
            if i.active:
                ids_tiendas_seleccionadas.append(i.text)
        tiendas_seleccionadas= []
        for id in ids_tiendas_seleccionadas:
            tiendas = self.anuncio[9]
            for t in tiendas:
                if str(t[0]) == id:
                    tiendas_seleccionadas.append(t)
        self.manager.encargodata.set_tiendas_seleccionadas(tiendas_seleccionadas)
    def gather_go(self):
        self.check_boxes()
        if self.manager.encargodata.get_tiendas_seleccionadas() != []:
            sm.transition = SlideTransition(direction="left")
            sm.current = "encargo2"
        else:
            self.invalidData()
    def invalidData(self):
        pop = NewEncargoNoTiendasPopup()
        pop.open()

class Encargo2Window(Screen):
    productos_grid = ObjectProperty(None)
    carrobut = ObjectProperty(None)
    buscador = ObjectProperty(None)
    productos_grid_list = []
    #guardamos los productos en un buffer
    productos = []


    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)

    def on_pre_enter_real(self, pop):
        self.children[0].add_widget(TopScreenLayout())
        self.reset()
        self.load_productos()
        self.refresh_cant()
        pop.dismiss()

    def reset(self):
        sm.encargodata.empty_carro()
        self.productos_grid.clear_widgets()
        self.productos_grid_list = []
        self.refresh_cant()


    def refresh_cant(self):
        self.carrobut.refresh_cant()

    def load_productos(self,searchword=""):
        tiendas_seleccionadas = self.manager.encargodata.get_tiendas_seleccionadas()
        self.productos = [] #ID, NOMBRE, IMG, PESO, PRECIO, TIENDAID, NECESIDAD, TIENDA[]
        for t in tiendas_seleccionadas:
            tid = t[0]
            print(tid)
            productos_list= post_api.get_productos_by_tienda_id(tid)
            for p in productos_list:
                #linkeamos cada producto con su tienda
                p.append(t)
                self.productos.append(p)
        self.load_productos_widgets()



    def load_productos_widgets(self,searchword=""):
        # checkeamos lo que ya tenemos (en un principio deberia ser nada)
        prods_seleccionados = sm.encargodata.get_carro()
        for prod in self.productos:
            img = prod[2]
            logo = prod[7][3]
            nombre = prod[1]
            nombre_tienda = prod[7][1]
            precio = prod[4]
            peso = prod[3]
            #si hay una searchword, comprobar que calze
            if searchword != "":
                if (str(nombre.lower()).find(searchword.lower()) == -1) and (str(nombre_tienda.lower()).find(searchword.lower()) == -1):
                    continue
            playout = ProductoLayout()
            playout.set_img_source(str(img))
            playout.set_logo_source(str(logo))
            playout.set_nombre(str(nombre))
            playout.set_detalles(str(precio),str(peso))
            playout.set_info(prod)
            print("seleccionado")
            print(prods_seleccionados)
            print(prod)
            playout.refresh_color()
            print(prod)
            self.productos_grid.add_widget(playout)
            self.productos_grid_list.append(playout)

    def show_carro(self):
        pop = CarroPopup(caller=self)
        pop.open()

    def search_productos(self):
        search_text = str(self.buscador.text)
        self.productos_grid.clear_widgets()
        self.productos_grid_list = []
        if not search_text or search_text.isspace():
            self.load_productos_widgets()
        else:
            self.load_productos_widgets(search_text)

    def gather_go(self):
        loading_function(self.gather_go_real)


    def gather_go_real(self,pop):
        #checkeamos si carro tiene productos
        if self.manager.encargodata.carro_has_products():
            sm.transition = SlideTransition(direction="left")
            sm.current = "encargo2"
            pedidos = self.manager.encargodata.get_carro()
            for p in pedidos:
                productoid = p[0][0]
                cantidad = p[1]
                tiendaid = p[0][7][0]
                compradorid = self.manager.encargodata.get_anuncio()[5]
                solicitanteid = self.manager.userdata.get_user_info()[0]
                anuncioid = self.manager.encargodata.get_anuncio()[0]
                post_api.add_pedido(productoid, cantidad, tiendaid, compradorid, solicitanteid,anuncioid)
            self.anuncio_success()
        else:
            self.invalidData()
        pop.dismiss()
    def unselect_producto(self,producto):
        #recargamos numero del boton
        self.refresh_cant()
        for playout in self.productos_grid_list:
            playout.refresh_color()



    def invalidData(self):
        pop = NewEncargoNoProductosPopup()
        pop.open()
    def back_to_menu(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menucompras"

    def anuncio_success(self):
        pop = NewEncargoSucessPopup(caller=self)
        pop.open()

#PROCESO ACEPTAR PEDIDOS
class TerminarOferta1Window(Screen):
    pedidos_grid = ObjectProperty(None)
    montoreal = ObjectProperty(None)
    montomax = ObjectProperty(None)
    cantreal = ObjectProperty(None)
    cantmax = ObjectProperty(None)
    pesoreal = ObjectProperty(None)
    pesomax = ObjectProperty(None)
    monto_real = 0
    monto_max = 0
    cant_real = 0
    cant_max = 0
    peso_real = 0.0
    peso_max = 0.0
    limit_override = False
    pedidos = []
    empty = False
    def on_pre_enter(self, *args):
        loading_function(self.on_pre_enter_real)
    def on_pre_enter_real(self, pop):
        self.pedidos_grid.clear_widgets()
        self.children[0].add_widget(TopScreenLayout())
        self.manager.pedidosacomprardata.reload(self.manager.userdata)
        pedidos = self.manager.pedidosacomprardata.get_pedidos()  # ID, COMPRADO, ESPERA, PRODUCTOID, CANTIDAD, TIENDAID, COMPRADORID, SOLICITANTEID, SOLICITANTENOMBRE, TIENDANOMBRE, PRODUCTONOMBRE,PRODUCTOPRECIO,PRODUCTOPESO, ENLISTA
        print(pedidos)

        if pedidos == []:
            self.empty = True
            self.pedidos_grid.add_widget(NoPedidosRecibidos())
        else:
            self.pedidos = pedidos
            self.load_pedidos()
        self.set_datos()
        self.set_limites()
        pop.dismiss()
    def load_pedidos(self):
        # debemos agrupar pedidos que vayan por el mismo producto
        # Y NO MOSTRAR AL USUARIO
        pedidos = self.pedidos
        tiendas = column(pedidos,5)
        tiendas = list(dict.fromkeys(tiendas))
        p_total_total = 0
        peso_total = 0
        cant_total = 0
        # hacer un for por tienda, para eso primero obetenemos los ditintos tiendas
        for t in tiendas:
            grouplayout = TerminarOfertaGroupLayout()
            p_total = 0
            t_nombre = ""
            # buscamos pedidos que pertenezcan a esta tienda
            #conseguimos los ids de cada producto por tienda
            productos_ids = []
            for p in pedidos:
                if str(p[5]) == str(t):
                    print("PEDIDO EN TIENDA")
                    print(p)
                    productos_ids.append(int(p[3]))

            productos_ids = list(dict.fromkeys(productos_ids))
            print("PRODUCTOS IDS")
            print(productos_ids)
            for prod_id in productos_ids:
                cantidad = 0
                p_unit = 0
                nombre = ""
                agroupedlayout = TerminarOfertaPedidoAgroupedLayout()
                for p in pedidos:
                    if str(p[3]) == str(prod_id):
                        nombre = str(p[10])
                        cantidad = cantidad + int(p[4])
                        p_unit = int(p[11])
                        p_total = p_total + int(p[11])*int(p[4])
                        p_total_total = p_total_total + int(p[11])*int(p[4])
                        peso_total = peso_total + float(p[12]) * int(p[4])  # M
                        cant_total = cant_total + int(p[4])
                        #peso_tot = peso_tot + int(12)*int(p[4])
                        t_nombre = str(p[9])
                agroupedlayout.set_cantidad(cantidad)
                agroupedlayout.set_nombre(nombre)
                agroupedlayout.set_precio(p_unit)
                grouplayout.add_widget(agroupedlayout)

            grouplayout.set_tienda(t_nombre)
            grouplayout.set_precio_total(p_total)
            self.pedidos_grid.add_widget(grouplayout)
        # seteamos precio total
        self.monto_real = p_total_total
        self.cant_real = cant_total
        self.peso_real = round(peso_total, 1)






    def set_datos(self):
        self.montoreal.text ="Monto total: $"+str(self.monto_real)
        self.cantreal.text = "Cantidad: " + str(self.cant_real)
        self.pesoreal.text = "Peso: " + str(self.peso_real)+"kg"
    def set_limites(self):
        #conseguimos los datos de mi anuncio
        mi_anuncio = self.manager.comprasdata.get_mi_anuncio()
        presupuesto = mi_anuncio[2]
        cantmax = mi_anuncio[4]
        pesomax = mi_anuncio[3]
        self.monto_max = int(presupuesto)
        self.cant_max = int(cantmax)
        self.peso_max = float(pesomax)
        self.montomax.text = "Monto max: $"+str(self.monto_max)
        self.cantmax.text = "Cant max: " + str(self.cant_max)
        self.pesomax.text = "Peso max: " + str(self.peso_max)+"kg"
        if self.monto_max < self.monto_real:
            #nos pasamos
            self.limit_override = True
            self.montomax.color = (240/255,58/255,71/255)
        else:
            self.montomax.color = (91/255,183/255,55/255)
        if self.cant_max < self.cant_real:
            # nos pasamos
            self.limit_override = True
            self.cantmax.color = (240/255,58/255,71/255)
        else:
            self.cantmax.color = (91/255,183/255,55/255)
        if self.peso_max < self.peso_real:
            # nos pasamos
            self.limit_override = True
            self.pesomax.color = (240/255,58/255,71/255)
        else:
            self.pesomax.color = (91/255,183/255,55/255)
    def confirm_list(self):
        if self.limit_override == False:
            print("yesy")
            self.end_oferta()

        else:
            self.warning()


    def back_to_menu(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menupedidos_b"

    def end_oferta(self):
        loading_function(self.end_oferta_real)


    def end_oferta_real(self,popext):
        #CAMBIAMOS FLAGS DE PEDIDOS EN BBDD
       #OJO: CAMBIAMOS TODOS LOS PEDIDOS ASOCIADOS A MI ID EN COMPRADOR ID SUPONIENDO QUE UNA PERSONA SOLO PUEDE HACER 1 ANUNCIO AL MISMO TIEMPO
        #ACA DEBEMOS CORRER EL ALGORITMO
        if self.pedidos != []:
            self.manager.knapsackloader.set_pedidos(self.pedidos)
            self.manager.knapsackloader.set_anuncio(self.manager.comprasdata.get_mi_anuncio())
            self.manager.knapsackloader.download_data_from_pedidos()
            idspedidosselect = self.manager.knapsackloader.calculate_best_group()
            print(idspedidosselect)
            # QUE HACEMOS SI PRODUCTOS PIERDEN CANTIDAD
            self.manager.knapsackloader.update_pedidos(idspedidosselect)
            self.manager.comprasdata.end_mi_anuncio()
            pop = EndOfertaSucessPopup(caller=self)

            pop.open()
        else:#en caso de que no hayan pedidos
            self.manager.comprasdata.delete_mi_anuncio()
            print("NO HAY NADAAAAAA")
            pop = EndOfertaSucessNoPedidosPopup(caller=self)
            pop.open()

        popext.dismiss()

    def warning(self):
        # MENSAJE DE ADVERTENCIA
        pop = TerminarOfertaWarningPopup(caller=self)
        limitlist = []
        if self.monto_max < self.monto_real:
            limitlist.append("monto")
        if self.cant_max < self.cant_real:
            limitlist.append("cantidad")
        if self.peso_max < self.peso_real:
            limitlist.append("peso")
        pop.set_limits(limitlist)
        pop.open()
    def back_to_menu(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menucompras"


#PROCESO TERMINAR COMPRAS
class TerminarCompras1Window(Screen):
    pedidos_grid = ObjectProperty(None)
    #son independientes, pero hay que tener referencia
    pedidos_seleccionados_grid = None
    pedidos_no_seleccionados_grid = None
    limit_override = False
    pedidos_seleccionados = []
    pedidos_no_seleccionados = []
    pedidos_waiting = []
    popupswarning = []

    def on_pre_enter(self, *args):
        self.pedidos_grid.clear_widgets()
        self.pedidos_seleccionados = []
        self.pedidos_no_seleccionados = []
        self.pedidos_waiting = []
        #self.manager.pedidosterminadosdata.reset()
        self.children[0].add_widget(TopScreenLayout())
        self.pedidos_seleccionados = self.manager.pedidosterminadosdata.get_pedidos_selected()
        self.pedidos_no_seleccionados = self.manager.pedidosterminadosdata.get_pedidos_unselected()
        print(self.pedidos_seleccionados)
        self.load_pedidos()


    def load_pedidos(self):
        if len(self.pedidos_seleccionados) > 0:
            print("SELECCIONADOS")
            initiallabel = TerminarComprasInitialLabel()
            self.pedidos_seleccionados_grid = PedidosSeleccionadosTerminarComprasLayout(pedidos = self.pedidos_seleccionados)
            self.pedidos_grid.add_widget(initiallabel)
            self.pedidos_grid.add_widget(self.pedidos_seleccionados_grid)

        if len(self.pedidos_no_seleccionados) > 0:
            print("NOSELECCIONADOS")
            warninglabel = TerminarComprasWarningLabel()
            self.pedidos_no_seleccionados_grid = PedidosNoSeleccionadosTerminarComprasLayout(pedidos=self.pedidos_no_seleccionados)
            self.pedidos_grid.add_widget(warninglabel)
            self.pedidos_grid.add_widget(self.pedidos_no_seleccionados_grid)




    def sacamos_popup(self):
        self.popupswarning.pop(0)

    def terminar_compras(self):
        # analizamos los pedidos que no señeccionamos
        if len(self.pedidos_no_seleccionados) > 0:
            for p in self.pedidos_no_seleccionados:
                popup = TerminarCompraPedidoFallidoPopup(pedido=p, caller=self)
                self.popupswarning.append(popup)
            primero = self.popupswarning[0]
            primero.open()


        #si no hay no seleccionados, vamos directo a seleccionados
        else:
            self.agregamos_cobros()

    def continuar_con_no_seleccionados(self):
        if len(self.popupswarning) > 0:
            primero = self.popupswarning[0]
            primero.open()
        else:
            #VER COMO IMPLEMENTAR LISTA DE ESPERA
            self.manager.pedidosterminadosdata.load_pedidos_en_espera_by_anuncioid_not_in_tiendaid()
            self.pedidos_waiting = self.manager.pedidosterminadosdata.get_pedidos_en_espera()
            if self.pedidos_waiting == []:
                self.agregamos_cobros()
            else:
                popup = AddWaitingPopup(caller=self)
                popup.open()
            #checkeamos si hay pedidos en lista de espera
            #si se desea agregar nuevas cosas, primero eliminamos lo que no se seleccionó,
            #y despues usamos un knapsack loader con las restricciones nuevas
    def calcular_pedidos_espera(self):
        pedidos_waiting= self.pedidos_waiting
        self.manager.knapsackloaderrest.set_pedidos_rest(pedidos_waiting)
        self.manager.knapsackloaderrest.set_pedidos_selected(self.pedidos_seleccionados)
        self.manager.knapsackloaderrest.download_data_from_pedidos()
        self.manager.knapsackloaderrest.download_anunciodata()
        self.manager.knapsackloaderrest.calculate_and_set_limits()
        idspedidosselect = self.manager.knapsackloaderrest.calculate_best_group()
        self.manager.knapsackloaderrest.update_pedidos(idspedidosselect)
        if idspedidosselect == []:
            pop = AddWaitingListFailedPopup(caller=self)
            pop.open()
        self.agregamos_cobros()

    def agregamos_cobros(self):
        # revisamos nuevos precios en pedidos
        newprices = []
        pedidos_selected = []
        if self.pedidos_seleccionados_grid != None:
            for pnewp in self.pedidos_seleccionados_grid.get_pedidos_widgets():

                id_pedido = pnewp.get_id()
                new_precio = pnewp.get_text()
                if isint(new_precio) == False:
                    self.precios_invalidos()
                    return None
                # conseguimos pedido usando su id
                pedido = None
                for p in self.pedidos_seleccionados:
                    if p[0] == id_pedido:
                        pedido = p
                        break
                newprices.append(new_precio)
                pedidos_selected.append(pedido)
        if len(pedidos_selected) > 0:
            print(pedidos_selected)
            # actualizamos pedidos y creamos cobros con nuevos precios
            my_id = self.manager.userdata.get_user_info()[0]
            print("PEDIDOS SELECCIONADOS")
            print(pedidos_selected)
            print(newprices)
            self.manager.pedidosterminadosdata.update_pedidos_selected_with_new_price(pedidos_selected, newprices, my_id)
            print("ACTUALIZAMOS USUARIOS")
            self.manager.pedidosterminadosdata.update_usuarios_of_pedidos(pedidos_selected)

        self.manager.pedidosterminadosdata.delete_pedidos_unselected()
        self.manager.pedidosterminadosdata.delete_pedidos_en_espera()
        self.manager.pedidosterminadosdata.delete_anuncio_if_all_bought()
        self.cobros_agregados()



    def precios_invalidos(self):
        pop = Popup(title='Datos inválidos',
                            content=Label(
                                text='->Los precios ingresados no son números enteros.',
                                halign='center'),
                            size_hint=(0.8, 0.6))

        pop.open()

    def cobros_agregados(self):
        pop = Popup(title='Listo',
                            content=Label(
                                text='Para recordar cuanto debe cobrar\nrecuerde usar el menu de cobros.',
                                halign='center'),
                            size_hint=(0.8, 0.6), on_dismiss=self.back_to_menu)

        pop.open()
    def back_to_menu(self,instance):
        sm.transition = SlideTransition(direction="right")
        sm.current = "menupedidos_c"


#-------------------------------------BOTONES----------------------------------------------

class MenuButton(Button):
    def go_to_menugrupo(self):

        sm.transition = FadeTransition()
        sm.current = "menugrupo"
        sm.transition = SlideTransition()
    def go_to_menucompras(self):
        sm.transition = FadeTransition()
        sm.current = "menucompras"
        sm.transition = SlideTransition()
    def go_to_menupedidos(self):
        sm.transition = FadeTransition()
        sm.current = "menupedidos_a"
        sm.transition = SlideTransition()
    def go_to_menuopciones(self):
        sm.transition = FadeTransition()
        sm.current = "menuopciones"
        sm.transition = SlideTransition()

class MenuPedidosButton(Button):
    def go_to_menupedidos_a(self):
        sm.transition = FadeTransition()
        sm.current = "menupedidos_a"
        sm.transition = SlideTransition()
    def go_to_menupedidos_b(self):
        sm.transition = FadeTransition()
        sm.current = "menupedidos_b"
        sm.transition = SlideTransition()
    def go_to_menupedidos_c(self):
        sm.transition = FadeTransition()
        sm.current = "menupedidos_c"
        sm.transition = SlideTransition()

class EncargarProductosButton(Button):
    info_anuncio = []
    def set_info_anuncio(self,info_anuncio):
        self.info_anuncio = info_anuncio
    def go_to_encargo(self):
        #hacer cosas con info_anuncio
        print(self.info_anuncio)
        #PUEDO ACCEDER A MANAGER A TRAVES DE SM
        sm.encargodata.set_anuncio(self.info_anuncio)
        sm.transition = SlideTransition(direction="left")
        sm.current = "encargo1"


class TerminarOfertaButton(Button):
    info_anuncio = []

    def set_info_anuncio(self, info_anuncio):
        self.info_anuncio = info_anuncio

    def go_to_oferta(self):
        # hacer cosas con info_anuncio

        sm.transition = SlideTransition(direction="left")
        sm.current = "terminaroferta1"

class TerminarComprasEnTiendaButton(Button):
    layout = ObjectProperty(None)
    def set_layout(self,layout):
        self.layout = layout
    def go_to_terminar_compras(self):
        print("llamamos a papa")
        self.layout.go_to_terminar_compras()

class TerminarCobrosSolicitanteButton(Button):
    layout = ObjectProperty(None)
    def set_layout(self,layout):
        self.layout = layout
    def end_cobros(self):
        print("llamamos a papa")
        self.layout.end_cobros()


class ProductoClickButton(Button):
    info_producto = []
    def set_info_producto(self,info_producto):
        self.info_producto = info_producto
    def pop_up_producto(self):
        #guardamso referencia a layout
        pop = ProductoPopup(caller=self.parent)
        nomb_producto = self.info_producto[1]
        precio = self.info_producto[4]
        pop.set_title(nomb_producto)
        pop.set_cantidad(1)
        pop.set_precio(precio)
        pop.set_info(self.info_producto)
        print("POP")
        pop.open()
class CarroBut(Button):
    cant = ObjectProperty(None)
    def refresh_cant(self):
        self.cant.text = str(sm.encargodata.get_cantidad_total())





#-------------------------------------LAYOUTS----------------------------------------------
#LAYOUT QUE VA ARRIBA DE LÑA PANTALLA CON NOMBRES DE USUSARIO Y GRUPO
class TopScreenLayout(GridLayout):
    group_name = ObjectProperty(None)
    user_name = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TopScreenLayout, self).__init__()
        self.set_info()


    def set_group_name(self,name):
        self.group_name.text = "[b]Grupo[/b]: "+ str(name)
    def set_user_name(self,name):
        self.user_name.text = "[b]Usuario[/b]: "+ str(name)
    def set_info(self):
        self.set_group_name(sm.userdata.get_group_info()[1])
        self.set_user_name(sm.userdata.get_user_info()[1])






class PedidoLayout(FloatLayout):
    comprador_nombre = ObjectProperty(None)
    hora_anuncio= ObjectProperty(None)
    tiendas_grid= ObjectProperty(None)
    button= ObjectProperty(None)
    def set_name_comprador(self,name_comprador):
        self.comprador_nombre.text = "[b]Comprador: [/b]" +name_comprador
    def set_time(self,hora,minutos):
        if len(str(minutos)) >1:
            self.hora_anuncio.text = "[b]Hora anuncio: [/b]" + str(hora)+":"+str(minutos)
        else:
            self.hora_anuncio.text = "[b]Hora anuncio: [/b]" + str(hora) + ":0" + str(minutos)

    def set_tienda(self,tiendalabel):
        self.tiendas_grid.add_widget(tiendalabel)
    def set_info(self,anuncio):
        self.button.set_info_anuncio(anuncio)


class MiPedidoLayout(FloatLayout):
    comprador_nombre = ObjectProperty(None)
    hora_anuncio = ObjectProperty(None)
    tiendas_grid = ObjectProperty(None)
    button = ObjectProperty(None)
    def set_name_comprador(self,name_comprador):
        self.comprador_nombre.text = "[b]Comprador: [/b]" +name_comprador
    def set_time(self,hora,minutos):
        if len(str(minutos)) >1:
            self.hora_anuncio.text = "[b]Hora anuncio: [/b]" + str(hora)+":"+str(minutos)
        else:
            self.hora_anuncio.text = "[b]Hora anuncio: [/b]" + str(hora) + ":0" + str(minutos)
    def set_tienda(self,tiendalabel):
        self.tiendas_grid.add_widget(tiendalabel)
    def set_info(self,anuncio):
        self.button.set_info_anuncio(anuncio)

class ProductoLayout(FloatLayout):
    button= ObjectProperty(None)
    img = ObjectProperty(None)
    logo = ObjectProperty(None)
    nombre = ObjectProperty(None)
    detalles = ObjectProperty(None)
    info_producto = []

    def set_info(self,producto):
        self.info_producto = producto
        self.button.set_info_producto(producto)
    def set_img_source(self,source):
        self.img.source = source
    def set_logo_source(self,source):
        self.logo.source = source
    def set_nombre(self,nombre):
        self.nombre.text = str(nombre)
    def set_detalles(self,precio,peso):
        self.detalles.text = "$" + str(precio) + " - " + str(peso) + " kg"
    def add_to_cart(self,cantidad,precio_total):
        # PUEDO ACCEDER A MANAGER A TRAVES DE SM
        sm.encargodata.add_to_carro(self.info_producto,cantidad,precio_total,sm.userdata.get_user_info())
        #ACCESO A CURRENT WINDOW
        sm.current_screen.refresh_cant()
        self.confirm()
        print(sm.encargodata.get_carro())
    def confirm(self):
        self.nombre.color = (0,1,0,1)
    def deconfirm(self):
        self.nombre.color = (1,1,1,1)
    def refresh_color(self):
        carro = sm.encargodata.get_carro()
        for prods in column(carro,0):
            if self.info_producto == prods:
                self.confirm()
                return
        self.deconfirm()

#PARA POPUP DE CARRO
class PedidoInCarroLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    detalles = ObjectProperty(None)
    detalles2 = ObjectProperty(None)
    delete_button = ObjectProperty(None)
    popup = [] #popup del carro
    pedido = [] #info del pedido
    def __init__(self,**kwargs):
        self.pedido = kwargs.get('pedido')
        self.popup = kwargs.get('popup')
        super(PedidoInCarroLayout, self).__init__()
        nombre = "[b]"+str(self.pedido[0][1])+"[/b]"
        cantidad = self.pedido[1]
        precio_total = self.pedido[2]
        precio_unit = int(precio_total/cantidad)
        tienda_nombre= self.pedido[0][7][1]
        self.set_cantidad(cantidad)
        self.set_nombre(nombre)
        detalles = "$"+ str(precio_total)+ "($"+str(precio_unit)+"/un)"
        detalles2 = str(tienda_nombre)
        self.set_detalles(detalles,detalles2)

    def set_cantidad(self,cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self,nombre):
        self.nombre.text = str(nombre)
    def set_detalles(self,detalles,detalles2):
        self.detalles.text = str(detalles)
        self.detalles2.text = str(detalles2)
    def delete_pedido(self):
        #primero eleiminamos refrencia en el state loader, luego en el buscador, finalmente nosotros
        pedido_a_eliminar = self.pedido
        self.popup.delete_pedido(pedido_a_eliminar)
        #nos eliminamos
        #self.parent.remove_widget(self)




#LAYOUT QUE AGRUPA TODOS MIS PEDIDOS HACIA UN COMPRADOR EN MIS_PEDIDOS
class MisPedidosGroupLayout(GridLayout):
    comprador = ObjectProperty(None)
    precio_total = ObjectProperty(None)
    pedido = []

    def set_comprador(self,comprador):
        self.comprador.text = "Comprador(a): [b]" + str(comprador)+"[/b]"
    def set_precio_total(self,precio_total):
        self.precio_total.text = "$" + str(precio_total)

# LAYOUT QUE REPRESENTA UNO DE MIS PEDIDOS
class MisPedidosPedidoLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    detalles = ObjectProperty(None)
    detalles2 = ObjectProperty(None)
    icon = ObjectProperty(None)
    def __init__(self,**kwargs):
        self.pedido = kwargs.get('pedido')
        super(MisPedidosPedidoLayout, self).__init__()

        self.set_icon(self.pedido)

        cantidad = self.pedido[4]
        nombre = self.pedido[10]
        precio_unit  = self.pedido[11]
        precio = int(precio_unit)*int(cantidad)
        tienda = self.pedido[9]
        self.set_nombre(nombre)

        detalles = "$" + str(precio) + " ($" + str(precio_unit) + "/un)"
        #checkeamos si esta completado para agregar precio final y cantidad final
        if self.pedido[1] == "true":
            detalles = detalles + " [b]Final: $[/b]"+str(self.pedido[15])
            cantidad = self.pedido[17]
        self.set_cantidad(cantidad)
        detalles2 = str(tienda)
        self.set_detalles(detalles)
        self.set_detalles2(detalles2)




    def set_cantidad(self,cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self,nombre):
        self.nombre.text = "[b]"+ str(nombre)+ "[/b]"
    def set_detalles(self,detalles):
        self.detalles.text = str(detalles)
    def set_detalles2(self,detalles2):
        self.detalles2.text = str(detalles2)
    def set_icon(self,pedido):
        #determinamos estado pedido
        print(pedido)
        if pedido[1] == 'true':
            #comprado
            self.icon.source = 'icons/checked.png'
        elif pedido[16] == 'true':
            #eliminado
            self.icon.source = 'icons/delete.png'
        elif pedido[2] == 'true':
            #en espera
            self.icon.source = 'icons/hourglass.png'
        else:
            print("NUEVO")
            #nuevo o en lista
            self.icon.source = 'icons/run.png'

class MisPedidosHelpBut(Button):
    pass





#LAYOUT QUE INDICA EL ESTADO DE MIS PEDIDOS (ABAJO DE LA LISTA DE ENCARGOS)
#DEPRECATED NO LO USAMOS
class MisPedidosEstadoLayout(FloatLayout):
    estado = ObjectProperty(None)
    def set_estado(self,estado):
        self.estado.text = "Estado: [b]"+str(estado)+"[/b]"

#LAYOUT QUE AGRUPA TODOS MIS PEDIDOS HACIA UNA TIENDA
class TerminarOfertaGroupLayout(GridLayout):
    tienda = ObjectProperty(None)
    precio_total = ObjectProperty(None)
    pedido = []

    def set_tienda(self, tienda):
        self.tienda.text = "Tienda: [b]" + str(tienda)+"[/b]"

    def set_precio_total(self, precio_total):
        self.precio_total.text = "$[b]" + str(precio_total)+"[/b]"


# LAYOUT QUE DE UN PEDIDO DENTRO DEL MENU DE TERMINAR OFERTA
class TerminarOfertaPedidoLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    precio = ObjectProperty(None)
    pedido = []
    def __init__(self,**kwargs):
        self.pedido = kwargs.get('pedido')
        super(TerminarOfertaPedidoLayout, self).__init__()
        cantidad = self.pedido[4]
        nombre = self.pedido[10]
        precio = self.pedido[11]
        self.set_cantidad(cantidad)
        self.set_nombre(nombre)
        self.set_precio(precio)

    def set_cantidad(self, cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self, nombre):
        self.nombre.text = "[b]"+ str(nombre)+"[/b]"
    def set_precio(self, precio):
        cantidad = int(self.cantidad.text)
        precio_total = int(precio)* cantidad
        self.precio.text = "$" + str(precio_total) + " ($" + str(precio) + "/un)"

# LAYOUT QUE DE UN PEDIDO DENTRO DEL MENU DE TERMINAR OFERTA
class TerminarOfertaPedidoAgroupedLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    precio = ObjectProperty(None)

    def set_cantidad(self, cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self, nombre):
        self.nombre.text = "[b]"+ str(nombre)+"[/b]"
    def set_precio(self, precio):
        cantidad = int(self.cantidad.text)
        precio_total = int(precio)* cantidad
        self.precio.text = "$" + str(precio_total) + " ($" + str(precio) + "/un)"


#LAYOUT QUE AGRUPA TODOS MIS PEDIDOS HACIA UNA TIENDA EN PEDIDOS POR COMPRAR
class PedidosPorComprarGroupLayout(GridLayout):
    tienda = ObjectProperty(None)
    tiendaid = ""
    precio_total = ObjectProperty(None)
    tienda_nombre = ""
    pedidos_layouts = []
    caller = None

    def __init__(self,**kwargs):
        self.caller = kwargs.get('caller')
        super(PedidosPorComprarGroupLayout, self).__init__()

    def set_tienda(self, tienda):
        self.tienda.text = "Tienda: [b]" + str(tienda)+"[/b]"
        self.tienda_nombre = str(tienda)
    def set_tienda_id(self, tiendaid):
        self.tiendaid = tiendaid

    def set_precio_total(self, precio_total):
        self.precio_total.text = "$[b]" + str(precio_total)+"[/b]"
    def add_pedido(self,playout):
        print("pedido agregado a grupo")
        self.pedidos_layouts.append(playout)
    def clear_pedidos(self):
        self.pedidos_layouts = []

#checkeamos que pedidos fueron checkeados y los que no (entrega dos listas de ids)
    def check_boxes(self):
        ids_checkeadas = []
        ids_no_checkeadas = []

        for plout in self.pedidos_layouts:

            checkbox= plout.get_checkbox()
            if checkbox.active:
                print("hay uno checkeado")
                ids_checkeadas.append(checkbox.get_id())
            else:
                print("hay uno no checkeado")
                ids_no_checkeadas.append(checkbox.get_id())
        return (ids_checkeadas,ids_no_checkeadas)
    def go_to_terminar_compras(self):

        (ids_checkeadas, ids_no_checkeadas) = self.check_boxes()
        self.caller.terminar_compras(self.tiendaid)

# LAYOUT QUE DE UN PEDIDO DENTRO DEL MENU DE TERMINAR OFERTA
class PedidosPorComprarPedidoLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    precio = ObjectProperty(None)
    solicitante = ObjectProperty(None)
    check = ObjectProperty(None)
    pedido = []
    def __init__(self,**kwargs):
        self.pedido = kwargs.get('pedido')
        super(PedidosPorComprarPedidoLayout, self).__init__()
        cantidad = self.pedido[4]
        nombre = self.pedido[10]
        precio = self.pedido[11]
        solicitante = self.pedido[8]
        self.set_cantidad(cantidad)
        self.set_nombre(nombre)
        self.set_precio(precio)
        self.set_solicitante(solicitante)
        self.set_check_info(str(self.pedido[0]))

    def set_cantidad(self, cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self, nombre):
        self.nombre.text = "[b]"+str(nombre)+"[/b]"
    def set_precio(self, precio):
        cantidad = int(self.cantidad.text)
        precio_total = int(precio)* cantidad
        self.precio.text = "$" + str(precio_total) + " ($" + str(precio) + "/un)"
    def set_solicitante(self,solicitante):
        self.solicitante.text = "Solicita: "+ str(solicitante)
    def set_check_info(self,id_pedido):
        self.check.set_name(str(id_pedido))
        print("seteamos info pedido")
        print(id_pedido)
    def get_checkbox(self):
        return self.check

class PedidosPorComprarTerminarTiendaLayout(FloatLayout):

    def set_button_info(self,grouplayout):
        button = TerminarComprasEnTiendaButton()
        button.set_layout(grouplayout)
        self.add_widget(button)

#LAYOUT QUE AGRUPA TODOS LOS COBROS HACIA UN SOLICITANTE
class CobrosGroupLayout(GridLayout):
    solicitante = ObjectProperty(None)
    precio_total = ObjectProperty(None)
    solicitante_nombre = ""
    pedidos_layouts = []
    cobros_ids = []
    caller = None

    def __init__(self,**kwargs):
        self.caller = kwargs.get('caller')
        super(CobrosGroupLayout, self).__init__()


    def set_solicitante(self, solicitante):
        self.solicitante.text = str(solicitante)
        self.solicitante_nombre = str(solicitante)

    def set_precio_total(self, precio_total):
        self.precio_total.text = "$" + str(precio_total)
    def add_pedido(self,playout,pid):
        print("pedido agregado a grupo")
        self.pedidos_layouts.append(playout)
        self.cobros_ids.append(pid)
    def clear_pedidos(self):
        self.pedidos_layouts = []
        self.cobros_ids = []

    def end_cobros(self):
        self.caller.end_cobros(self.cobros_ids)

# LAYOUT QUE DE UN COBRO DENTRO DEL MENU DE COBROS
class CobrosPedidoLayout(FloatLayout):
    cantidad = ObjectProperty(None)
    nombre = ObjectProperty(None)
    precio = ObjectProperty(None)
    tienda = ObjectProperty(None)
    pedido = []
    def __init__(self,**kwargs):
        self.pedido = kwargs.get('pedido')
        super(CobrosPedidoLayout, self).__init__()
        cantidad = self.pedido[16]
        nombre = self.pedido[10]
        precio = self.pedido[14]
        tienda = self.pedido[9]
        self.set_cantidad(cantidad)
        self.set_nombre(nombre)
        self.set_precio(precio)
        self.set_tienda(tienda)

    def set_cantidad(self, cantidad):
        self.cantidad.text = str(cantidad)
    def set_nombre(self, nombre):
        self.nombre.text = "[b]"+str(nombre)+"[/b]"
    def set_precio(self, precio):
        self.precio.text = "$" + str(precio)
    def set_tienda(self,tienda):
        self.tienda.text = str(tienda)

class CobrosTerminarSolicitanteLayout(FloatLayout):
    def set_button_info(self,grouplayout):
        button = TerminarCobrosSolicitanteButton()
        button.set_layout(grouplayout)
        self.add_widget(button)

#LAYOUT QUE CONTIENE a los agrouped pedidos en pedidos por comprar por tienda
class PedidosPorComprarAgroupedPedidosLayout(GridLayout):
    pedidos = []
    pedidos_new_precio_widgets = []
    pedidos_new_cantidad_widgets = []
    checks = []
    tiendaid = ""
    def __init__(self, **kwargs):
        self.pedidos = kwargs.get('pedidos')
        self.pedidos_new_precio_widgets = []
        self.pedidos_new_cantidad_widgets = []
        self.checks = []
        super(PedidosPorComprarAgroupedPedidosLayout, self).__init__()
        self.set_pedidos()
    def set_pedidos(self):
        self.pedidos_new_cantidad_widgets = []
        #en vez de recibir pedidos, recibimos una nueva estrcutura de pseudopedidos
        #id(del producto),nombre,cantidad,p_unit
        for p in self.pedidos:
            #usamos el id del primer pedido con este producto
            id = p[0]
            name = p[1]
            cantidad = p[2]
            precio_unit = int(p[3])
            precio = int(p[2]) * precio_unit
            namel = PedidosPorComprarLabelA()
            namel.set_text(str(name))
            self.add_widget(namel)
            precio_input = PedidosPorComprarTextInputPrecioLayout()
            precio_input.set_text(str(precio_unit))
            self.add_widget(precio_input)
            self.pedidos_new_precio_widgets.append(precio_input)
            cantidad_input = PedidosPorComprarTextInputCantidadLayout()
            cantidad_input.set_text(str(cantidad))
            self.add_widget(cantidad_input)
            self.pedidos_new_cantidad_widgets.append(cantidad_input)
            check = PedidosPorComprarCheck()
            check.set_id(id)
            self.add_widget(check)
            self.checks.append(check)
    def get_pedidos(self):
        return self.pedidos
    def get_pedidos_precio_widgets(self):
        return self.pedidos_new_precio_widgets
    def get_pedidos_cantidad_widgets(self):
        return self.pedidos_new_cantidad_widgets
    def get_checks(self):
        return self.checks
    def get_tienda_id(self):
        return self.tiendaid
    def set_tienda_id(self,id):
        self.tiendaid = id


#LAYOUT QUE CONTIENE info de los pedidos seleccionados
class PedidosSeleccionadosTerminarComprasLayout(GridLayout):
    pedidos = []
    pedidos_new_precio_widgets = []
    def __init__(self, **kwargs):
        self.pedidos = kwargs.get('pedidos')
        self.pedidos_new_precio_widgets = []
        super(PedidosSeleccionadosTerminarComprasLayout, self).__init__()
        self.set_pedidos()
    def set_pedidos(self):
        for p in self.pedidos:
            id = p[0]
            name = p[10]
            cantidad = p[4]
            precio_unit = int(p[11])
            precio = int(p[4]) * precio_unit
            namel = TerminarComprasLabelA()
            namel.set_text(str(cantidad) + "x "+ str(name))
            self.add_widget(namel)
            preciol = TerminarComprasLabelB()
            preciol.set_text(str(precio))
            self.add_widget(preciol)
            new_precio_l = TerminarComprasTextInput()
            new_precio_l.set_text(str(precio))
            new_precio_l.set_id(id)

            self.pedidos_new_precio_widgets.append(new_precio_l)
            self.add_widget(new_precio_l)
    def get_pedidos(self):
        return self.pedidos
    def get_pedidos_widgets(self):
        return self.pedidos_new_precio_widgets



#LAYOUT QUE CONTIENE info de los pedidos no seleccionados
class PedidosNoSeleccionadosTerminarComprasLayout(GridLayout):
    pedidos = []
    def __init__(self, **kwargs):
        self.pedidos = kwargs.get('pedidos')
        super(PedidosNoSeleccionadosTerminarComprasLayout, self).__init__()
        self.set_pedidos()



    def set_pedidos(self):
        for p in self.pedidos:
            name = p[10]
            cantidad = p[4]
            precio_unit = int(p[11])
            precio = int(p[4]) * precio_unit
            namel = TerminarComprasLabelC()
            namel.set_text(str(cantidad) + "x " + str(name))
            self.add_widget(namel)
            preciol = TerminarComprasLabelD()
            preciol.set_text(str(precio))
            self.add_widget(preciol)

#LAYOUT PARA CONTENER GRUPOS DE TIENDA POR CATEGORIA EN EL MENU DE CREACION DE OFERTA
class TiendaGrupoLayout(GridLayout):
    pass


#layout para contener a una tienda y su checkbox en el menu de tiendas
class TiendaLayout(GridLayout):
    tienda = []
    check = ObjectProperty(None)
    name = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.tienda = kwargs.get('tienda')
        super(TiendaLayout, self).__init__()
        self.check.text = str(self.tienda[0])
        self.name.text = str(self.tienda[1])
    def check_box(self):
        if self.check.active:
            return self.check.text
        else:
            return False


class PedidosPorComprarTextInputPrecioLayout(AnchorLayout):
    def set_text(self,text):
        self.children[0].text = str(text)
    def get_text(self):
        return self.children[0].text
    def set_id(self,id):
        self.children[0].id = id
    def get_id(self):
        return self.children[0].id
class PedidosPorComprarTextInputCantidadLayout(AnchorLayout):
    def set_text(self,text):
        self.children[0].text = str(text)
    def get_text(self):
        return self.children[0].text
    def set_id(self,id):
        self.children[0].id = id
    def get_id(self):
        return self.children[0].id







#-------------------------------------POPUPS----------------------------------------------



class LoadingGifPopup(Popup):
    pass

class ProductoPopup(Popup):
    cantidad = ObjectProperty(None)
    precio= ObjectProperty(None)
    info_producto = []
    caller= None
    def __init__(self,**kwargs):
        self.caller = kwargs.get('caller')
        print(self.caller)
        super(ProductoPopup, self).__init__()

    def set_info(self,producto):
        self.info_producto = producto
    def set_title(self,title):
        self.title = title
    def set_cantidad(self,cantidad):
        self.cantidad.text = str(cantidad)
    def set_precio(self,precio):
        self.precio.text = "$" + str(precio)

    def add(self):
        precio = self.precio.text[1:]
        precio_unit = int(precio)/int(self.cantidad.text)
        self.cantidad.text = str(int(self.cantidad.text) + 1)
        self.precio.text = "$" +str(int(int(precio) + precio_unit))


    def minus(self):
        precio = self.precio.text[1:]
        precio_unit = int(precio) / int(self.cantidad.text)
        if int(self.cantidad.text ) > 1:
            self.cantidad.text = str(int(self.cantidad.text) - 1)
            self.precio.text = "$" + str(int(int(precio) - precio_unit))

    def add_to_cart(self):
        print(self.parent)
        self.caller.add_to_cart(int(self.cantidad.text), int(self.precio.text[1:]))
        self.dismiss()

class CarroPopup(Popup):
    carro = []
    caller= None
    total = ObjectProperty(None)
    pedidos_grid = ObjectProperty(None)
    def __init__(self,**kwargs):
        self.caller = kwargs.get('caller')
        print(self.caller)
        super(CarroPopup, self).__init__()
        self.set_carro(sm.encargodata.get_carro())
        self.load_pedidos()


    def set_carro(self,carro):
        self.carro = carro
    def set_total(self,total):
        self.total.text = "Total: $"+str(total)
    def load_pedidos(self):
        self.pedidos_grid.clear_widgets()
        precios = []
        for p in self.carro:
            layout= PedidoInCarroLayout(pedido=p,popup = self)
            self.pedidos_grid.add_widget(layout)
            print(p)
            precio_pedido = int(p[2])
            precios.append(precio_pedido)
        if len(precios) > 0:
            self.set_total(str(sum(precios)))
        else:
            self.set_total(str(0))
    def delete_pedido(self,pedido):
        #eliminamos del state loader
        sm.encargodata.delete_pedido_from_carro(pedido)
        #cargamos monto total de nuevo
        self.set_carro(sm.encargodata.get_carro())
        self.load_pedidos()
        self.caller.unselect_producto(pedido[0])


class TerminarOfertaWarningPopup(Popup):
    lista = ObjectProperty(None)
    caller = None

    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(TerminarOfertaWarningPopup, self).__init__()
    def set_limits(self,limitlist):
        limits = ""
        if "monto" in limitlist:
            limits = limits+ "->Monto max\n"
        if "cantidad" in limitlist:
            limits = limits+ "->Cant max\n"
        if "peso" in limitlist:
            limits = limits+ "->Peso max\n"
        self.lista.text = limits
    def end_oferta(self):
        self.caller.end_oferta()
        self.dismiss()

class TerminarCobroWarningPopup(Popup):
    caller = None
    cobros_ids = []

    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        self.cobros_ids = kwargs.get('cobros_ids')
        super(TerminarCobroWarningPopup, self).__init__()

    def end_cobros_confirmed(self):
        self.caller.end_cobros_confirmed(self.cobros_ids)
        self.dismiss()

class TerminarCompraPedidoFallidoPopup(Popup):
    pedido = []
    caller = None
    pedido_grid = ObjectProperty(None)
    solicitante = ObjectProperty(None)
    nombre = ObjectProperty(None)
    peso = ObjectProperty(None)
    precio = ObjectProperty(None)

    def __init__(self,**kwargs):
        self.caller = kwargs.get('caller')
        self.pedido = kwargs.get('pedido')
        super(TerminarCompraPedidoFallidoPopup, self).__init__()
        self.load_pedido()

    def load_pedido(self):
        pedido = self.pedido
        solicitante = pedido[8]
        nombre = pedido[10]
        peso = pedido[12]
        precio = pedido[11]
        self.nombre.text = str(nombre)
        self.solicitante.text = str(solicitante)
        self.peso.text = str(peso)
        self.precio.text = str(precio)

    def next(self):
        self.caller.sacamos_popup()
        self.caller.continuar_con_no_seleccionados()
        self.dismiss()

class TerminarCompraPedidoFallidoGeneralPopup(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(TerminarCompraPedidoFallidoGeneralPopup, self).__init__()
    def check_waiting(self):
        self.caller.check_waiting()
        self.dismiss()

class TerminarCompraSucessPopup(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(TerminarCompraSucessPopup, self).__init__()
    def go_to_cobros(self):
        self.caller.go_to_cobros("test")

class TerminarCobroSucessPopup(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(TerminarCobroSucessPopup, self).__init__()
    def go_to_productos(self):
        self.caller.go_to_productos("test")

class NewAnuncioSucessPopup(Popup):
    caller = None
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(NewAnuncioSucessPopup, self).__init__()
    def back_to_menu(self):
        self.caller.back_to_menu("test")

class AddWaitingPopup(Popup):
    caller = None

    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(AddWaitingPopup, self).__init__()

    def calcular_pedidos_espera(self):
        self.caller.calcular_pedidos_espera()
        self.dismiss()
    def skip_espera(self):
        self.caller.agregamos_cobros()
        self.dismiss()

class AddWaitingListFailedPopup(Popup):
    caller = None
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(AddWaitingListFailedPopup, self).__init__()


class LoginFailedPopup(Popup):
    pass
class GroupNotFoundPopup(Popup):
    pass

class GroupNameFailedPopup(Popup):
    pass
class MisPedidosHelpPopup(Popup):
    pass

class NewUserIncorrectDateOrName(Popup):
    pass
class NewUserIncorrectPassword(Popup):
    pass

class NewAnuncioNoTiendasPopup(Popup):
    pass
class NewAnuncioInvalidResPopup(Popup):
    pass



class NewEncargoNoTiendasPopup(Popup):
    pass
class NewEncargoNoProductosPopup(Popup):
    pass

class NewEncargoSucessPopup(Popup):
    caller = None
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(NewEncargoSucessPopup, self).__init__()
    def back_to_menu(self):
        self.caller.back_to_menu("test")

class EndOfertaSucessPopup(Popup):
    caller = None
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(EndOfertaSucessPopup, self).__init__()
    def back_to_menu(self):
        self.caller.back_to_menu("test")

class EndOfertaSucessNoPedidosPopup(Popup):
    caller = None
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(EndOfertaSucessNoPedidosPopup, self).__init__()
    def back_to_menu(self):
        self.caller.back_to_menu("test")

class CerrarSesionWarningPopup(Popup):
    caller = None

    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(CerrarSesionWarningPopup, self).__init__()
    def cerrar_sesion(self):
        self.caller.cerrar_sesion_true()
        self.dismiss()






#-------------------------------------LABELS----------------------------------------------
class NoAnuncios(Label):
    pass

class NoMisPedidos(Label):
    pass
class NoPedidosPorComprar(Label):
    pass

class NoPedidosRecibidos(Label):
    pass
class NoCobros(Label):
    pass
class TiendaLabel(Label):
    def set_name(self,name):
        self.text = name

class TiendaForEncargoLabel(Label):
    def set_name(self,name):
        self.text = name
class TiendaForEncargoLabel1(TiendaForEncargoLabel):
    pass
class TiendaForEncargoLabel2(TiendaForEncargoLabel):
    pass

class TerminarComprasInitialLabel(Label):
    pass

class TerminarComprasWarningLabel(Label):
    pass

class TerminarComprasLabel(Label):
    def set_text(self,text):
        self.text = str(text)

class TerminarComprasLabelA(TerminarComprasLabel):
    pass
class TerminarComprasLabelB(TerminarComprasLabel):
    pass
class TerminarComprasLabelC(TerminarComprasLabel):
    pass
class TerminarComprasLabelD(TerminarComprasLabel):
    pass

class PedidosPorComprarLabelA(Label):
    def set_text(self,text):
        self.text = str(text)


class TiendaGrupoLabel(Label):
    def set_text(self,text):
        self.text = str(text)

#label para enfermedades/factores de rieswgo cuando se crea/edita usuario
class TableLabel(Label):
    def set_text(self,text):
        self.text = str(text)


class TableLabelTituloA(Label):
    def set_text(self,text):
        self.text = str(text)

class TableLabelTituloB(Label):
    def set_text(self,text):
        self.text = str(text)
class TableLabelTituloUsuario(Label):
    def set_text(self,text):
        self.text = str(text)
class TableLabelUsuario(Label):
    def set_text(self,text):
        self.text = str(text)


#-------------------------------------TEXTINPUTS----------------------------------------------

class TerminarComprasTextInput(TextInput):
    def set_text(self,text):
        self.text = str(text)
    def get_text(self):
        return self.text
    def set_id(self,id):
        self.id = id
    def get_id(self):
        return self.id




#-------------------------------------CHECKBOX----------------------------------------------
class TiendaForEncargoCheckBox(CheckBox):
    def set_name(self,name):
        self.text = name
    def set_id(self,id):
        self.id = id
#Check correspondientes a la seccion pedidos por comprar
class PedidosPorComprarCheck(CheckBox):
    def set_name(self,name):
        self.text = name
    def get_id(self):
        return self.id
    def set_id(self,id):
        self.id = id

#check para enfermedades y factores de riesgo cuando se crea/edita el ussuario
class TableCheck(CheckBox):

    def set_name(self,name):
        self.text = name
    def set_id(self,id):
        self.id = id



class TiendaForEncargoCheckBox1(TiendaForEncargoCheckBox):
    pass
class TiendaForEncargoCheckBox2(TiendaForEncargoCheckBox):
    pass


#------------------------------------NOTIFICATIONS----------------------------------------------

#def show_notification(self):
#    plyer.notification.notify(title='Oferta Nueva', message="Juanito ha abierto una oferta")


#-------------------------------------IMAGES----------------------------------------------
class EstadoPedidoAComprarImg(AsyncImage):
    pass
class EstadoPedidoEnEsperaImg(AsyncImage):
    pass
class EstadoPedidoCompradoImg(AsyncImage):
    pass
class EstadoPedidoEliminadoImg(AsyncImage):
    pass

#------------------------------FUNCIONES AUXILIARES-----------------------------------------
#para sacar un arreglo con la fecha actual
def current_date():
    now = datetime.datetime.now()
    return [str(now.day),str(now.month),str(now.year)]

#para checkear si numero es float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#para checkear si numero es int
def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False
#para seleccionar columans en arrays multidimensionales
def column(matrix, i):
    return [row[i] for row in matrix]

#para calcula vulberabilidad a partir de fechanacimiento, condiciones y factores
def calcular_vulnerabilidad(fechnacimiento,condiciones,factores):
    vulnerabilidad = 0.0

    edad = get_edad(fechnacimiento)
    #aumentamos por edad
    if edad >= 70:
        vulnerabilidad = vulnerabilidad + 0.5
    elif edad >= 50 and edad <= 69:
        vulnerabilidad = vulnerabilidad + 0.25
    f_bajos = 0
    f_altos = 0
    c_bajos = 0
    c_altas = 0
    for c in condiciones:
        if c[2] > 1.0:
            c_altas = c_altas +1
        elif c[2] > 0.0:
            c_bajos = c_bajos +1
    for f in factores:
        if f[2] > 1.0:
            f_altos = f_altos +1
        elif f[2] > 0.0:
            f_bajos = f_bajos +1
    #analizamos cuentas
    if (f_altos > 0) or (f_bajos > 1) or (c_altas > 0):
        vulnerabilidad = vulnerabilidad + 0.5
    elif (f_bajos > 0) or (c_bajos > 0):
        vulnerabilidad = vulnerabilidad + 0.25
    return vulnerabilidad
#pasamos los valores de starving por una cola para luego editar la lista completa de valores

def edit_starvings_by_queue(starvings):
    largo = len(starvings)
    if largo == 1:
        return starvings
    level_magnitude = float(1/(largo-1))
    ordered_starvings = sorted(starvings)
    new_starvings = [None]*largo
    level = 0
    last_starving_viewed = None
    last_starving_set = None
    for ordstarv in ordered_starvings:
        index= starvings.index(ordstarv)
        #para asegurar que no hemos repetido el starving
        while new_starvings[index] != None:
            index = starvings.index(ordstarv,index+1)
        if ordstarv == 0:
            new_starvings[index] = 0
        else:
            if ordstarv == last_starving_viewed:
                new_starvings[index] = last_starving_set
            else:
                new_starvings[index] = level
                last_starving_set = level
        level = level + level_magnitude
        last_starving_viewed = ordstarv
    return new_starvings



#para calcular la edad de una persona a partir de su fecha de nacimiento
def get_edad(fecha):
    hoy = date.today()
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    edad = int(hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day)))
    return edad


#funcion que recibe una funcion y la ejecuta durante una pantalla de carga
def loading_function(fun):
    pop = LoadingGifPopup()
    pop.open()
    threading.Thread(target=fun, args=[pop], daemon=True).start()



confkv = Builder.load_file("kvs/config.kv")
kv1 = Builder.load_file("kvs/login.kv")
kv2 = Builder.load_file("kvs/newuser1.kv")
kv3 = Builder.load_file("kvs/newuser2.kv")
kv4 = Builder.load_file("kvs/newuser3.kv")
kv4_5 = Builder.load_file("kvs/newuser3_5.kv")
kv5 = Builder.load_file("kvs/newuser4.kv")
kv6 = Builder.load_file("kvs/newuser5.kv")
kv7 = Builder.load_file("kvs/newuser6.kv")
kv8 = Builder.load_file("kvs/newuser7.kv")
kv9 = Builder.load_file("kvs/newuser8.kv")
kv10 = Builder.load_file("kvs/newuserjoin1.kv")
kv10_5 = Builder.load_file("kvs/newuserjoin2.kv")
kv11 = Builder.load_file("kvs/newusercreate1.kv")
kv12 = Builder.load_file("kvs/newusercreate2.kv")
kvtest = Builder.load_file("kvs/testsuccess.kv")
kvmenu1 = Builder.load_file("kvs/menucompras.kv")
kvmenu2_1 = Builder.load_file("kvs/menupedidos_mispedidos.kv")
kvmenu2_2 = Builder.load_file("kvs/menupedidos_porcomprar.kv")
kvmenu2_3 = Builder.load_file("kvs/menupedidos_cobros.kv")
kvmenu3 = Builder.load_file("kvs/menugrupo.kv")
kvmenu4 = Builder.load_file("kvs/menuopciones.kv")
kvanuncio1 = Builder.load_file("kvs/anuncio1.kv")
kvanuncio2 = Builder.load_file("kvs/anuncio2.kv")
kvencargo1= Builder.load_file("kvs/encargo1.kv")
kvencargo2= Builder.load_file("kvs/encargo2.kv")
kvterminaroferta1= Builder.load_file("kvs/terminaroferta1.kv")
kvterminarcompras1 = Builder.load_file("kvs/terminarcompras1.kv")
kvopcionescondiciones = Builder.load_file("kvs/opcionescondiciones.kv")
kvopcionesfactores = Builder.load_file("kvs/opcionesfactores.kv")
sm = WindowManager()


screens = [LoginWindow(name="login"),NewUser1Window(name="newuser1"),NewUser2Window(name="newuser2"),
           NewUser3Window(name="newuser3"),NewUser3_5Window(name="newuser3_5"),NewUser4Window(name="newuser4"),NewUser5Window(name="newuser5"),
           NewUser6Window(name="newuser6"), NewUser7Window(name="newuser7"), NewUser8Window(name="newuser8"),
           NewUserJoin1Window(name="newuserjoin1"), NewUserJoin2Window(name="newuserjoin2"),
           NewUserCreate1Window(name="newusercreate1"),
           NewUserCreate2Window(name="newusercreate2"),
           TestSuccess(name="testsuccess"),
           MenuComprasWindow(name= "menucompras"), MenuPedidosAWindow(name="menupedidos_a"),
           MenuPedidosBWindow(name="menupedidos_b"), MenuPedidosCWindow(name="menupedidos_c"),
           MenuGrupoWindow(name="menugrupo"), MenuOpcionesWindow(name="menuopciones"),
           Anuncio1Window(name="anuncio1"),Anuncio2Window(name="anuncio2"), Encargo1Window(name="encargo1"),
           Encargo2Window(name="encargo2"), TerminarOferta1Window(name="terminaroferta1"),
           TerminarCompras1Window(name = "terminarcompras1"), OpcionesCondicionesWindow(name = "opcionescondiciones"),OpcionesFactoresWindow(name="opcionesfactores")
           ]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login" \



class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()