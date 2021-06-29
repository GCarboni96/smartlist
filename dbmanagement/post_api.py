import requests
import random
import string
import pandas
from pypika import Table, MySQLQuery, MSSQLQuery, PostgreSQLQuery, OracleQuery, VerticaQuery, Query, Order

from credentials import get_credentials


def get(query):
    host, auth_header = get_credentials()
    sql_command = {
        "commands": query,
        "limit": 1000,
        "separator": ";",
        "stop_on_error": "yes"
    }
    service = "/sql_jobs"
    r = requests.post(host + service, headers=auth_header, json=sql_command)
    # DEBERIA RETORNAR EL NUEVO DATO AGREGADO
    jobid = ""
    if r.status_code == 201:
        jobid = r.json()['id']
    else:
        print("ERROR")
        print()
    r2 = requests.get(host + service + "/" + jobid, headers=auth_header)
    if r2.status_code != 200:
        print("ERROR DE NUEVO")
        print(r2)
    results = r2.json()['results']
    columns = results[0]['columns']
    rows = results[0]['rows']
    df = pandas.DataFrame(data=rows, columns=columns)
    cols = df.columns
    df[cols] = df[cols].apply(pandas.to_numeric, errors="ignore")
    print(df[cols])
    return df[cols]


def post(query):
    host, auth_header = get_credentials()
    sql_command = {
        "commands": query,
        "limit": 1000,
        "separator": ";",
        "stop_on_error": "yes"
    }
    service = "/sql_jobs"
    r = requests.post(host + service, headers=auth_header, json=sql_command)
    return r.json()

def group_code_generator():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


