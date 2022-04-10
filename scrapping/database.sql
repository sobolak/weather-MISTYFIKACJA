drop database weather;
create database weather;

use weather;

CREATE TABLE IF NOT EXISTS `weather`.`interia` (
  `id` INT  PRIMARY KEY auto_increment,
  `temperature` INT NULL,
  `wind` INT NULL,
  `humidity` INT NULL,
  `rain` FLOAT NULL,
  `cloudiness` INT NULL, 
  `update_time` VARCHAR(50) NULL,
  `weather_time` VARCHAR(20) NULL,
  `hour` INT NULL,
  `region` VARCHAR(20) NULL)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `weather`.`weatherChannel` (
  `id` INT  PRIMARY KEY auto_increment,
  `temperature` INT NULL,
  `wind` INT NULL,
  `humidity` INT NULL,
  `rain` FLOAT NULL,
  `cloudiness` INT NULL, 
  `update_time` VARCHAR(50) NULL,
  `weather_time` VARCHAR(20) NULL,
  `hour` INT NULL,
  `region` VARCHAR(20) NULL)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `weather`.`avenue` (
  `id` INT  PRIMARY KEY auto_increment,
  `temperature` INT NULL,
  `wind` INT NULL,
  `humidity` INT NULL,
  `rain` FLOAT NULL,
  `cloudiness` INT NULL, 
  `update_time` VARCHAR(50) NULL,
  `weather_time` VARCHAR(20) NULL,
  `hour` INT NULL,
  `region` VARCHAR(20) NULL)
ENGINE = InnoDB;


DELIMITER //
CREATE PROCEDURE  delete_interia (  weather_time_X VARCHAR(20), hour_X INT, region_X VARCHAR(20))BEGIN

  DELETE FROM interia WHERE weather_time = weather_time_X AND hour = hour_X AND region = region_X;

END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE  delete_weatherChannel (  weather_time_X VARCHAR(20), hour_X INT, region_X VARCHAR(20))BEGIN

  DELETE FROM weatherChannel WHERE weather_time = weather_time_X AND hour = hour_X AND region = region_X;

END; //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE  delete_avenue (  weather_time_X VARCHAR(20), hour_X INT, region_X VARCHAR(20))BEGIN

  DELETE FROM avenue WHERE weather_time = weather_time_X AND hour = hour_X AND region = region_X;

END; //
DELIMITER ;

