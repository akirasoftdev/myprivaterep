-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: fudosan
-- ------------------------------------------------------
-- Server version	5.7.12-log

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

--
-- Table structure for table `railwayroutes`
--

DROP TABLE IF EXISTS `railwayroutes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `railwayroutes` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `railwayroutes`
--

LOCK TABLES `railwayroutes` WRITE;
/*!40000 ALTER TABLE `railwayroutes` DISABLE KEYS */;
INSERT INTO `railwayroutes` VALUES (3,'ＪＲ青梅線'),(6,'ＪＲ中央線'),(7,'京王線'),(8,'西武新宿線'),(9,'京王高尾線'),(10,'東武伊勢崎線'),(11,'つくばエクスプレス'),(12,'東京メトロ有楽町線'),(13,'東武東上線'),(14,'日暮里舎人ライナー'),(15,'都営三田線'),(16,'ＪＲ千代田・常磐緩行線'),(17,'京成本線'),(18,'京成金町線'),(19,'西武池袋線'),(20,'ＪＲ総武線'),(21,'東京メトロ千代田線'),(22,'京成押上線'),(23,'東急池上線'),(24,'東京メトロ日比谷線'),(25,'東急多摩川線'),(26,'東京メトロ丸ノ内線'),(27,'ＪＲ総武本線'),(28,'東急東横線'),(29,'ＪＲ京浜東北線'),(30,'東急大井町線'),(31,'京急本線'),(32,'ＪＲ山手線'),(33,'東武亀戸線'),(34,'京王井の頭線'),(35,'ＪＲ埼京線'),(36,'東京メトロ丸ノ内方南支線'),(37,'都営浅草線'),(38,'小田急小田原線'),(39,'都営大江戸線'),(40,'都営新宿線'),(41,'東急世田谷線'),(42,'西武多摩湖線'),(43,'東急田園都市線'),(44,'ＪＲ高崎線'),(45,'東京メトロ東西線'),(46,'東京メトロ南北線'),(47,'東京メトロ副都心線'),(48,'東急目黒線'),(49,'東京メトロ銀座線'),(50,'東京メトロ半蔵門線'),(51,'ＪＲ京葉線'),(52,'新交通ゆりかもめ'),(53,'ＪＲ南武線'),(54,'西武拝島線'),(55,'京王相模原線'),(56,'ＪＲ横浜線'),(57,'京急空港線'),(58,'ＪＲ横須賀線'),(59,'西武有楽町線'),(60,'多摩モノレール'),(61,'都電荒川線'),(62,'ＪＲ常磐線'),(63,'りんかい線'),(64,'東京モノレール'),(65,'ＪＲ東北本線'),(66,'ＪＲ八高線'),(67,'西武多摩川線'),(68,'ＪＲ武蔵野線'),(69,'湘南新宿ライン宇須'),(70,'小田急多摩線'),(71,'東北新幹線'),(72,'東海道新幹線'),(73,'ＪＲ東海道本線'),(74,'北総線'),(75,'西武国分寺線'),(76,'ＪＲ五日市線'),(77,'小田急江ノ島線'),(78,'ブルーライン'),(79,'相鉄本線'),(80,'京急逗子線'),(81,'ＪＲ根岸線'),(82,'京急大師線'),(83,'湘南新宿ライン高海'),(84,'シーサイドライン'),(85,'グリーンライン'),(86,'ＪＲ鶴見線'),(87,'ＪＲ相模線'),(88,'相鉄いずみ野線'),(89,'横浜高速鉄道みなとみらい線'),(90,'京急久里浜線'),(91,'箱根登山ケーブル線'),(92,'箱根登山鉄道'),(93,'江ノ島電鉄線'),(94,'湘南モノレール'),(95,'伊豆箱根鉄道大雄山線'),(96,'湘南新宿ライン宇須【バス】11分 狩場東 停歩5分'),(97,'東急こどもの国線'),(98,'ＪＲ外房線'),(99,'新京成線'),(100,'ＪＲ内房線'),(101,'東武野田線'),(102,'京成千原線'),(103,'ＪＲ東金線'),(104,'外房線'),(105,'内房線'),(106,'京成千葉線'),(108,'ユーカリが丘線'),(110,'unknown'),(111,'千葉都市モノレール'),(112,'東葉高速鉄道'),(113,'ＪＲ成田線'),(114,'ＪＲ久留里線'),(115,'流鉄流山線'),(116,'成田スカイアクセス'),(117,'ＪＲ川越線'),(118,'埼玉高速鉄道'),(119,'秩父鉄道'),(120,'東武越生線'),(121,'西武狭山線'),(122,'西武山口線'),(123,'東武日光線'),(124,'埼玉新都市交通伊奈線'),(125,'西武秩父線'),(126,'こどもの国線');
/*!40000 ALTER TABLE `railwayroutes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-08  6:28:30
