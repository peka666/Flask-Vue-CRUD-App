-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 31, 2026 at 11:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `komentar`
--

CREATE TABLE `komentar` (
  `ID` int(11) NOT NULL,
  `Naslov` varchar(30) NOT NULL,
  `Tekst` varchar(200) NOT NULL,
  `Proizvod_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `komentar`
--

INSERT INTO `komentar` (`ID`, `Naslov`, `Tekst`, `Proizvod_ID`) VALUES
(1, 'Zadovoljan', 'Giros je odlican', 1),
(3, 'Preslano', 'Burger je preslan', 2),
(4, 'aaaaaaaaaa', 'aaaaaaaaaa', 1),
(5, 'aaaaaaaa', 'aaaaaaaaa', 1);

-- --------------------------------------------------------

--
-- Table structure for table `korisnik`
--

CREATE TABLE `korisnik` (
  `ID` int(11) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `GodinaRodjenja` int(11) NOT NULL,
  `ProfilnaSlika` varchar(50) DEFAULT NULL,
  `TrenutnoStanjeNovca` float NOT NULL,
  `VrstaKorisnika_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `korisnik`
--

INSERT INTO `korisnik` (`ID`, `Username`, `Password`, `Email`, `GodinaRodjenja`, `ProfilnaSlika`, `TrenutnoStanjeNovca`, `VrstaKorisnika_ID`) VALUES
(1, 'MarkoNikolic', 'zekapeka1', 'markonikolic1122@gmail.com', 2004, 'pictures/slika1.avif', 0, 3),
(2, 'PeraPeric', 'zekapeka2', 'peraperic@gmail.com', 2001, 'pictures/slika2.avif', -8500, 1),
(3, 'Prodavac1', 'prodaja2026', 'prodavac222@gmail.com', 1992, 'pictures/slika3.avif', 2400, 2),
(4, 'Prodavac2', 'prodaja2026', 'prodavac333@gmail.com', 2002, 'pictures/slika2.avif', 7300, 2);

-- --------------------------------------------------------

--
-- Table structure for table `kupovina`
--

CREATE TABLE `kupovina` (
  `ID` int(11) NOT NULL,
  `DatumKupovine` date NOT NULL,
  `UkupnaCena` float NOT NULL,
  `Korisnik_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `kupovina`
--

INSERT INTO `kupovina` (`ID`, `DatumKupovine`, `UkupnaCena`, `Korisnik_ID`) VALUES
(1, '2026-01-31', 500, 2),
(2, '2026-01-31', 1500, 2),
(3, '2026-01-31', 2400, 2),
(4, '2026-01-31', 1300, 2),
(5, '2026-01-31', 500, 2),
(6, '2026-01-31', 500, 2),
(7, '2026-01-31', 500, 2);

-- --------------------------------------------------------

--
-- Table structure for table `proizvod`
--

CREATE TABLE `proizvod` (
  `ID` int(11) NOT NULL,
  `Naziv` varchar(30) NOT NULL,
  `Opis` varchar(100) NOT NULL,
  `Cena` float NOT NULL,
  `KolicinaNaStanju` int(11) NOT NULL,
  `Popust` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `proizvod`
--

INSERT INTO `proizvod` (`ID`, `Naziv`, `Opis`, `Cena`, `KolicinaNaStanju`, `Popust`) VALUES
(1, 'Giros', 'giros sa 300g mesa', 500, 25, 0),
(2, 'Burger', 'burger sa govedinom i cedar sirom', 600, 20, 0),
(3, 'Pomfrit', '300g pomfrita', 200, 15, 0),
(5, 'Nudle', 'Nudle u soja sosu', 700, 15, 0);

-- --------------------------------------------------------

--
-- Table structure for table `proizvod_has_korisnik`
--

CREATE TABLE `proizvod_has_korisnik` (
  `Proizvod_ID` int(11) NOT NULL,
  `Korisnik_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `proizvod_has_korisnik`
--

INSERT INTO `proizvod_has_korisnik` (`Proizvod_ID`, `Korisnik_ID`) VALUES
(1, 4),
(2, 3),
(3, 4),
(5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `proizvod_u_korpi`
--

CREATE TABLE `proizvod_u_korpi` (
  `Proizvod_ID` int(11) NOT NULL,
  `Kolicina` int(11) NOT NULL,
  `UkupnaCena` float NOT NULL,
  `Korisnik_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vrstakorisnika`
--

CREATE TABLE `vrstakorisnika` (
  `ID` int(11) NOT NULL,
  `Naziv` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `vrstakorisnika`
--

INSERT INTO `vrstakorisnika` (`ID`, `Naziv`) VALUES
(1, 'kupac'),
(2, 'prodavac'),
(3, 'administrator');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `komentar`
--
ALTER TABLE `komentar`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `fk_Komentar_Proizvod1_idx` (`Proizvod_ID`);

--
-- Indexes for table `korisnik`
--
ALTER TABLE `korisnik`
  ADD PRIMARY KEY (`ID`,`VrstaKorisnika_ID`),
  ADD KEY `fk_Korisnik_VrstaKorisnika_idx` (`VrstaKorisnika_ID`);

--
-- Indexes for table `kupovina`
--
ALTER TABLE `kupovina`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `fk_Kupovina_Korisnik1_idx` (`Korisnik_ID`);

--
-- Indexes for table `proizvod`
--
ALTER TABLE `proizvod`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `proizvod_has_korisnik`
--
ALTER TABLE `proizvod_has_korisnik`
  ADD PRIMARY KEY (`Proizvod_ID`,`Korisnik_ID`),
  ADD KEY `fk_Proizvod_has_Korisnik_Korisnik1_idx` (`Korisnik_ID`),
  ADD KEY `fk_Proizvod_has_Korisnik_Proizvod1_idx` (`Proizvod_ID`);

--
-- Indexes for table `proizvod_u_korpi`
--
ALTER TABLE `proizvod_u_korpi`
  ADD PRIMARY KEY (`Proizvod_ID`),
  ADD KEY `fk_Korpa_has_Proizvod_Proizvod1_idx` (`Proizvod_ID`),
  ADD KEY `fk_Proizvod_U_Korpi_Korisnik1_idx` (`Korisnik_ID`);

--
-- Indexes for table `vrstakorisnika`
--
ALTER TABLE `vrstakorisnika`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `komentar`
--
ALTER TABLE `komentar`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `korisnik`
--
ALTER TABLE `korisnik`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `kupovina`
--
ALTER TABLE `kupovina`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `proizvod`
--
ALTER TABLE `proizvod`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vrstakorisnika`
--
ALTER TABLE `vrstakorisnika`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `komentar`
--
ALTER TABLE `komentar`
  ADD CONSTRAINT `fk_Komentar_Proizvod1` FOREIGN KEY (`Proizvod_ID`) REFERENCES `proizvod` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `korisnik`
--
ALTER TABLE `korisnik`
  ADD CONSTRAINT `fk_Korisnik_VrstaKorisnika` FOREIGN KEY (`VrstaKorisnika_ID`) REFERENCES `vrstakorisnika` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `kupovina`
--
ALTER TABLE `kupovina`
  ADD CONSTRAINT `fk_Kupovina_Korisnik1` FOREIGN KEY (`Korisnik_ID`) REFERENCES `korisnik` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proizvod_has_korisnik`
--
ALTER TABLE `proizvod_has_korisnik`
  ADD CONSTRAINT `fk_Proizvod_has_Korisnik_Korisnik1` FOREIGN KEY (`Korisnik_ID`) REFERENCES `korisnik` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Proizvod_has_Korisnik_Proizvod1` FOREIGN KEY (`Proizvod_ID`) REFERENCES `proizvod` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proizvod_u_korpi`
--
ALTER TABLE `proizvod_u_korpi`
  ADD CONSTRAINT `fk_Korpa_has_Proizvod_Proizvod1` FOREIGN KEY (`Proizvod_ID`) REFERENCES `proizvod` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Proizvod_U_Korpi_Korisnik1` FOREIGN KEY (`Korisnik_ID`) REFERENCES `korisnik` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