class PostAPI():
    credentials = get_credentials()
    #METODO LOGIN DONDE OBTENGO TAMBIEN MIS DATOS DE USUARIO A PARTIR DE NOMBRE Y CLAVE
    @classmethod
    def login(self, name,password):
        users = Table('USUARIOS')
        q = Query.from_(users).select('ID', 'NOMBRE', 'CLAVE', 'FECHANACIMIENTO', 'GRUPOID', 'ADMIN', 'PARTICIPACION','VULNERABILIDAD','STARVING','MOROSIDAD').where(users.NOMBRE == name).where(users.CLAVE == password)
        answer = get(q.get_sql())
        print("answer")
        print(answer)
        if answer.empty:
            return "ERROR: USUARIO NO EXISTE"
        else:
            return answer.values.tolist()[0]

    # NUEVO GRUPO
    @classmethod
    def add_group_query(self,name):
        group_name = name
        group_code = group_code_generator()
        groups = Table('GRUPOS')
        q = Query.into(groups).columns('NOMBRE', 'CLAVE', 'OWNERID').insert(group_name, group_code, 1)
        answer = post(q.get_sql())
        return answer

    # OBTENGO ULTIMO GRUPO AÑADIDO
    @classmethod
    def get_last_group_query(self, element):
        groups = Table('GRUPOS')
        q = Query.from_(groups).select('ID', 'NOMBRE', 'CLAVE', 'OWNERID').orderby('ID', order=Order.desc).limit(1)
        answer = get(q.get_sql())
        if element == "ID":
            return answer.iat[0,0]

    # OBTENGO ULTIMO USUARIO AÑADIDO
    @classmethod
    def get_last_user_query(self, element):
        users = Table('USUARIOS')
        q = Query.from_(users).select('ID', 'NOMBRE','CLAVE', 'FECHANACIMIENTO','GRUPOID','ADMIN','PARTICIPACION','VULNERABILIDAD','STARVING','MOROSIDAD').orderby('ID', order=Order.desc).limit(1)
        answer = get(q.get_sql())
        if element == "ID":
            return answer.iat[0, 0]

    # AGREGO UN NUEVO USUARIO JUMTO A SUS RESPECTIVOS FACTORES Y CONDICIONES
    # FALTA CALCULAR STARVING Y VULNERABILIDAD
    @classmethod
    def add_user_query(self, user_name,password,birthday,diseases,conditions,groupid,admin,vulnerabilidad):
        users = Table('USUARIOS')
        q = Query.into(users).columns('NOMBRE', 'CLAVE', 'FECHANACIMIENTO','GRUPOID','ADMIN','PARTICIPACION','VULNERABILIDAD','STARVING','MOROSIDAD').insert(user_name, password, birthday,groupid,admin,0.5,vulnerabilidad,0,5)
        answer = post(q.get_sql())
        userid = self.get_last_user_query('ID')
        diseases_tab = Table('USUARIOS_X_FACTORES')
        conditions_tab = Table('USUARIOS_X_CONDICIONES')
        for d in diseases:
            q = Query.into(diseases_tab).columns('USUARIOID','FACTORID').insert(userid,d)
            post(q.get_sql())
        for c in conditions:
            q = Query.into(conditions_tab).columns('USUARIOID','CONDICIONID').insert(userid,c)
            post(q.get_sql())
        return userid

    # EDITO EL ID DEL DUEÑO DE UN GRUPO
    @classmethod
    def edit_group_owner(self,id,groupid):
        groups = Table('GRUPOS')
        q = groups.update().set(groups.OWNERID, id).where(groups.ID == groupid)
        post(q.get_sql())

    # OBTENGO CODIGO DE GRUPO A PARTIR DE SU ID
    @classmethod
    def get_group_code(self,groupid):
        groups = Table('GRUPOS')
        q = Query.from_(groups).select('CLAVE').where(groups.ID == groupid)
        answer = get(q.get_sql())
        if answer.empty:
            return "ERROR: NO CODE"
        else:
            return answer.iat[0, 0]


    @classmethod
    #JUNTO METODOS PARA REGISTRAR GRUPO Y USUARIO
    def create_user_and_group(self,user_name,password,birthday,diseases,conditions,group_name,vulnerabilidad):
        self.add_group_query(group_name)
        groupid = self.get_last_group_query("ID")
        #creamos usuario junto a sus relaciones y obtenemos su id
        userid= self.add_user_query(user_name,password,birthday,diseases,conditions,groupid,True,vulnerabilidad)
        self.edit_group_owner(userid,groupid)
        group_code= self.get_group_code(groupid)
        return group_code

    @classmethod
    #OBTENGO ID DE GRUPO USANDO SU CLAVE
    def get_group_via_code(self, group_code):
        groups = Table('GRUPOS')
        q = Query.from_(groups).select('ID','NOMBRE','CLAVE','OWNERID').where(groups.CLAVE == group_code)
        answer = get(q.get_sql())
        print(answer)
        if answer.empty:
            return "ERROR: NO CODE"
        else:
            return answer.iat[0, 0]

    # OBTENGO GRUPO ENTERO USANDO SU ID
    @classmethod
    def get_group_via_id(self, group_id):
        groups = Table('GRUPOS')
        q = Query.from_(groups).select('ID', 'NOMBRE', 'CLAVE', 'OWNERID').where(groups.ID == group_id)
        answer = get(q.get_sql())
        print(answer)
        if answer.empty:
            return "ERROR: NO GROUP"
        else:
            return answer.values.tolist()[0]

    #obtengo elemento de ultimo anuncio
    @classmethod
    def get_last_anuncio_query(self, element):
        anuncios = Table('ANUNCIOS')
        q = Query.from_(anuncios).select('ID', 'GRUPOID','PRESUPUESTO','PESOMAX','CANTMAX','COMPRADORID', 'HORA', 'MINUTOS', 'TERMINADO').orderby('ID', order=Order.desc).limit(1)
        answer = get(q.get_sql())
        if element == "ID":
            return answer.iat[0, 0]

    @classmethod
    def add_anuncio(self, group_id, presupuesto, pesomax, cantmax, comprador_id, hora, minutos, tiendas):
        anuncios = Table('ANUNCIOS')
        q = Query.into(anuncios).columns('GRUPOID', 'PRESUPUESTO', 'PESOMAX', 'CANTMAX', 'COMPRADORID', 'HORA',
                                         'MINUTOS', 'TERMINADO').insert(group_id, presupuesto, pesomax, cantmax, comprador_id,
                                                           hora, minutos, False)
        answer = post(q.get_sql())
        # conseguimos anuncio
        anuncio_id = self.get_last_anuncio_query("ID")
        anunciosxtiendas_tab = Table('ANUNCIOS_X_TIENDAS')
        for t in tiendas:
            q = Query.into(anunciosxtiendas_tab).columns('TIENDAID', 'ANUNCIOID').insert(int(t), anuncio_id)
            print(q)
            post(q.get_sql())
        return answer

    #AGREGO NUEVO PEDIDO JUNTO A SUS RESPECTIVAS RELACIONES
    @classmethod
    def add_pedido(self, productoid, cantidad, tiendaid, compradorid, solicitanteid,anuncioid):
        pedidos = Table('PEDIDOS')
        q = Query.into(pedidos).columns('PRODUCTOID','CANTIDAD','TIENDAID','COMPRADORID','SOLICITANTEID', 'ANUNCIOID','ENLISTA').insert(productoid, cantidad, tiendaid, compradorid, solicitanteid,anuncioid, False)
        answer = post(q.get_sql())


    @classmethod
    # CONSEGUIMOS EL ANUNCIO QUE CREAMOS NOSOTROS COMO COMPRADOR (OJO TIENE QUE SER UNO DE LOS NO TERMINADOS)
    def get_anuncio_by_compradorid(self,id):
        anuncios = Table('ANUNCIOS')
        anuncios_x_tiendas = Table('ANUNCIOS_X_TIENDAS')
        tiendas = Table('TIENDAS')

        q = Query.from_(anuncios).select(anuncios_x_tiendas.ANUNCIOID, anuncios.GRUPOID, anuncios.PRESUPUESTO,
                                         anuncios.PESOMAX, anuncios.CANTMAX, anuncios.COMPRADORID, anuncios.HORA,
                                         anuncios.MINUTOS, anuncios_x_tiendas.TIENDAID, tiendas.NOMBRE, tiendas.TIPO,
                                         tiendas.LOGO).join(anuncios_x_tiendas).on(
            anuncios.ID == anuncios_x_tiendas.ANUNCIOID).join(tiendas).on(
            tiendas.ID == anuncios_x_tiendas.TIENDAID).where(anuncios.COMPRADORID == id).where(anuncios.TERMINADO == "false")
        answer = get(q.get_sql())
        anuncio_info = []
        if answer.empty:
            return "ERROR: NO ANUNCIO"
        else:
            #si hay anuncio, contamos cuantos pedidos hay asociados a el


            anuncio_info= answer


        #OBTENEMOS TIENDAS
        anuncio = anuncio_info.iloc[0, 0:8].values.tolist()
        tiendas_tab = anuncio_info.iloc[:, 8:12].values.tolist()
        tiendas= []
        for t in tiendas_tab:
            tiendas.append(t)

        #RETORNAMOS EN UN PAR EL ANUNCIO Y LAS TIENDAS ASOCIADAS
        return (anuncio,tiendas)

    @classmethod
    # CONSEGUIMOS LOS ANUNCIOS DE NUESTRO GRUPO (EXCEPTO NUESTRO ANUNCIO) (OJO TIENE QUE SER UNO DE LOS NO TERMINADOS)
    def get_anuncios_by_grupoid(self, groupid,userid):
        anuncios = Table('ANUNCIOS')
        usuarios = Table('USUARIOS')
        anuncios_x_tiendas = Table('ANUNCIOS_X_TIENDAS')
        tiendas = Table('TIENDAS')
        q = Query.from_(anuncios).select(anuncios_x_tiendas.ANUNCIOID, anuncios.GRUPOID, anuncios.PRESUPUESTO,
                                         anuncios.PESOMAX, anuncios.CANTMAX, anuncios.COMPRADORID,usuarios.NOMBRE.as_("NOMBRECOMPRADOR"),anuncios.HORA,
                                         anuncios.MINUTOS, anuncios_x_tiendas.TIENDAID, tiendas.NOMBRE, tiendas.TIPO,
                                         tiendas.LOGO).join(anuncios_x_tiendas).on(
            anuncios.ID == anuncios_x_tiendas.ANUNCIOID).join(tiendas).on(
            tiendas.ID == anuncios_x_tiendas.TIENDAID).join(usuarios).on(anuncios.COMPRADORID == usuarios.ID).where(anuncios.GRUPOID == groupid).where(anuncios.COMPRADORID != userid).where(anuncios.TERMINADO == "false")
        print(q)

        answer = get(q.get_sql())
        anuncios = []
        if answer.empty:
            return "ERROR: NO ANUNCIO"
        else:
            anuncios= answer
        # OBTENEMOS IDS DE CADA ANUNCIO
        ids_anuncio = anuncios.iloc[:, 0].values.tolist()
        ids_anuncio = list(dict.fromkeys(ids_anuncio))

        anunciosxtiendas = []

        for i in ids_anuncio:
            a = anuncios.loc[anuncios["ANUNCIOID"] == i]
            # OBTENEMOS TIENDAS
            anuncio = a.iloc[0, 0:9].values.tolist()
            tiendas_tab = a.iloc[:, 9:13].values.tolist()
            tiendas = []
            for t in tiendas_tab:
                tiendas.append(t)
            anunciosxtiendas.append([anuncio, tiendas])
        return anunciosxtiendas

    @classmethod
    # CONSEGUIMOS LOS PRODUCTOS A PARTIR DEL ID DE SU TIENDA
    def get_productos_by_tienda_id(self, tiendaid):
        products = Table('PRODUCTOS')
        q = Query.from_(products).select(products.star).where(products.TIENDAID == tiendaid)
        answer = get(q.get_sql())
        if answer.empty:
            return []
        else:
            print("PRODUCTOS:")
            print(answer.values.tolist())
            return answer.values.tolist()

    @classmethod
    # CONSIGO LOS PEDIDOS QUE SOLICITÉ JUNTO A LOS DATOS DEL PRODUCTO, NOMBRE DE TIENDA, Y NOMBRE DE COMPRADOR
    def get_mis_pedidos_with_comprador(self,solicitanteid):
        pedidos = Table('PEDIDOS')
        usuarios = Table('USUARIOS')
        tiendas = Table('TIENDAS')
        productos = Table('PRODUCTOS')
        q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA, pedidos.PRODUCTOID, pedidos.CANTIDAD, pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID, usuarios.NOMBRE.as_("COMPRADORNOMBRE"), tiendas.NOMBRE.as_("TIENDANOMBRE"), productos.NOMBRE.as_("PRODUCTONOMBRE"), productos.PRECIO.as_("PRODUCTOPRECIO"), productos.PESO.as_("PRODUCTOPESO"),pedidos.ENLISTA,pedidos.ANUNCIOID,pedidos.PRECIOFINAL,pedidos.ELIMINADO,pedidos.CANTIDADFINAL).join(usuarios).on(
            pedidos.COMPRADORID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).join(productos).on(productos.ID == pedidos.PRODUCTOID).where(
            pedidos.SOLICITANTEID == solicitanteid)

        answer = get(q.get_sql())

        if answer.empty:
            return "ERROR: NO PEDIDOS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSIGO LOS PEDIDOS QUE ME SOLIITAN JUNTO A LOS DATOS DEL PRODUCTO, NOMBRE DE TIENDA, Y NOMBRE DE SOLICITANTE PARA CARGARLOS EN LA VENTANA DE TERMINAR OFERTA
    # AGREGAMOS LA CONDICION DE QUE NO ESTAN NI EN ESPERA NI COMPRADO NI EN LISTA
    def get_mis_pedidos_with_solicitante_terminaroferta(self,compradorid):
        pedidos = Table('PEDIDOS')
        usuarios = Table('USUARIOS')
        tiendas = Table('TIENDAS')
        productos = Table('PRODUCTOS')
        q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA, pedidos.PRODUCTOID,
                                        pedidos.CANTIDAD, pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID, usuarios.NOMBRE.as_("SOLICITANTENOMBRE"),
                                        tiendas.NOMBRE.as_("TIENDANOMBRE"), productos.NOMBRE.as_("PRODUCTONOMBRE"), productos.PRECIO.as_("PRODUCTOPRECIO"), productos.PESO.as_("PRODUCTOPESO"),pedidos.ENLISTA, pedidos.ANUNCIOID).join(usuarios).on(
            pedidos.SOLICITANTEID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).join(productos).on(productos.ID == pedidos.PRODUCTOID).where(
            pedidos.COMPRADORID == compradorid).where(pedidos.ESPERA == "false").where(pedidos.ENLISTA== "false").where(pedidos.COMPRADO == "false").where(pedidos.ELIMINADO == "false")

        answer = get(q.get_sql())

        if answer.empty:
            return "ERROR: NO PEDIDOS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSIGO LOS PEDIDOS QUE ME SOLIITAN JUNTO A LOS DATOS DEL PRODUCTO, NOMBRE DE TIENDA, Y NOMBRE DE SOLICITANTE PARA CARGARLOS EN LA VENTANA DE PEDIDOS POR COMPRAR
    # AGREGAMOS LA CONDICION DE QUE NO ESTAN NI EN ESPERA NI COMPRADO Y EN LA LISTA
    def get_mis_pedidos_with_solicitante_porcomprar(self, compradorid):
        pedidos = Table('PEDIDOS')
        usuarios = Table('USUARIOS')
        tiendas = Table('TIENDAS')
        productos = Table('PRODUCTOS')
        q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA, pedidos.PRODUCTOID,
                                        pedidos.CANTIDAD, pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID,
                                        usuarios.NOMBRE.as_("SOLICITANTENOMBRE"),
                                        tiendas.NOMBRE.as_("TIENDANOMBRE"), productos.NOMBRE.as_("PRODUCTONOMBRE"),
                                        productos.PRECIO.as_("PRODUCTOPRECIO"), productos.PESO.as_("PRODUCTOPESO"),
                                        pedidos.ENLISTA,pedidos.ANUNCIOID).join(usuarios).on(
            pedidos.SOLICITANTEID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).join(productos).on(
            productos.ID == pedidos.PRODUCTOID).where(
            pedidos.COMPRADORID == compradorid).where(pedidos.ESPERA == "false").where(
            pedidos.ENLISTA == "true").where(pedidos.COMPRADO == "false").where(pedidos.ELIMINADO == "false")

        answer = get(q.get_sql())

        if answer.empty:
            return "ERROR: NO PEDIDOS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSIGO LOS PEDIDOS COMPRADOS QUE ME SOLICITARON PARA
    # AGREGAMOS LA CONDICION DE QUE NO ESTAN NI EN ESPERA, COMPRADO Y NO EN LA LISTA
    def get_cobros_by_comprador_id(self, compradorid):
        pedidos = Table('PEDIDOS')
        usuarios = Table('USUARIOS')
        tiendas = Table('TIENDAS')
        productos = Table('PRODUCTOS')
        q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA, pedidos.PRODUCTOID,
                                        pedidos.CANTIDAD, pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID,
                                        usuarios.NOMBRE.as_("SOLICITANTENOMBRE"),
                                        tiendas.NOMBRE.as_("TIENDANOMBRE"), productos.NOMBRE.as_("PRODUCTONOMBRE"),
                                        productos.PRECIO.as_("PRODUCTOPRECIO"), productos.PESO.as_("PRODUCTOPESO"),
                                        pedidos.ENLISTA, pedidos.PRECIOFINAL,pedidos.ANUNCIOID,pedidos.CANTIDADFINAL).join(usuarios).on(
            pedidos.SOLICITANTEID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).join(productos).on(
            productos.ID == pedidos.PRODUCTOID).where(
            pedidos.COMPRADORID == compradorid).where(pedidos.ESPERA == "false").where(
            pedidos.ENLISTA == "false").where(pedidos.COMPRADO == "true").where(pedidos.ELIMINADO == "false")

        answer = get(q.get_sql())

        if answer.empty:
            return "ERROR: NO PEDIDOS"
        else:
            return answer.values.tolist()

    @classmethod
    # CAMBIO TODOS LOS PEDIDOS ASOCIADOS A MI ID DE COMPRADOR ID PARA QUE ESTEN EN LA LISTA
    def update_pedidos_enlista_with_compradorid(self, compradorid):
        pedidos = Table('PEDIDOS')
        q = Query.update(pedidos).set(pedidos.ENLISTA,True).set(pedidos.COMPRADO,False).set(pedidos.ESPERA,False).where(pedidos.COMPRADORID == compradorid)
        answer = post(q.get_sql())
        return answer

    @classmethod
    # CAMBIO TODOS LOS PEDIDOS ASOCIADOS A PARTIR DE UNA LISTA PARA QUE ESTEN EN LA LISTA
    def update_pedidos_enlista_with_multiple_ids(self, listid):
        pedidos = Table('PEDIDOS')
        first = True
        q = Query.update(pedidos).set(pedidos.ENLISTA, True).set(pedidos.COMPRADO,False).set(pedidos.ESPERA,False).where(pedidos.ID.isin(listid))

        print(q)
        answer = post(q.get_sql())
    @classmethod
    # CAMBIO LOS PEDIDOS ASOCIADOS A PARTIR DE UNA LISTA JUNTO A UNA NUEVA CANTIDAD
    def update_pedidos_enlista_with_multiple_ids_and_new_cantidad(self, list):
        #OPTIMIZAR
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        for pair in list:
            id = pair[0]
            cant = pair[1]
            # first
            if first:
                first = False
                q = Query.update(pedidos).set(pedidos.ENLISTA, True).set(pedidos.COMPRADO,False).set(pedidos.ESPERA,False).set(pedidos.CANTIDAD, cant).where(pedidos.ID == id)
                post(q.get_sql())
                q_base = q
            else:
                q = Query.update(pedidos).set(pedidos.ENLISTA, True).set(pedidos.COMPRADO,False).set(pedidos.ESPERA,False).set(pedidos.CANTIDAD, cant).where(pedidos.ID == id)
                q_base = q_base * q
                post(q.get_sql())
        print(q_base)
        #answer = post(q_base.get_sql())

    @classmethod
    # agrego pedidos con cantidad de resto a lista de espera
    def add_rejected_cantidad_to_wait_list(self,list):
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        for pair in list:
            id = pair[0]
            cant = pair[1]
            # first
            if first:
                first = False
                q = Query.into(pedidos).columns('COMPRADO','ESPERA','PRODUCTOID','CANTIDAD','TIENDAID','COMPRADORID','SOLICITANTEID','ANUNCIOID','ENLISTA').from_(pedidos).select(pedidos.COMPRADO,True,pedidos.PRODUCTOID, cant,pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID,pedidos.ANUNCIOID,False).where(pedidos.ID == id)
                q_base = q
            else:
                q = Query.into(pedidos).columns('COMPRADO', 'ESPERA', 'PRODUCTOID', 'CANTIDAD', 'TIENDAID',
                                                'COMPRADORID', 'SOLICITANTEID', 'ANUNCIOID', 'ENLISTA').from_(
                    pedidos).select(pedidos.COMPRADO, True, pedidos.PRODUCTOID, cant, pedidos.TIENDAID,
                                    pedidos.COMPRADORID, pedidos.SOLICITANTEID, pedidos.ANUNCIOID, False).where(
                    pedidos.ID == id)
                q_base = q_base * q
        print(q_base)
        answer = post(q_base.get_sql())

    @classmethod
    # edito pedidos para que esten en espera a partir de una lista de ids
    def update_pedidos_rejected(self,listid):

        pedidos = Table('PEDIDOS')
        q = Query.update(pedidos).set(pedidos.ESPERA, True).set(pedidos.COMPRADO, False).set(pedidos.ENLISTA, False).where(pedidos.ID.isin(listid))
        print(q)
        answer = post(q.get_sql())


    @classmethod
    # "ELIMINO" UN ANUNCIO JUNTO A SUS REFERENCIAS A LAS TIENDAS
    def termino_anuncio_by_id(self,anuncioid):
        anuncios = Table('ANUNCIOS')
        q = Query.update(anuncios).set(anuncios.TERMINADO, True).where(anuncios.ID == anuncioid)
        answer = post(q.get_sql())
        return answer
    @classmethod
    # CONSIGO PRODUCTOS CON LISTA DE IDS
    def get_multiple_productos_by_id(self, listid):
        q_base = ""
        first = True
        products = Table("PRODUCTOS")
        for id in listid:
            #first
            if first:
                first = False
                q = Query.from_(products).select(products.star).where(products.ID == id)
                q_base = q
            else:
                q = Query.from_(products).select(products.star).where(products.ID == id)
                q_base = q_base * q

        print(q_base)
        answer = get(q_base.get_sql())
        print(answer)
        return answer.values.tolist()

    @classmethod
    # CONSIGO PRODUCTOS CON LISTA DE IDS
    def get_multiple_usuarios_by_id(self, listid):
        q_base = ""
        usuarios = Table("USUARIOS")
        first = True
        for id in listid:
            # first
            if first:
                first = False
                q = Query.from_(usuarios).select(usuarios.star).where(usuarios.ID == id)
                q_base = q
            else:
                print("yos")
                q = Query.from_(usuarios).select(usuarios.star).where(usuarios.ID == id)
                q_base = q_base * q
        answer = get(q_base.get_sql())
        print(q_base)
        print(answer)
        return answer.values.tolist()

    @classmethod
    #actualizo pedidos con nuevo precio y estado comprado Y APROVECHAMOS DE cambiar precio
    def update_pedidos_comprados_with_id_and_new_price(self,pedidos_selected,newprices):
        # OPTIMIZAR
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        for i in range(len(pedidos_selected)):
            print("ACTUALIZAMOS PEDIDO COMPRADO")
            p = pedidos_selected[i]
            print(p)
            newp = newprices[i]
            id = p[0]
            # first
            if first:
                first = False
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, True).set(pedidos.ESPERA, False).set(pedidos.PRECIOFINAL, int(newp)).where(pedidos.ID == int(id))
                answer = post(q.get_sql())
                q_base = q
            else:
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, True).set(pedidos.ESPERA, False).set(pedidos.PRECIOFINAL, int(newp)).where(pedidos.ID == int(id))
                q_base = q_base * q
                answer= post(q.get_sql())
            return answer

    @classmethod
    # actualizo pedidos con nueva
    def update_pedidos_comprados_with_id(self, pedidos_selected_id, newprices,newcants):
        # OPTIMIZAR
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        print(pedidos_selected_id)
        for i, c in enumerate(pedidos_selected_id):
            print("ACTUALIZAMOS PEDIDO COMPRADO")
            p = pedidos_selected_id[i]
            print(p)
            newpbeta = newprices[i]
            newc = newcants[i]
            newp = int(newpbeta)*int(newc)
            id = p
            # first
            if first:
                first = False
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, True).set(pedidos.ESPERA,False).set(
                    pedidos.PRECIOFINAL, int(newp)).set(
                    pedidos.CANTIDADFINAL, int(newc)).where(pedidos.ID == int(id))
                answer = post(q.get_sql())
                q_base = q
            else:
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, True).set(pedidos.ESPERA,
                                                                                                      False).set(
                    pedidos.PRECIOFINAL, int(newp)).set(
                    pedidos.CANTIDADFINAL, int(newc)).where(pedidos.ID == int(id))
                q_base = q_base * q
                answer = post(q.get_sql())


    @classmethod
    # dejamos pedidos en estado de eliminado
    def eliminar_pedidos_by_list_id(self, listid):
        # OPTIMIZAR
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        for id in listid:
            print("ELIMINO UN PEDIDO")
            # first
            if first:
                first = False
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, False).set(pedidos.ESPERA,False).set(pedidos.ELIMINADO, True).where(pedidos.ID == id)
                post(q.get_sql())
                q_base = q
            else:
                q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, False).set(pedidos.ESPERA,False).set(pedidos.ELIMINADO, True).where(pedidos.ID == id)
                q_base = q_base * q
                post(q.get_sql())



    @classmethod
    #borramos pedidos por listid (DE VERDAD LOS ELIMINAMOS)
    def delete_pedidos_by_list_id(self,listid):
        q_base = ""
        pedidos = Table('PEDIDOS')
        first = True
        for id in listid:
            q = Query.from_(pedidos).delete().where(pedidos.ID == id)
            if first:
                first = False
                q_base = q
            else:
                q_base = q_base * q
            post(q.get_sql())

    @classmethod
    # dejamos pedidos en estado de eliminado de una tienda visitada pertenecientes a un anuncio en particular
    def eliminar_pedidos_en_espera_by_tienda_and_anuncio(self,tiendaid,anuncioid):
        pedidos = Table('PEDIDOS')
        q = Query.update(pedidos).set(pedidos.ENLISTA, False).set(pedidos.COMPRADO, False).set(pedidos.ESPERA,False).set(pedidos.ELIMINADO, True).where(pedidos.TIENDAID == tiendaid).where(pedidos.ANUNCIOID == anuncioid).where(pedidos.ESPERA == "true")
        post(q.get_sql())

    @classmethod
    # OBTENGO PEDIDOS DE UN ANUNCIO QUE SE ENCUENTREN EN LISTA
    def check_pedidos_on_list_by_anuncio_id(self, anuncioid):
        pedidos = Table('PEDIDOS')
        q = Query.from_(pedidos).select(pedidos.star).where(pedidos.ENLISTA == "true").where(pedidos.ANUNCIOID == anuncioid )
        answer = get(q.get_sql())
        print(answer)
        if answer.empty:
            return False
        else:
            return True

    @classmethod
    # borramos anuncio terminado a partir de su id
    def delete_anuncio_by_id(self, anuncioid):
        anuncios = Table('ANUNCIOS')
        q = Query.from_(anuncios).delete().where(anuncios.ID == anuncioid).where(anuncios.TERMINADO == "true")

        print("NUESTRA QUERY DE BORRAR")
        print(q)
        post(q.get_sql())

    @classmethod
    # borramos anuncio terminado a partir de su id
    def delete_anuncio_forced_by_id(self, anuncioid):
        anuncios = Table('ANUNCIOS')
        q = Query.from_(anuncios).delete().where(anuncios.ID == anuncioid)

        print("NUESTRA QUERY DE BORRAR")
        print(q)
        post(q.get_sql())

    @classmethod
    # borramos relaciones anuncioxtiend con id del anuncio
    def delete_anuncio_x_tiendas_by_id(self, anuncioid):
        anuncios_x_tiendas = Table('ANUNCIOS_X_TIENDAS')
        q = Query.from_(anuncios_x_tiendas).delete().where(anuncios_x_tiendas.ANUNCIOID == anuncioid)
        post(q.get_sql())

    @classmethod
    # borramos pedidos que quedaron en espera a partir de un anuncio
    def delete_pedidos_en_espera_by_anuncio_id(self, anuncioid):
        pedidos = Table('PEDIDOS')
        q = Query.from_(pedidos).delete().where(pedidos.ANUNCIOID == anuncioid).where(pedidos.ESPERA == "true").where(pedidos.COMPRADO == "false")

        post(q.get_sql())

    @classmethod
    # borramos pedidos que estaban en estadp "eliminado"
    def delete_pedidos_eliminados_by_anuncio_id(self, anuncioid):
        pedidos = Table('PEDIDOS')
        q = Query.from_(pedidos).delete().where(pedidos.ANUNCIOID == anuncioid).where(pedidos.ELIMINADO == "true").where(pedidos.COMPRADO == "false")

        post(q.get_sql())

    @classmethod
    # conseguimos los pedidos en espera que no esten en la tienda que acabamos de visitar
    def get_pedidos_en_espera_by_anuncioid_not_in_tiendaid(self, anuncioid,tiendaid):
        pedidos = Table('PEDIDOS')
        usuarios = Table('USUARIOS')
        tiendas = Table('TIENDAS')
        productos = Table('PRODUCTOS')
        q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA, pedidos.PRODUCTOID,
                                        pedidos.CANTIDAD, pedidos.TIENDAID, pedidos.COMPRADORID, pedidos.SOLICITANTEID,
                                        usuarios.NOMBRE.as_("SOLICITANTENOMBRE"),
                                        tiendas.NOMBRE.as_("TIENDANOMBRE"), productos.NOMBRE.as_("PRODUCTONOMBRE"),
                                        productos.PRECIO.as_("PRODUCTOPRECIO"), productos.PESO.as_("PRODUCTOPESO"),
                                        pedidos.ENLISTA, pedidos.ANUNCIOID).join(usuarios).on(
            pedidos.SOLICITANTEID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).join(productos).on(
            productos.ID == pedidos.PRODUCTOID).where(
            pedidos.ANUNCIOID == anuncioid).where(pedidos.TIENDAID != tiendaid).where(pedidos.ESPERA == "true").where(
            pedidos.ENLISTA == "false").where(pedidos.COMPRADO == "false").where(pedidos.ELIMINADO == "false")

        answer = get(q.get_sql())

        if answer.empty:
            return "ERROR: NO PEDIDOS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSEGUIMOS UN ANUNCIO POR ID
    def get_anuncio_by_id(self, id):
        anuncios = Table('ANUNCIOS')
        q = Query.from_(anuncios).select(anuncios.star).where(anuncios.ID == id)
        answer = get(q.get_sql())
        anuncio_info = []
        if answer.empty:
            return "ERROR: NO ANUNCIO"
        else:
            return answer.values.tolist()[0]

    @classmethod
    # CONSEGUIMOS TODAS LAS TIENDAS DISPONIBLES Y SUS INFFOS
    def get_all_tiendas(self):
        tiendas = Table('TIENDAS')
        q = Query.from_(tiendas).select(tiendas.star)
        answer = get(q.get_sql())
        if answer.empty:
            return "ERROR: NO TIENDAS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSEGUIMOS TODAS LAS CONDICIONES DE MOVILIDAD POSIBLES
    def get_all_conditions(self):
        conditions = Table('CONDICIONES')
        q = Query.from_(conditions).select(conditions.star)
        answer = get(q.get_sql())
        if answer.empty:
            return "ERROR: NO CONDITIONS"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSEGUIMOS TODAS LOS FACTORES DE RIESGO POSIBLE
    def get_all_factores(self):
        factores = Table('FACTORES')
        q = Query.from_(factores).select(factores.star)
        answer = get(q.get_sql())
        if answer.empty:
            return "ERROR: NO FACTORES"
        else:
            return answer.values.tolist()

    @classmethod
    # CONSEGUIMOS A LOS USUARIOS DE MI GRUPO
    def get_users_in_my_group_by_group_id(self, groupid):
        usuarios = Table("USUARIOS")
        q = Query.from_(usuarios).select(usuarios.star).where(usuarios.GRUPOID == int(groupid))
        answer = get(q.get_sql())
        if answer.empty:
            return []
        else:
            return answer.values.tolist()


    @classmethod
    # CONSEGUIMOS LAS CONDICIONES DE MOVILIDAD DE UN USUARIO EN PARTICULAR
    def get_user_conditions(self,userid):
        usuarios_x_condiciones = Table("USUARIOS_X_CONDICIONES")
        condiciones = Table("CONDICIONES")
        q = Query.from_(condiciones).select(condiciones.ID, condiciones.NOMBRE, condiciones.NIVEL).join(usuarios_x_condiciones).on(
            condiciones.ID == usuarios_x_condiciones.CONDICIONID).where(usuarios_x_condiciones.USUARIOID == int(userid))

        answer = get(q.get_sql())
        if answer.empty:
            return []
        else:
            return answer.values.tolist()

    @classmethod
    # CONSEGUIMOS LOS FACTORES DE RIESGO DE UN USUARIO EN PARTICULAR
    def get_user_diseases(self, userid):
        usuarios_x_factores = Table("USUARIOS_X_FACTORES")
        factores = Table("FACTORES")
        q = Query.from_(factores).select(factores.ID, factores.NOMBRE, factores.NIVEL).join(
            usuarios_x_factores).on(
            factores.ID == usuarios_x_factores.FACTORID).where(usuarios_x_factores.USUARIOID == int(userid))

        answer = get(q.get_sql())
        if answer.empty:
            return []
        else:
            return answer.values.tolist()

    @classmethod
    #editamos condiciones de usuario (borramos actuales y agregamos nuevas)
    def edit_user_conditions(self,userid,newconditions):
        usuarios_x_condiciones = Table("USUARIOS_X_CONDICIONES")
        q = Query.from_(usuarios_x_condiciones).delete().where(usuarios_x_condiciones.USUARIOID == int(userid))
        post(q.get_sql())
        for c in newconditions:
            id = c[0]
            q = Query.into(usuarios_x_condiciones).columns('USUARIOID', 'CONDICIONID').insert(int(userid), id)
            post(q.get_sql())

    @classmethod
    # editamos factores de riesgo (borramos actuales y agregamos nuevas)
    def edit_user_diseases(self, userid, newdiseases):
        usuarios_x_factores = Table("USUARIOS_X_FACTORES")
        q = Query.from_(usuarios_x_factores).delete().where(usuarios_x_factores.USUARIOID == int(userid))
        post(q.get_sql())
        for f in newdiseases:
            id = f[0]
            q = Query.into(usuarios_x_factores).columns('USUARIOID', 'FACTORID').insert(int(userid), id)
            post(q.get_sql())

    @classmethod
    # editamos vulnerabilidad de usuario
    def update_user_vulnerabilidad(self,userid,vulnerabilidad):
        usuarios = Table('USUARIOS')
        q = usuarios.update().set(usuarios.VULNERABILIDAD, float(vulnerabilidad)).where(usuarios.ID == userid)
        post(q.get_sql())

    @classmethod
    #reseteamos morosidad de usuario
    def reset_user_morosidad_and_participacion(self,userid):
        usuarios = Table('USUARIOS')
        q = usuarios.update().set(usuarios.PARTICIPACION, 1.0).set(usuarios.MOROSIDAD, 0).where(usuarios.ID == userid)
        post(q.get_sql())

    @classmethod
    # CONSEGUIMOS UN USUARIO POR ID
    def get_user_by_id(self, id):
        usuarios = Table('USUARIOS')
        q = Query.from_(usuarios).select(usuarios.star).where(usuarios.ID == id)
        answer = get(q.get_sql())
        anuncio_info = []
        if answer.empty:
            return "ERROR: NO USER"
        else:
            return answer.values.tolist()[0]

    @classmethod
    # subimos morosidad y devolvemos usuario completo
    def add_morosidad_to_user(self,userid):
        usuarios = Table('USUARIOS')
        q = usuarios.update().set(usuarios.MOROSIDAD, usuarios.MOROSIDAD+1).where(usuarios.ID == userid)
        post(q.get_sql())
        return self.get_user_by_id(userid)

    @classmethod
    # cambiamos nivel de participacion a estándar (0.5)
    def set_standard_participacion_to_user(self, userid):
        usuarios = Table('USUARIOS')
        q = usuarios.update().set(usuarios.PARTICIPACION, 0.5).where(usuarios.ID == userid)
        post(q.get_sql())

    @classmethod
    # cambiamos nivel de participacion a estándar (0.5)
    def set_low_participacion_to_user(self, userid):
        usuarios = Table('USUARIOS')
        q = usuarios.update().set(usuarios.PARTICIPACION, 0).where(usuarios.ID == userid)
        post(q.get_sql())

    @classmethod
    #conseguimos info de los solicitantes y sus pedidos, y a partir de eso seteamos su nuevo valor de starving
    def refresh_starving_of_solicitantes(self,anuncioid):
        usuarios = Table('USUARIOS')
        pedidos = Table('PEDIDOS')
        q = Query.from_(pedidos).select(pedidos.ID,pedidos.SOLICITANTEID,pedidos.CANTIDADFINAL,pedidos.COMPRADO,pedidos.CANTIDAD).where(pedidos.ANUNCIOID == anuncioid)
        pedidostabla = get(q.get_sql()).values.tolist()
        solicitantesid = []
        for p in pedidostabla:
            if p[1] not in solicitantesid:
                solicitantesid.append(p[1])

        for s in solicitantesid:
            pedidos_success = 0
            pedidos_failed = 0
            for p in pedidostabla:
                #si se trata de un pedido nuestro
                if p[1] == s:
                    if p[3] == "true":
                        print("pedido comprado")
                        pedidos_success = pedidos_success + int(p[2])
                        pedidos_failed = pedidos_failed + int(p[4]) -int(p[2])

                    else:
                        print("pedido F")
                        pedidos_failed = pedidos_failed + int(p[4])
            print("aciertos")
            print(pedidos_success)
            print("fallos")
            print(pedidos_failed)
            newstarving = round(float(pedidos_failed/(pedidos_success+pedidos_failed)),2)
            print("NUEVO STARVING")
            print(newstarving)
            q = usuarios.update().set(usuarios.STARVING, newstarving).where(usuarios.ID == s)
            post(q.get_sql())
















































































