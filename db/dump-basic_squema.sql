-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: pruebabd
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.19-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE DATABASE /*!32312 IF NOT EXISTS*/ `pruebaBD` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `pruebaBD`;
--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES 
  -- Punto de encuentro 
  (1,'punto_encuentro_index'),
  (2,'punto_encuentro_new'),
  (13,'punto_encuentro_create'),
  (3,'punto_encuentro_destroy'),
  (14,'punto_encuentro_edit'),
  (4,'punto_encuentro_update'),
  (5,'punto_encuentro_show'),
  -- Recorridos de evacuación 
  (19,'evacuation_route_index'),
  (20,'evacuation_route_new'),
  (21,'evacuation_route_create'),
  (22,'evacuation_route_destroy'),
  (23,'evacuation_route_edit'),
  (24,'evacuation_route_update'),
  (25,'evacuation_route_show'),
    -- Denuncias 
  (28,'complaint_index'),
  (29,'complaint_new'),
  (30,'complaint_create'),
  (31,'complaint_destroy'),
  (32,'complaint_edit'),
  (33,'complaint_update'),
  (34,'complaint_show'),
  -- USER
  (6,'usuario_index'),
  (7,'usuario_new'),
  (8,'usuario_destroy'),
  (9,'usuario_update'),
  (10,'usuario_show'),
  (26,'usuario_show_my_profile'),
  (27,'usuario_update_my_profile'),
  -- CONFIG
  (11,'config_show'),
  (12,'config_update');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_has_permissions`
--

DROP TABLE IF EXISTS `role_has_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_has_permissions` (
  `role_id` int(11) unsigned NOT NULL,
  `permission_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `role_id` (`role_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_has_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`),
  CONSTRAINT `role_has_permissions_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_has_permissions`
--

LOCK TABLES `role_has_permissions` WRITE;
/*!40000 ALTER TABLE `role_has_permissions` DISABLE KEYS */;
INSERT INTO `role_has_permissions` VALUES 
  -- ADMIN
  (1,1),
  (1,2),
  (1,3),
  (1,4),
  (1,5),
  (1,6),
  (1,7),
  (1,8),
  (1,9),
  (1,10),
  (1,11),
  (1,12),
  (1,13),
  (1,14),
  (1,26),
  (1,27),
  (1,19),
  (1,20),
  (1,21),
  (1,22),
  (1,23),
  (1,24),
  (1,25),
  (1,28),
  (1,29),
  (1,30),
  (1,31),
  (1,32),
  (1,33),
  (1,34),
  -- OPERATOR
  (2,1),
  (2,2),
  (2,4),
  (2,5),
  (2,13),
  (2,14),
  (2,26),
  (2,27),
  (2,19),
  (2,20),
  (2,21),
  (2,23),
  (2,24),
  (2,25),
  (2,28),
  (2,29),
  (2,30),
  (2,32),
  (2,33),
  (2,34);
  -- (2,6),
  -- (2,7),
  -- (2,9),
  -- (2,10)
/*!40000 ALTER TABLE `role_has_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'rol_administrador'),(2,'rol_operador');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_has_roles`
--

DROP TABLE IF EXISTS `user_has_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_has_roles` (
  `user_id` int(11) unsigned NOT NULL,
  `role_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_has_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_has_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_has_roles`
--

LOCK TABLES `user_has_roles` WRITE;
/*!40000 ALTER TABLE `user_has_roles` DISABLE KEYS */;
INSERT INTO `user_has_roles` VALUES (1,1),(2,2),(3,2);
/*!40000 ALTER TABLE `user_has_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(150) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` longtext NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
-- Las contraseñas de estos usuarios son "123123"
  (1,'admin@gmail.com','administrador','$2a$12$NqYB/2oRmZEuuWmACDX4cuM/g5Ez1JCsHN20zo/Ds4mTtX6zT806O','Cosme','Fulanito',1,0,'2021-10-02 14:46:18','2021-10-02 14:46:18'),
  (2,'ron@gmail.com','operador1','$2a$12$nAy4sJ2yWS14H2TiMROS..Df52NS72jLwJbsOHJ9nYVumxn9n/LRe','Ron','Perez',1,0,'2021-10-02 14:46:18','2021-10-02 14:46:18');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `configuration`
--

DROP TABLE IF EXISTS `configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuration` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `elements_quantity` int(5) NOT NULL DEFAULT 50,
  `order_by` varchar(25) NOT NULL DEFAULT 'asc',
  `colors_id_public` int(11) unsigned NOT NULL,
  `colors_id_private` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`colors_id_public`),
  KEY (`colors_id_private`),
  CONSTRAINT `config_ibfk_1` FOREIGN KEY (`colors_id_public`) REFERENCES `colors` (`id`),
  CONSTRAINT `config_ibfk_2` FOREIGN KEY (`colors_id_private`) REFERENCES `colors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration`
--

LOCK TABLES `configuration` WRITE;
/*!40000 ALTER TABLE `configuration` DISABLE KEYS */;
INSERT INTO `configuration` VALUES (1,'50', 'asc', 1, 2);
/*!40000 ALTER TABLE `configuration` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `colors`
--

DROP TABLE IF EXISTS `colors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colors` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `color_1` varchar(15) NOT NULL COMMENT 'Textos con color, gradient(der) botones',
  `color_2` varchar(15) NOT NULL COMMENT 'gradient(izq) botones',
  `color_3` varchar(15) NOT NULL COMMENT 'background header',
  `color_4` varchar(15) NOT NULL COMMENT 'ilustraciones',
  `color_5` varchar(15) NOT NULL COMMENT 'background app',
  PRIMARY KEY (`id`),
  KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `colors` WRITE;
/*!40000 ALTER TABLE `colors` DISABLE KEYS */;
INSERT INTO `colors` VALUES 
  (1,'#00D9F5','#00F5A0','#C6FCE5','#63FFC2','#F5FFFD'), 
  (2,'#F1BD04','#F50F00','#FCE6C6','#FFAE63','#FFFAF5'),
  (3,'#0463F1','#F500CE','#C6D8FC','#637CFF','#F5F8FF'),
  (4,'#F50000','#0045F5','#FCC6D3','#8D1CD2','#FFF5F5'), 
  (5,'#EFA8E4','#34E8FF','#F8E1F4','#9CD7F6','#FFF7FA'),
  (6,'#B8DFD8','#FFB319','#FFF0C9','#F8CC32','#F3F3F0');
