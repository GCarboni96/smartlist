CREATE TABLE Usuarios(
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    nombre varchar(255) NOT NULL,
    clave varchar(255) NOT NULL,
    fechanacimiento date,
    grupoid int,
    admin boolean,
    participacion float DEFAULT 0.5,
    vulnerabilidad float DEFAULT 0.5,
    starving float DEFAULT 0.5,
    morosidad int DEFAULT 5,
    CONSTRAINT FK_Grupo_Usuario FOREIGN KEY (grupoid)
        REFERENCES GRUPOS(id)
);