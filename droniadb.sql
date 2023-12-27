BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "map_operador" (
	"id_operador"	INT,
	"nombre"	VARCHAR(50),
	"apellido"	VARCHAR(50),
	"mail"	VARCHAR(254),
	PRIMARY KEY("id_operador")
);
CREATE TABLE IF NOT EXISTS "map_imagenes" (
	"id_imagen"	integer NOT NULL,
	"nombre_imagen"	varchar(255),
	"create_at"	datetime NOT NULL,
	"update_at"	datetime NOT NULL,
	"vuelo_id"	integer NOT NULL,
	"analizada"	bool NOT NULL,
	"image_file"	varchar(100),
	"resultado"	text,
	"porcentaje_prediccion"	decimal,
	FOREIGN KEY("vuelo_id") REFERENCES "map_vuelo"("id_vuelo") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id_imagen" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "map_ubicaciones" (
	"id_ubicaciones"	integer NOT NULL,
	"direccion"	varchar(255),
	"vuelo_id_id"	integer,
	FOREIGN KEY("vuelo_id_id") REFERENCES "map_vuelo"("id_vuelo") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id_ubicaciones" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "map_vuelo" (
	"id_vuelo"	integer NOT NULL,
	"sector_vuelo"	varchar(255) NOT NULL,
	"fecha_vuelo"	date NOT NULL,
	"create_at"	datetime NOT NULL,
	"update_at"	datetime NOT NULL,
	"cantidad_imagenes"	integer NOT NULL,
	"cantidad_predicciones"	integer NOT NULL,
	"operador_id"	integer,
	"latitud"	real,
	"longitud"	real,
	"cantidad_imagenes_nuevas"	integer NOT NULL,
	FOREIGN KEY("operador_id") REFERENCES "map_operador"("id_operador") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id_vuelo" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "map_areamuestreo" (
	"id"	integer NOT NULL,
	"direccion"	varchar(200) NOT NULL,
	"latitud"	decimal NOT NULL,
	"longitud"	decimal NOT NULL,
	"detecciones"	integer NOT NULL,
	"especieArbol"	varchar(200),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "map_imagenes" ("id_imagen","nombre_imagen","create_at","update_at","vuelo_id","analizada","image_file","resultado","porcentaje_prediccion") VALUES (1,'DJI_0140.jpg','2023-12-27 01:23:51.919097','2023-12-27 01:23:51.919097',1,1,'','Durazno',96.2),
 (2,'DJI_0050.jpg','2023-12-27 01:27:12.510225','2023-12-27 01:27:12.510225',2,1,'','Olivo',100),
 (3,'DJI_0110.jpg','2023-12-27 01:27:13.218004','2023-12-27 01:27:13.218004',2,1,'','Olivo',99),
 (4,'DJI_0160.jpg','2023-12-27 01:53:53.185772','2023-12-27 01:53:53.185772',3,1,'','Palto',99.5);
INSERT INTO "map_vuelo" ("id_vuelo","sector_vuelo","fecha_vuelo","create_at","update_at","cantidad_imagenes","cantidad_predicciones","operador_id","latitud","longitud","cantidad_imagenes_nuevas") VALUES (1,'sector 1','2023-08-16','2023-12-27 01:23:26.959096','2023-12-27 01:23:26.959096',0,0,NULL,NULL,NULL,0),
 (2,'sector 2','2023-09-01','2023-12-27 01:26:46.720489','2023-12-27 01:26:46.720489',0,0,NULL,NULL,NULL,0),
 (3,'Sector 3','2023-12-09','2023-12-27 01:53:14.028633','2023-12-27 01:53:14.028633',0,0,NULL,NULL,NULL,0);
INSERT INTO "map_areamuestreo" ("id","direccion","latitud","longitud","detecciones","especieArbol") VALUES (1,'Av el palomar',-27.368683,-70.320124,0,NULL),
 (2,'Muestreo Casa De barro 677',-27.368683,-70.328549,0,NULL),
 (3,'Muestreo 0123',-27.366207,-70.326789,0,NULL),
 (4,'Muestreo 555',-27.366207,-70.341242,0,NULL);
CREATE INDEX IF NOT EXISTS "map_imagenes_vuelo_id_1b325c2b" ON "map_imagenes" (
	"vuelo_id"
);
CREATE INDEX IF NOT EXISTS "map_ubicaciones_vuelo_id_id_a83c4867" ON "map_ubicaciones" (
	"vuelo_id_id"
);
CREATE INDEX IF NOT EXISTS "map_vuelo_operador_id_c10277ea" ON "map_vuelo" (
	"operador_id"
);
COMMIT;