/*!40000 ALTER TABLE `colors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meeting_point`
--

DROP TABLE IF EXISTS `meeting_point`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meeting_point` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL ,
  `address` varchar(255) NOT NULL,
  `coor_X` varchar(100),
  `coor_Y` varchar(100),
  `state` varchar(100),
  `telephone` varchar(50),
  `email` varchar(150),
  PRIMARY KEY (`id`),
  KEY (`id`),
  KEY (`address`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meeting_point`
--

LOCK TABLES `meeting_point` WRITE;
/*!40000 ALTER TABLE `meeting_point` DISABLE KEYS */;
INSERT INTO `meeting_point` VALUES 
  (1,'Polideportivo Los Hornos','66 y 153','121','341','publicated', '234165', 'polideportivo@gmail.com'), 
  (2,'Pasaje Dardo Rocha','7 y 50','421','500','despublicated', '232157', 'pasaje@hotmail.com'), 
  (3,'Estadio Único','32 y 25','311','560','publicated', '532557', 'estadio@hotmail.com'), 
  (4,'Meridiano V','17 y 72','223','213','publicated', '352157', 'meridiano@gmail.com'), 
  (5,'Hipódromo','44 y 115','503','921','despublicated', '842348', 'hipódromo@gmail.com'),
  (6,'Centro Comunal Villa Elvira','82 e/ 7 y 8','324','102','despublicated', '932145', 'villaelvira@gmail.com'),
  (7,'Centro Comunal Ringuelet','Av. 7 2180','142', '441', 'publicated', '934549', 'ringuelet@gmail.com'),
  (8,'Centro Comunal Abasto','516 bis e/210 y 211','572', '111', 'publicated', '632172', 'abasto@gmail.com'),
  (9,'Centro Comunal Arana','131 e/ 636 y 637','321', '401', 'publicated', '622571', 'arana@hotmail.com'),
  (10,'Centro Comunal Gorina','140 bis y 489','222', '303', 'despublicated', '992231', 'gorina@hotmail.com');
/*!40000 ALTER TABLE `meeting_point` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `evacuation_route`
--

DROP TABLE IF EXISTS `evacuation_route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evacuation_route` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) NOT NULL,
  `state` varchar(100),
  PRIMARY KEY (`id`),
  KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `complaint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `closed_at` datetime NULL,
  `description` varchar(500) NOT NULL,
  `state` varchar(100),
  `creator_first_name` varchar(100),
  `creator_last_name` varchar(100),
  `creator_telephone` varchar(50),
  `creator_email` varchar(150),
  `assigned_to` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`id`),
  KEY `assigned_to` (`assigned_to`),
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`assigned_to`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `complaint follow up`
--

DROP TABLE IF EXISTS `complaint_follow_up`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `complaint_follow_up` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(500) NOT NULL,
  `author_id` int(11) unsigned NOT NULL,
  `complaint_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `complaint_id` (`complaint_id`),
  CONSTRAINT `complaint_follow_up_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `complaint_follow_up_ibfk_2` FOREIGN KEY (`complaint_id`) REFERENCES `complaint` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coordinate`
--

DROP TABLE IF EXISTS `coordinate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coordinate` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `latitude` varchar(100) NOT NULL,
  `longitude` varchar(100) NOT NULL,
  `evacuation_route_id` int(11) DEFAULT NULL,
  `complaint_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `latitude_longitude` (`latitude`,`longitude`) USING BTREE,
  KEY `evacuation_route_id` (`evacuation_route_id`),
  KEY `complaint_id` (`complaint_id`),
  CONSTRAINT `coordinate_ibfk_1` FOREIGN KEY (`evacuation_route_id`) REFERENCES `evacuation_route` (`id`),
  CONSTRAINT `coordinate_ibfk_2` FOREIGN KEY (`complaint_id`) REFERENCES `complaint` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Dumping routines for database 'pruebabd'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-02 14:47:23




-- COMENTARIOS

-- CREATE TABLE `users` (
-- `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `email` varchar(30) NOT NULL,
-- `username` varchar(30) NOT NULL,
-- `password` varchar(30) NOT NULL,
-- `first_name` varchar(30) NOT NULL,
-- `last_name` varchar(30) NOT NULL,
-- `activo` tinyint(1) NOT NULL,
-- `created_at` datetime DEFAULT NULL,
-- `updated_at` datetime DEFAULT NULL,
-- `Column1` varchar(100) DEFAULT NULL COMMENT 'sdfsdfsdf',
-- PRIMARY KEY (`id`),
-- UNIQUE KEY `email` (`email`),
-- UNIQUE KEY `username` (`username`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1