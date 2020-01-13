CREATE DATABASE  IF NOT EXISTS `flow_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `flow_db`;
-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: flow_db
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rtsp_tcptb`
--

DROP TABLE IF EXISTS `rtsp_tcptb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rtsp_tcptb` (
  `sip` varchar(15) NOT NULL,
  `dip` varchar(15) NOT NULL,
  `sport` smallint(5) unsigned NOT NULL,
  `dport` smallint(5) unsigned NOT NULL,
  `session` varchar(24) NOT NULL,
  `starttime` timestamp NULL DEFAULT NULL,
  `endtime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`sip`,`dip`,`sport`,`dport`,`session`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `rtsp_tcptb_BEFORE_DELETE` BEFORE DELETE ON `rtsp_tcptb` FOR EACH ROW BEGIN
insert ignore into rtsp_tcptb_backup
values(old.sip,old.dip,old.sport,old.dport,old.session,old.starttime,current_timestamp);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rtsp_tcptb_backup`
--

DROP TABLE IF EXISTS `rtsp_tcptb_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rtsp_tcptb_backup` (
  `sip` varchar(15) NOT NULL,
  `dip` varchar(15) NOT NULL,
  `sport` smallint(5) unsigned NOT NULL,
  `dport` smallint(5) unsigned NOT NULL,
  `session` varchar(24) NOT NULL,
  `starttime` timestamp NOT NULL,
  `endtime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sip`,`dip`,`sport`,`dport`,`session`,`starttime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rtsp_udptb`
--

DROP TABLE IF EXISTS `rtsp_udptb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rtsp_udptb` (
  `sip` varchar(15) NOT NULL,
  `dip` varchar(15) NOT NULL,
  `sport` smallint(5) unsigned NOT NULL,
  `dport` smallint(5) unsigned NOT NULL,
  `session` varchar(24) NOT NULL,
  `starttime` timestamp NULL DEFAULT NULL,
  `endtime` timestamp NULL DEFAULT NULL,
  `client_port` json DEFAULT NULL,
  `server_port` json DEFAULT NULL,
  PRIMARY KEY (`sip`,`dip`,`sport`,`dport`,`session`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `rtsp_udptb_BEFORE_DELETE` BEFORE DELETE ON `rtsp_udptb` FOR EACH ROW BEGIN
insert ignore into rtsp_udptb_backup 
values (old.sip,old.dip,old.sport,old.dport,old.session,old.starttime,current_timestamp,old.client_port,old.server_port);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rtsp_udptb_backup`
--

DROP TABLE IF EXISTS `rtsp_udptb_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rtsp_udptb_backup` (
  `sip` varchar(15) NOT NULL,
  `dip` varchar(15) NOT NULL,
  `sport` smallint(5) unsigned NOT NULL,
  `dport` smallint(5) unsigned NOT NULL,
  `session` varchar(24) NOT NULL,
  `starttime` timestamp NOT NULL,
  `endtime` timestamp NULL DEFAULT NULL,
  `client_port` json DEFAULT NULL,
  `server_port` json DEFAULT NULL,
  PRIMARY KEY (`sip`,`dip`,`sport`,`dport`,`session`,`starttime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-25 14:54:30
