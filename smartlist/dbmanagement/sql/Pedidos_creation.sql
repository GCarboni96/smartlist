CREATE TABLE Pedidos(
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    comprado boolean NOT NULL DEFAULT False,
    espera boolean NOT NULL DEFAULT False,
    productoid int,
    cantidad int,
    tiendaid int,
    compradorid int,
    solicitanteid int,
    anuncioid int,
    enlista boolean NOT NULL DEFAULT False,
    preciofinal int DEFAULT 0,
    eliminado boolean NOT NULL DEFAULT False,
    cantidadfinal int DEFAULT 0,
    CONSTRAINT FK_Producto_Pedido FOREIGN KEY (productoid) REFERENCES PRODUCTOS(id),
    CONSTRAINT FK_Tienda_Pedido FOREIGN KEY (tiendaid) REFERENCES TIENDAS(id),
    CONSTRAINT FK_Comprador_Pedido FOREIGN KEY (compradorid) REFERENCES USUARIOS(id),
    CONSTRAINT FK_Solicitante_Pedido FOREIGN KEY (solicitanteid) REFERENCES USUARIOS(id)
);