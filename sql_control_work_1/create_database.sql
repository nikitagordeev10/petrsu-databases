--DROP TABLE IF EXISTS tblParticipate;
--DROP TABLE IF EXISTS tblUse;
--DROP TABLE IF EXISTS tblDelivery;
--ALTER TABLE tblProject DROP CONSTRAINT IF EXISTS FK_tblWorker;
--DROP TABLE IF EXISTS tblWorker;
--DROP TABLE IF EXISTS tblProvider;
--DROP TABLE IF EXISTS tblDetail;
--DROP TABLE IF EXISTS tblProject;

--CREATE DATABASE ProductionManagement;

USE ProductionManagement;

CREATE TABLE tblWorker (
  id_worker INT PRIMARY KEY,
  name VARCHAR(50),
  spec VARCHAR(50),
  status INT
);

CREATE TABLE tblProject (
  id_project INT PRIMARY KEY,
  name VARCHAR(50),
  boss INT,
  deadline DATE,
  FOREIGN KEY (boss) REFERENCES tblWorker(id_worker)
);

CREATE TABLE tblParticipate (
  id_project INT,
  id_worker INT,
  salary DECIMAL(10,2),
  PRIMARY KEY (id_project, id_worker),
  FOREIGN KEY (id_project) REFERENCES tblProject(id_project),
  FOREIGN KEY (id_worker) REFERENCES tblWorker(id_worker)
);

CREATE TABLE tblDetail (
  id_detail INT PRIMARY KEY,
  name VARCHAR(30),
  color VARCHAR(20),
  city VARCHAR(40),
  weight DECIMAL(8,2)
);

CREATE TABLE tblUse (
  id_project INT,
  id_detail INT,
  number INT,
  PRIMARY KEY (id_project, id_detail),
  FOREIGN KEY (id_project) REFERENCES tblProject(id_project),
  FOREIGN KEY (id_detail) REFERENCES tblDetail(id_detail)
);

CREATE TABLE tblProvider (
  id_provider INT PRIMARY KEY,
  name VARCHAR(30),
  city VARCHAR(40),
  status INT
);

CREATE TABLE tblDelivery (
  id_delivery INT PRIMARY KEY,
  id_detail INT,
  id_provider INT,
  number INT,
  FOREIGN KEY (id_detail) REFERENCES tblDetail(id_detail),
  FOREIGN KEY (id_provider) REFERENCES tblProvider(id_provider)
);