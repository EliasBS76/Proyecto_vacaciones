CREATE DATABASE REPORTE_LIBROS
USE REPORTE_LIBROS
USE REPORTES
CREATE TABLE autor (
  id BIGINT PRIMARY KEY IDENTITY(1,1),
  nombre NVARCHAR(45) NOT NULL,
  nacionalidad NVARCHAR(45)
);

CREATE TABLE libro (
  id BIGINT PRIMARY KEY IDENTITY(1,1),
  titulo NVARCHAR(55) NOT NULL,
  genero NVARCHAR(40)NOT NULL,
  precio int NOT NULL ,
  autor_id BIGINT FOREIGN KEY REFERENCES autor(id),
  
);

CREATE TABLE venta (
  id BIGINT PRIMARY KEY IDENTITY(1,1),
  libro_id BIGINT FOREIGN KEY REFERENCES libro(id),
  continente varchar(25),
  enero INT DEFAULT 0,
  febrero INT DEFAULT 0,
  marzo INT DEFAULT 0,
  abril INT DEFAULT 0,
  mayo INT DEFAULT 0,
  junio INT DEFAULT 0,
  julio INT DEFAULT 0,
  agosto INT DEFAULT 0,
  septiembre INT DEFAULT 0,
  octubre INT DEFAULT 0,
  noviembre INT DEFAULT 0,
  diciembre INT DEFAULT 0,
  venta_anual INT DEFAULT 0
  )


SELECT id,nombre  FROM autor
SELECT * FROM libro
SELECT * FROM venta
DROP DATABASE REPORTE_LIBROS

