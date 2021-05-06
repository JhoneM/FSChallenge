-- phpMyAdmin SQL Dump
-- version 4.4.15.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 30, 2017 at 10:34 AM
-- Server version: 5.7.17-0ubuntu0.16.04.1
-- PHP Version: 7.0.13-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rip_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `operations`
--

CREATE TABLE IF NOT EXISTS `operations` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    `type` INT NOT NULL DEFAULT TRUE COMMENT 'in = 1, out = 2, trans = 3',
    `name` varchar(50) UNIQUE NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `coin`
--

CREATE TABLE IF NOT EXISTS `coin` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    `name` varchar(50) NOT NULL,
    `iso_code` varchar(50) UNIQUE NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `coin`
--

CREATE TABLE IF NOT EXISTS `level_user` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    `name` varchar(50) UNIQUE NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    `username` varchar(50) UNIQUE NOT NULL,
    `password` varchar(100) NOT NULL,
    `name` varchar(100) NOT NULL,
    `last_name` varchar(100) NOT NULL,
    `level_id` INT NOT NULL,
    FOREIGN KEY (level_id) REFERENCES level_user (id)

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `accounts`
--

CREATE TABLE IF NOT EXISTS `account` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `coin_id` INT NOT NULL,
    `balance` FLOAT(10,2) NOT NULL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (coin_id) REFERENCES coin (id),
    UNIQUE KEY unique_account (user_id, coin_id)

) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `operation_id` INT NOT NULL,
    `account_id` INT NOT NULL,
    `acc_amount_initial` float(10,2) NOT NULL,
    `acc_amount_final` float(10,2) NOT NULL,
    `acc_dest_id` INT,
    `amount` float(10,2) NOT NULL,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operation_id) REFERENCES operations (id),
    FOREIGN KEY (account_id) REFERENCES account (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Insert Values
--
INSERT INTO operations (name, type) VALUES("Deposito", 1), ("Retiro", 2), ("Transferencia", 3);
INSERT INTO coin (name, iso_code) VALUES("Peso", "ARS"), ("Peso Chileno", "CLP");
INSERT INTO level_user (name) VALUES("admin"), ("usuario");

INSERT INTO user (username, password, name, last_name, level_id) VALUES("admin", "pbkdf2:sha256:150000$EEOzaq6g$2ea92eb990581cf1212821a77967642f98425b20fa005c77ca42ce37dc870416", "admin", "admin", (SELECT MIN(id) FROM level_user) );
INSERT INTO user (username, password, name, last_name, level_id) VALUES("jmendez", "pbkdf2:sha256:150000$evHJ0HnX$5a5b4a74bce2357c18b06a969f6eb0aa4cf0577f84dfe1a56372f5ec11812924", "Jhone", "Mendez", (SELECT MAX(id) FROM level_user) );
INSERT INTO user (username, password, name, last_name, level_id) VALUES("martu", "pbkdf2:sha256:150000$evHJ0HnX$5a5b4a74bce2357c18b06a969f6eb0aa4cf0577f84dfe1a56372f5ec11812924", "Martina", "M", (SELECT MAX(id) FROM level_user) );

INSERT INTO account (user_id, coin_id, balance) VALUES((SELECT id FROM user WHERE username = 'jmendez'), (SELECT id FROM coin WHERE iso_code = "ARS"), 500);
INSERT INTO account (user_id, coin_id, balance) VALUES((SELECT id FROM user WHERE username = 'martu'), (SELECT id FROM coin WHERE iso_code = "ARS"), 1500);
INSERT INTO account (user_id, coin_id, balance) VALUES((SELECT id FROM user WHERE username = 'martu'), (SELECT id FROM coin WHERE iso_code = "CLP"), 20000);
