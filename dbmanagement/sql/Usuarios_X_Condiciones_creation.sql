CREATE TABLE Usuarios_X_Condiciones (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1, NO CACHE ),
    usuarioid int NOT NULL,
    condicionid int NOT NULL,
    CONSTRAINT FK_Usuario_Condicion FOREIGN KEY (usuarioid) REFERENCES USUARIOS(id),
    CONSTRAINT FK_Usuario_Condicion_2 FOREIGN KEY (condicionid) REFERENCES CONDICIONES(id)
);