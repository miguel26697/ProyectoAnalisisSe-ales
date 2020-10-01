drop database if exists covid;
create database covid;
use covid;

create table casos(
id_casos varchar(15) primary key,
numCasos int,
numCasosHoy int,
numHospi int,
numHospiHoy int,
numFalle int,
numFalleHoy int,
numCasa int,
numCasaHoy int, 
numRecupe int,
numRecupeHoy int,
numUci int,
numUciHoy int);


select * from casos where id_casos = "2020-09-29";

select * from casos