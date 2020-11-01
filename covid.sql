drop database if exists covid;
create database covid;
use covid;

create table total( 
fecha varchar(100)  primary key, 
Casos varchar(30), 
Recuperados varchar(30),
 Hospitalizados varchar(30),
 Unidades varchar(30), 
 Muertes varchar(30)); 
 
 create table localidades( 
 fecha varchar(100),
 nombre varchar(30), 
 casos varchar(30));
 
 create table depa( 
 fecha varchar(100),
 nombre varchar(30), 
 casos varchar(30));
 
Select * from localidades;
Select * from depa;
Select * from total;