-- Adminer 4.8.1 MySQL 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `aplikacja_turystyczna`;
CREATE DATABASE `aplikacja_turystyczna` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `aplikacja_turystyczna`;

DROP TABLE IF EXISTS `achievements`;
CREATE TABLE `achievements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_points` int(11) NOT NULL COMMENT 'Określa ilość punktów za każdą odwiedzoną lokalizację przez użytkownika',
  `description` text NOT NULL COMMENT 'Opis za co zostały przyznane punkty',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `achievements` (`id`, `user_points`, `description`) VALUES
(1,	5,	'NASTĘPNY PRZYSTANEK... (KOLEJKOWO)'),
(2,	10,	'AZJA WZYWA! (OGRÓD JAPOŃSKI)'),
(3,	15,	'WODNE ATRAKCJE! (FONTANNY BLISKO HALI STULECIA)'),
(4,	20,	'POŚRÓD DZIKICH ZWIĘRZĄT! (WROCŁAWSKIE ZOO)'),
(5,	25,	'JAK TO ZOSTAŁO NAMALOWANE? (PANORAMA RACŁAWICKA)'),
(6,	30,	'SPOTKANIE Z HISTORIĄ! (MUZEUM NARODOWE)'),
(7,	35,	'PODNIEBNA PRZEPRAWA! (POLINKA PWR)'),
(8,	40,	'W GŁĘBINACH OCEANU! (HYDROPOLIS)'),
(9,	45,	'NIEZŁE WIDOKI! (SKY TOWER)'),
(10,	50,	'JEDEN BY RZĄDZIĆ NIMI WSZYSTKIMI! (PAPA KRASNAL RYNEK)');

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `poi`;
CREATE TABLE `poi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(60) NOT NULL,
  `description` text NOT NULL,
  `longitude` decimal(7,5) NOT NULL,
  `latitude` decimal(7,5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(10) NOT NULL,
  `login` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_achievements`;
CREATE TABLE `user_achievements` (
  `user_id` int(11) NOT NULL,
  `achievements_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `achievements_id` (`achievements_id`),
  CONSTRAINT `achievements_user-achievements` FOREIGN KEY (`achievements_id`) REFERENCES `achievements` (`id`),
  CONSTRAINT `user_achievements_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_comments_poi`;
CREATE TABLE `user_comments_poi` (
  `user_id` int(11) NOT NULL,
  `poi_id` int(11) NOT NULL,
  `comments_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `poi_id` (`poi_id`),
  KEY `comments_id` (`comments_id`),
  CONSTRAINT `user_comments_poi_ibfk_1` FOREIGN KEY (`comments_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `user_comments_poi_ibfk_3` FOREIGN KEY (`poi_id`) REFERENCES `poi` (`id`),
  CONSTRAINT `user_comments_poi_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user_poi` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_poi`;
CREATE TABLE `user_poi` (
  `poi_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `poi_id` (`poi_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `poi_user-poi` FOREIGN KEY (`poi_id`) REFERENCES `poi` (`id`),
  CONSTRAINT `user_user-poi` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2024-05-20 13:03:07
