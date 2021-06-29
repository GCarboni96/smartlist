CREATE TABLE Tiendas (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    nombre varchar(255) NOT NULL,
    tipo varchar(255),
    logo varchar(255)
);