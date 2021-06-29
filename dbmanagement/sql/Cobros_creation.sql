CREATE TABLE Cobros (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    cobrado boolean NOT NULL DEFAULT False,
    cobradorid int,
    deudorid int,
    productonombre varchar(255),
    pedidoprecio int,
    pedidocantidad int,
    tienda varchar(255),
    CONSTRAINT FK_Deudor_Cobro FOREIGN KEY (deudorid) REFERENCES Usuarios(id),
    CONSTRAINT FK_Cobrador_Cobro FOREIGN KEY (cobradorid) REFERENCES Usuarios(id)
);