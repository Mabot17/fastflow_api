-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.0 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for fastflow
DROP DATABASE IF EXISTS `fastflow`;
CREATE DATABASE IF NOT EXISTS `fastflow` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fastflow`;

-- Dumping structure for table fastflow.produk
DROP TABLE IF EXISTS `produk`;
CREATE TABLE IF NOT EXISTS `produk` (
  `produk_id` int NOT NULL AUTO_INCREMENT,
  `produk_kode` varchar(20) NOT NULL,
  `produk_sku` varchar(100) DEFAULT NULL COMMENT 'hanya utk informasi sku satuan terkecil',
  `produk_group` int DEFAULT NULL COMMENT 'grup 1 / kategori',
  `produk_nama` varchar(250) NOT NULL,
  `produk_satuan` int DEFAULT NULL COMMENT 'satuan terkecil',
  `produk_harga` double NOT NULL DEFAULT '0' COMMENT 'harga satuan default',
  `produk_foto_path` varchar(1000) DEFAULT NULL,
  `produk_keterangan` varchar(500) DEFAULT NULL,
  `produk_aktif` enum('Aktif','Tidak Aktif') DEFAULT 'Aktif',
  `created_by` varchar(50) DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `revised` int DEFAULT '0',
  PRIMARY KEY (`produk_id`),
  KEY `ref_produk_group_on_group_id` (`produk_group`)
) ENGINE=InnoDB AUTO_INCREMENT=7209 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- Data exporting was unselected.

-- Dumping structure for table fastflow.produk_group
DROP TABLE IF EXISTS `produk_group`;
CREATE TABLE IF NOT EXISTS `produk_group` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_kode` varchar(5) DEFAULT NULL,
  `group_nama` varchar(250) DEFAULT NULL,
  `group_foto_path` varchar(1000) DEFAULT NULL,
  `group_keterangan` varchar(250) DEFAULT NULL,
  `group_aktif` enum('Aktif','Tidak Aktif') DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `revised` int DEFAULT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- Data exporting was unselected.

-- Dumping structure for table fastflow.satuan
DROP TABLE IF EXISTS `satuan`;
CREATE TABLE IF NOT EXISTS `satuan` (
  `satuan_id` int NOT NULL AUTO_INCREMENT,
  `satuan_kode` varchar(50) NOT NULL,
  `satuan_nama` varchar(250) NOT NULL,
  `satuan_keterangan` varchar(250) DEFAULT NULL,
  `satuan_aktif` enum('Aktif','Tidak Aktif') DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `revised` int DEFAULT NULL,
  PRIMARY KEY (`satuan_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- Data exporting was unselected.

-- Dumping structure for table fastflow.usergroups
DROP TABLE IF EXISTS `usergroups`;
CREATE TABLE IF NOT EXISTS `usergroups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL,
  `group_desc` varchar(250) DEFAULT NULL,
  `group_active` enum('Aktif','Tidak Aktif') CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` varchar(50) DEFAULT '',
  `updated_at` datetime DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT '',
  `deleted_at` datetime DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT '',
  `revised` tinyint DEFAULT '0',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- Data exporting was unselected.

-- Dumping structure for table fastflow.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_kode` varchar(2) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `user_name` varchar(50) NOT NULL DEFAULT '-',
  `user_password` varchar(250) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `user_group_id` int DEFAULT NULL,
  `user_aktif` enum('Aktif','Tidak Aktif') NOT NULL DEFAULT 'Aktif',
  `user_keterangan` varchar(250) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT 'Aktif',
  `user_otp_code` varchar(6) DEFAULT NULL COMMENT 'OTP Digunakan ketika \r\n- reset password (untuk saat ini 01-08-2023)',
  `created_at` datetime DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT NULL,
  `revised` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_kode` (`user_kode`),
  KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
