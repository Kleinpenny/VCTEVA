-- MySQL dump 10.13  Distrib 9.1.0, for macos14 (arm64)
--
-- Host: localhost    Database: VCTEVA
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE vcteva;
--
-- Table structure for table `Agents`
--

DROP TABLE IF EXISTS `Agents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Agents` (
  `agent_id` int NOT NULL AUTO_INCREMENT,
  `map_id` int DEFAULT NULL,
  `games_win` int DEFAULT NULL,
  `games_count` int DEFAULT NULL,
  PRIMARY KEY (`agent_id`),
  KEY `map_id` (`map_id`),
  CONSTRAINT `agents_ibfk_1` FOREIGN KEY (`map_id`) REFERENCES `Maps` (`map_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1716 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Agents`
--

LOCK TABLES `Agents` WRITE;
/*!40000 ALTER TABLE `Agents` DISABLE KEYS */;
/*!40000 ALTER TABLE `Agents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DamageDetails`
--

DROP TABLE IF EXISTS `DamageDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DamageDetails` (
  `damage_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `head_count` int DEFAULT NULL,
  `head_amount` float DEFAULT NULL,
  `body_count` int DEFAULT NULL,
  `body_amount` float DEFAULT NULL,
  `leg_count` int DEFAULT NULL,
  `leg_amount` float DEFAULT NULL,
  `general_count` int DEFAULT NULL,
  `general_amount` float DEFAULT NULL,
  PRIMARY KEY (`damage_id`),
  KEY `agent_id` (`agent_id`),
  CONSTRAINT `damagedetails_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `Agents` (`agent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=491 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DamageDetails`
--

LOCK TABLES `DamageDetails` WRITE;
/*!40000 ALTER TABLE `DamageDetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `DamageDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Maps`
--

DROP TABLE IF EXISTS `Maps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Maps` (
  `map_id` int NOT NULL AUTO_INCREMENT,
  `tournament_id` int DEFAULT NULL,
  `map_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`map_id`),
  KEY `tournament_id` (`tournament_id`),
  CONSTRAINT `maps_ibfk_1` FOREIGN KEY (`tournament_id`) REFERENCES `Tournaments` (`tournament_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1653 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Maps`
--

LOCK TABLES `Maps` WRITE;
/*!40000 ALTER TABLE `Maps` DISABLE KEYS */;
/*!40000 ALTER TABLE `Maps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PerformanceDetails`
--

DROP TABLE IF EXISTS `PerformanceDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PerformanceDetails` (
  `performance_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int DEFAULT NULL,
  `mode` varchar(10) DEFAULT NULL,
  `kills` int DEFAULT NULL,
  `deaths` int DEFAULT NULL,
  `assists` int DEFAULT NULL,
  `rounds_taken` int DEFAULT NULL,
  `rounds_win` int DEFAULT NULL,
  `cause` json DEFAULT NULL,
  PRIMARY KEY (`performance_id`),
  KEY `agent_id` (`agent_id`),
  CONSTRAINT `performancedetails_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `Agents` (`agent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=491 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PerformanceDetails`
--

LOCK TABLES `PerformanceDetails` WRITE;
/*!40000 ALTER TABLE `PerformanceDetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `PerformanceDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players`
--

DROP TABLE IF EXISTS `Players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Players` (
  `player_id` varchar(50) NOT NULL,
  `handle` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `team_id` varchar(50) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  `league` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players`
--

LOCK TABLES `Players` WRITE;
/*!40000 ALTER TABLE `Players` DISABLE KEYS */;
/*!40000 ALTER TABLE `Players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SummaryPerGame`
--

DROP TABLE IF EXISTS `SummaryPerGame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SummaryPerGame` (
  `summary_id` int NOT NULL AUTO_INCREMENT,
  `agent_id` int DEFAULT NULL,
  `combat_score` float DEFAULT NULL,
  `average_combat_score` float DEFAULT NULL,
  `kills` float DEFAULT NULL,
  `deaths` float DEFAULT NULL,
  `assists` float DEFAULT NULL,
  `kpr` float DEFAULT NULL,
  `dpr` float DEFAULT NULL,
  `total_damage_taken` float DEFAULT NULL,
  `total_damage_caused` float DEFAULT NULL,
  `average_damage_per_round` float DEFAULT NULL,
  `average_damage_taken_per_round` float DEFAULT NULL,
  `dddelta` float DEFAULT NULL,
  `headshot_hit_rate` float DEFAULT NULL,
  PRIMARY KEY (`summary_id`),
  KEY `agent_id` (`agent_id`),
  CONSTRAINT `summarypergame_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `Agents` (`agent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SummaryPerGame`
--

LOCK TABLES `SummaryPerGame` WRITE;
/*!40000 ALTER TABLE `SummaryPerGame` DISABLE KEYS */;
/*!40000 ALTER TABLE `SummaryPerGame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tournaments`
--

DROP TABLE IF EXISTS `Tournaments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tournaments` (
  `tournament_id` int NOT NULL AUTO_INCREMENT,
  `player_id` varchar(50) DEFAULT NULL,
  `tournament_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `tournaments_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1653 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tournaments`
--

LOCK TABLES `Tournaments` WRITE;
/*!40000 ALTER TABLE `Tournaments` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tournaments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-17 23:17:20
