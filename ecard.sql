-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2018-01-19 22:01:02
-- 服务器版本: 5.5.54-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `ecard`
--

-- --------------------------------------------------------

--
-- 表的结构 `ecard`
--

CREATE TABLE IF NOT EXISTS `ecard` (
  `number` varchar(12) COLLATE utf8_bin NOT NULL,
  `paydate` datetime NOT NULL,
  `paytype` varchar(50) COLLATE utf8_bin NOT NULL,
  `payloc` varchar(50) COLLATE utf8_bin NOT NULL,
  `account` varchar(20) COLLATE utf8_bin NOT NULL,
  `paycount` float NOT NULL,
  `balance` float NOT NULL,
  `payindex` float NOT NULL,
  `status` varchar(10) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`paydate`),
  KEY `number` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
