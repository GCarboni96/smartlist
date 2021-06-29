CREATE TABLE Productos (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    nombre varchar(255) NOT NULL,
    img varchar(255),
    peso float NOT NULL,
    precio int NOT NULL,
    tiendaid int NOT NULL,
    necesidad float DEFAULT 0.5
);
