CREATE TABLE Anuncios (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    grupoid int,
    presupuesto int,
    pesomax float,
    cantmax int,
    compradorid int,
    hora int,
    minutos int,
    terminado boolean DEFAULT False,
    CONSTRAINT FK_Grupo_Anuncio FOREIGN KEY (grupoid)
        REFERENCES GRUPOS(id)
);