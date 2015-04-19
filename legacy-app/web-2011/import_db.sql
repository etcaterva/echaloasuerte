-- phpMyAdmin SQL Dump
-- version 4.1.14.8
-- http://www.phpmyadmin.net
--
-- Host: db372506665.db.1and1.com
-- Generation Time: Apr 18, 2015 at 09:01 PM
-- Server version: 5.1.73-log
-- PHP Version: 5.4.39-0+deb7u2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `db372506665`
--

-- --------------------------------------------------------

--
-- Table structure for table `ALEATORIO`
--

CREATE TABLE IF NOT EXISTS `ALEATORIO` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` int(11) DEFAULT NULL,
  `desde` int(11) DEFAULT NULL,
  `hasta` int(11) DEFAULT NULL,
  `repetir` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=1782 ;

--
-- Table structure for table `ASOCIACION`
--

CREATE TABLE IF NOT EXISTS `ASOCIACION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repetir` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=1772 ;

--
-- Table structure for table `ELECCION`
--

CREATE TABLE IF NOT EXISTS `ELECCION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num` int(11) DEFAULT NULL,
  `repetir` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=1775 ;


--
-- Table structure for table `ITEM_SOLUCION`
--

CREATE TABLE IF NOT EXISTS `ITEM_SOLUCION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenido` varchar(255) COLLATE utf8_spanish_ci DEFAULT NULL,
  `tirada` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=5590 ;

--
-- Table structure for table `MENSAJE`
--

CREATE TABLE IF NOT EXISTS `MENSAJE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenido` varchar(255) COLLATE utf8_spanish_ci DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario` int(11) DEFAULT NULL,
  `tirada` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=7501 ;


--
-- Table structure for table `OPCION`
--

CREATE TABLE IF NOT EXISTS `OPCION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenido` varchar(255) COLLATE utf8_spanish_ci DEFAULT NULL,
  `eleccion` int(11) DEFAULT NULL,
  `asociacion_desde` int(11) DEFAULT NULL,
  `asociacion_hasta` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=3325 ;


--
-- Table structure for table `TIRADA`
--

CREATE TABLE IF NOT EXISTS `TIRADA` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(255) COLLATE utf8_spanish_ci DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `participantes` int(11) NOT NULL DEFAULT '0',
  `nombre` varchar(255) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=1782 ;


--
-- Table structure for table `USUARIO`
--

CREATE TABLE IF NOT EXISTS `USUARIO` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_spanish_ci NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `checked` tinyint(1) NOT NULL DEFAULT '0',
  `tirada` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci AUTO_INCREMENT=3612 ;

--
-- Table structure for table `tirada`
--

CREATE TABLE IF NOT EXISTS `tirada` (
  `id` int(11) NOT NULL,
  `pass` varchar(100) COLLATE latin1_german2_ci DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `restantes` int(11) DEFAULT NULL,
  `participantes` text COLLATE latin1_german2_ci,
  `resultado` text COLLATE latin1_german2_ci,
  `tipo` int(11) DEFAULT NULL,
  `repetir` tinyint(1) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `desde` int(11) DEFAULT NULL,
  `hasta` int(11) DEFAULT NULL,
  `val` text COLLATE latin1_german2_ci,
  `valB` text COLLATE latin1_german2_ci,
  `mails` text COLLATE latin1_german2_ci,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_german2_ci;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
