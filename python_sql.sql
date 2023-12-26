-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: pythonlogin
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'장성웅','qwer1211','wkdtjddnd10@naver.com',0),(3,'ㅈ라ㅣㅟㅈ라ㅣㄹ다ㅣㅈ','efklnfwnelknl','feklwnkelnekl@naver.com',0),(4,'장성우','qwer1234','wkdtjddn1@naver.com',1),(5,'efwe','wefef','ewfe@naver.com',1),(6,'김이박','qwer1234','rladlqkr1@naver.com',1),(7,'아아아','qwer1234','wfklenlnlkfe@naver.com',1),(8,'장성웅','qwer1211','storyone01@naver.com',0),(9,'장성웅','qwer1211','wkdtjddnd1@naver.com',1),(10,'장성웅','qwer1234','starrar1@naver.com',1);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploaded_files`
--

DROP TABLE IF EXISTS `uploaded_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploaded_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  `upload_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `uploaded_files_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploaded_files`
--

LOCK TABLES `uploaded_files` WRITE;
/*!40000 ALTER TABLE `uploaded_files` DISABLE KEYS */;
INSERT INTO `uploaded_files` VALUES (1,1,'20231213115625_output_video.mp4','2023-12-13 02:56:25'),(2,1,'20231213115625_circle.png','2023-12-13 02:56:25'),(3,1,'20231213115625_stick.png','2023-12-13 02:56:25'),(4,1,'20231213115808_output_video.mp4','2023-12-13 02:58:08'),(5,1,'20231213115808_circle.png','2023-12-13 02:58:08'),(6,1,'20231213115808_stick.png','2023-12-13 02:58:08'),(7,1,'20231213120222_output_video.mp4','2023-12-13 03:02:22'),(8,1,'20231213120222_circle.png','2023-12-13 03:02:22'),(9,1,'20231213120222_stick.png','2023-12-13 03:02:22'),(10,1,'20231215100640_output_video.mp4','2023-12-15 01:06:40'),(11,1,'20231215100640_circle.png','2023-12-15 01:06:40'),(12,1,'20231215100640_stick.png','2023-12-15 01:06:40'),(13,1,'20231215105728_output_video.mp4','2023-12-15 01:57:28'),(14,1,'20231215105728_circle.png','2023-12-15 01:57:29'),(15,1,'20231215105728_stick.png','2023-12-15 01:57:29'),(16,10,'20231215110341_output_video.mp4','2023-12-15 02:03:41'),(17,10,'20231215110341_circle.png','2023-12-15 02:03:41'),(18,10,'20231215110341_stick.png','2023-12-15 02:03:41'),(19,10,'20231217125310_output_video.mp4','2023-12-17 03:53:10'),(20,10,'20231217125310_circle.png','2023-12-17 03:53:10'),(21,10,'20231217125310_stick.png','2023-12-17 03:53:10'),(22,10,'20231217133807_output_video.mp4','2023-12-17 04:38:07'),(23,10,'20231217133807_circle.png','2023-12-17 04:38:07'),(24,10,'20231217133807_stick.png','2023-12-17 04:38:07');
/*!40000 ALTER TABLE `uploaded_files` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-17 14:15:42
