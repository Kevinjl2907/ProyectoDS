-- -----------------------------------------------------
-- Schema proyectoDisenoDb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `proyectoDisenoDb` ;

-- -----------------------------------------------------
-- Schema proyectoDisenoDb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `proyectoDisenoDb` DEFAULT CHARACTER SET utf8 ;
USE `proyectoDisenoDb` ;

-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Sede`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Sede` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Sede` (
  `idSede` INT NOT NULL,
  `codigoSede` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`idSede`));


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Estudiante`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Estudiante` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Estudiante` (
  `idEstDB` INT NOT NULL,
  `id` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `nombreAdicional` VARCHAR(45) NOT NULL,
  `apellido1` VARCHAR(45) NOT NULL,
  `apellido2` VARCHAR(45) NOT NULL,
  `sede` INT NOT NULL,
  `correoTec` VARCHAR(50) NOT NULL,
  `fedicion` DATETIME NULL,
  `editor` VARCHAR(120) NULL,
  `fcreacion` DATETIME NOT NULL,
  PRIMARY KEY (`idEstDB`),
  INDEX `sede_idx` (`sede` ASC) VISIBLE,
  CONSTRAINT `sedeEstudiante`
    FOREIGN KEY (`sede`)
    REFERENCES `proyectoDisenoDb`.`Sede` (`idSede`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`AsistenteAdministrativo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`AsistenteAdministrativo` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`AsistenteAdministrativo` (
  `idAsistente` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido1` VARCHAR(45) NOT NULL,
  `apellido2` VARCHAR(45) NOT NULL,
  `sede` INT NOT NULL,
  PRIMARY KEY (`idAsistente`),
  INDEX `sede_idx` (`sede` ASC) VISIBLE,
  CONSTRAINT `sedeAAdmi`
    FOREIGN KEY (`sede`)
    REFERENCES `proyectoDisenoDb`.`Sede` (`idSede`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Rol`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Rol` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Rol` (
  `idRol` INT NOT NULL,
  `desRol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idRol`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Profesor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Profesor` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Profesor` (
  `idProfesor` INT NOT NULL,
  `codigo` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido1` VARCHAR(45) NOT NULL,
  `apellido2` VARCHAR(45) NOT NULL,
  `oficina` VARCHAR(45) NOT NULL,
  `correo` VARCHAR(45) NOT NULL,
  `telOficina` INT NOT NULL,
  `telCelular` INT NOT NULL,
  `fotografia` BLOB NOT NULL,
  `rol` INT NOT NULL,
  `fcreacion` DATETIME NOT NULL,
  `fedicion` DATETIME NULL,
  PRIMARY KEY (`idProfesor`),
  INDEX `rol_idx` (`rol` ASC) VISIBLE,
  CONSTRAINT `rol`
    FOREIGN KEY (`rol`)
    REFERENCES `proyectoDisenoDb`.`Rol` (`idRol`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`EquipoTrabajo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`EquipoTrabajo` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`EquipoTrabajo` (
  `idEquipoTrabajo` INT NOT NULL,
  `coordinador` INT NOT NULL,
  `fedicion` DATETIME NULL,
  `editor` VARCHAR(45) NULL,
  PRIMARY KEY (`idEquipoTrabajo`),
  INDEX `coordinador_idx` (`coordinador` ASC) VISIBLE,
  CONSTRAINT `coordinador`
    FOREIGN KEY (`coordinador`)
    REFERENCES `proyectoDisenoDb`.`Profesor` (`idProfesor`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`TipoActividad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`TipoActividad` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`TipoActividad` (
  `idTipoActividad` INT NOT NULL,
  `desTipoActividad` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTipoActividad`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Actividad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Actividad` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Actividad` (
  `idActividad` INT NOT NULL,
  `semana` INT NOT NULL,
  `tipo` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `diaAviso` DATETIME NOT NULL,
  `diasRecordatorios` INT NOT NULL,
  `esVirtual` TINYINT(0) NOT NULL,
  `enlace` VARCHAR(100) NULL,
  `afiche` BLOB NOT NULL,
  `estado` INT NOT NULL,
  `comentario` VARCHAR(150) NULL,
  `fedicion` DATETIME NULL,
  `editor` VARCHAR(100) NULL,
  `Actividadcol` VARCHAR(45) NULL,
  PRIMARY KEY (`idActividad`),
  INDEX `tipoActividad_idx` (`tipo` ASC) VISIBLE,
  CONSTRAINT `tipoActividad`
    FOREIGN KEY (`tipo`)
    REFERENCES `proyectoDisenoDb`.`TipoActividad` (`idTipoActividad`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Comentario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Comentario` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Comentario` (
  `idComentario` INT NOT NULL,
  `contenido` VARCHAR(250) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `autor` INT NOT NULL,
  `actividad` INT NOT NULL,
  PRIMARY KEY (`idComentario`),
  INDEX `autor_idx` (`autor` ASC) VISIBLE,
  INDEX `actividad_idx` (`actividad` ASC) VISIBLE,
  CONSTRAINT `autor`
    FOREIGN KEY (`autor`)
    REFERENCES `proyectoDisenoDb`.`Profesor` (`idProfesor`)
    
    ,
  CONSTRAINT `actividadComentario`
    FOREIGN KEY (`actividad`)
    REFERENCES `proyectoDisenoDb`.`Actividad` (`idActividad`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Responsable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Responsable` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Responsable` (
  `idReponsable` INT NOT NULL,
  `idActividad` INT NOT NULL,
  `idProfesor` INT NOT NULL,
  PRIMARY KEY (`idReponsable`),
  INDEX `actividad_idx` (`idActividad` ASC) VISIBLE,
  INDEX `responsable_idx` (`idProfesor` ASC) VISIBLE,
  CONSTRAINT `actividadResponsable`
    FOREIGN KEY (`idActividad`)
    REFERENCES `proyectoDisenoDb`.`Actividad` (`idActividad`),
  CONSTRAINT `responsable`
    FOREIGN KEY (`idProfesor`)
    REFERENCES `proyectoDisenoDb`.`Profesor` (`idProfesor`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`PlanTrabajo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`PlanTrabajo` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`PlanTrabajo` (
  `idPlanTrabajo` INT NOT NULL,
  `id` INT NOT NULL,
  `semanaInicial` DATE NOT NULL,
  `semanafinal` DATE NOT NULL,
  `actividades` INT NOT NULL,
  PRIMARY KEY (`idPlanTrabajo`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`ActividadesPlanTrabajo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`ActividadesPlanTrabajo` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`ActividadesPlanTrabajo` (
  `idPK` INT NOT NULL,
  `idPlanTrabajo` INT NOT NULL,
  `idActividad` INT NOT NULL,
  PRIMARY KEY (`idPK`),
  INDEX `planTrabajo_idx` (`idPlanTrabajo` ASC) VISIBLE,
  INDEX `actividad_idx` (`idActividad` ASC) VISIBLE,
  CONSTRAINT `planTrabajoPlan`
    FOREIGN KEY (`idPlanTrabajo`)
    REFERENCES `proyectoDisenoDb`.`PlanTrabajo` (`idPlanTrabajo`),
  CONSTRAINT `actividadPlan`
    FOREIGN KEY (`idActividad`)
    REFERENCES `proyectoDisenoDb`.`Actividad` (`idActividad`)
    
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`Docentes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`Docentes` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`Docentes` (
  `idListaDocentes` INT NOT NULL,
  `idEquipoTrabajo` INT NOT NULL,
  `idProfesor` INT NOT NULL,
  `esRepresentante` TINYINT(1) NOT NULL,
  PRIMARY KEY (`idListaDocentes`),
  INDEX `equipoTrabajo_idx` (`idEquipoTrabajo` ASC) VISIBLE,
  INDEX `profesor_idx` (`idProfesor` ASC) VISIBLE,
  CONSTRAINT `equipoTrabajo`
    FOREIGN KEY (`idEquipoTrabajo`)
    REFERENCES `proyectoDisenoDb`.`EquipoTrabajo` (`idEquipoTrabajo`),
  CONSTRAINT `profesor`
    FOREIGN KEY (`idProfesor`)
    REFERENCES `proyectoDisenoDb`.`Profesor` (`idProfesor`)
);


-- -----------------------------------------------------
-- Table `proyectoDisenoDb`.`SemanasVacaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyectoDisenoDb`.`SemanasVacaciones` ;

CREATE TABLE IF NOT EXISTS `proyectoDisenoDb`.`SemanasVacaciones` (
  `idSemanasVacaciones` INT NOT NULL,
  `semanaVacacional` DATE NOT NULL,
  `idPlanTrabajo` INT NOT NULL,
  PRIMARY KEY (`idSemanasVacaciones`),
  INDEX `planTrabajo_idx` (`idPlanTrabajo` ASC) VISIBLE,
  CONSTRAINT `planTrabajoVacaciones`
    FOREIGN KEY (`idPlanTrabajo`)
    REFERENCES `proyectoDisenoDb`.`PlanTrabajo` (`idPlanTrabajo`)
);
