CREATE TABLE Cobros_X_Pedidos (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    cobroid int,
    pedidoid int,
    CONSTRAINT FK_Cobro FOREIGN KEY (cobroid) REFERENCES Cobros(id),
    CONSTRAINT FK_Pedido FOREIGN KEY (pedidoid) REFERENCES Pedidos(id)
);