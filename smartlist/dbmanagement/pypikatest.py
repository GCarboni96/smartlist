from pypika import Table, MySQLQuery, MSSQLQuery, PostgreSQLQuery, OracleQuery, VerticaQuery, Query, Order

import datetime

pedidos =  Table('PEDIDOS')
usuarios = Table('USUARIOS')
tiendas= Table('TIENDAS')
productos = Table('PRODUCTOS')
q = Query.from_(pedidos).select(pedidos.ID, pedidos.COMPRADO, pedidos.ESPERA,pedidos.PRODUCTOID,pedidos.CANTIDAD,pedidos.TIENDAID,pedidos.COMPRADORID,pedidos.SOLICITANTEID, usuarios.NOMBRE.as_("COMPRADORNOMBRE"), tiendas.NOMBRE.as_("TIENDANOMBRE")).join(usuarios).on(pedidos.COMPRADORID == usuarios.ID).join(tiendas).on(tiendas.ID == pedidos.TIENDAID).where(pedidos.SOLICITANTEID== 1)
print(q)



products = Table('PRODUCTS')

q = ""
q1 = Query.from_(products).select(products.star).where(products.ID == 1)

q2 = Query.from_(products).select(products.star).where(products.ID == 2)

print(q+q1+q2)

anuncios = Table('ANUNCIOS')

def edit_starvings_by_queue(starvings):
    largo = len(starvings)
    if largo == 1:
        return starvings
    print(largo)
    level_magnitude = float(1/(largo-1))
    print(level_magnitude)
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

print(edit_starvings_by_queue([0.5,0.7,0.0,0.0]))


