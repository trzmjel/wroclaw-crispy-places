-- Adminer 4.8.1 MySQL 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `aplikacja_turystyczna`;
CREATE DATABASE `aplikacja_turystyczna` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `aplikacja_turystyczna`;

DROP TABLE IF EXISTS `achievements`;
CREATE TABLE `achievements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_points` int(11) NOT NULL COMMENT 'Określa ilość punktów za każdą odwiedzoną lokalizację przez użytkownika',
  `description` text NOT NULL COMMENT 'Opis za co zostały przyznane punkty',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `achievements` (`id`, `user_points`, `description`) VALUES
(1,	5,	'NASTĘPNY PRZYSTANEK... (KOLEJKOWO)'),
(2,	10,	'AZJA WZYWA! (OGRÓD JAPOŃSKI)'),
(3,	15,	'WODNE ATRAKCJE! (FONTANNY BLISKO HALI STULECIA)'),
(4,	20,	'POŚRÓD DZIKICH ZWIĘRZĄT! (WROCŁAWSKIE ZOO)'),
(5,	25,	'JAK TO ZOSTAŁO NAMALOWANE? (PANORAMA RACŁAWICKA)'),
(6,	30,	'SPOTKANIE Z HISTORIĄ! (MUZEUM NARODOWE)'),
(7,	35,	'PODNIEBNA PRZEPRAWA! (POLINKA PWR)'),
(8,	40,	'W GŁĘBINACH OCEANU! (HYDROPOLIS)'),
(9,	45,	'NIEZŁE WIDOKI! (SKY TOWER)'),
(10,	50,	'JEDEN BY RZĄDZIĆ NIMI WSZYSTKIMI! (PAPA KRASNAL RYNEK)');

DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `poi`;
CREATE TABLE `poi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(60) NOT NULL,
  `description` text NOT NULL,
  `latitude` decimal(7,5) NOT NULL,
  `longitude` decimal(7,5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `poi` (`id`, `name`, `address`, `description`, `latitude`, `longitude`) VALUES
(1,	'Panorama Racławicka',	'Jana Ewangelisty Purkyniego 11, 50-155',	'Muzeum sztuki we Wrocławiu, oddział Muzeum Narodowego we Wrocławiu, założone w 1893 we Lwowie, od 1980 we Wrocławiu; eksponuje cykloramiczny obraz \"Bitwa pod Racławicami\" namalowany w latach 1893–1894 przez zespół malarzy pod kierunkiem Jana Styki i Wojciecha Kossaka. Obraz olejny przedstawia bitwę pod Racławicami (1794), jeden z epizodów insurekcji kościuszkowskiej, zwycięstwo wojsk polskich pod dowództwem gen. Tadeusza Kościuszki nad wojskami rosyjskimi',	51.11019,	17.04443),
(2,	'ZOO Wrocław',	'Zygmunta Wróblewskiego 1-5, 51-618',	'Ogród zoologiczny otwarty po raz pierwszy 10 lipca 1865. Jest najstarszym na obecnych ziemiach polskich ogrodem zoologicznym w Polsce. Powierzchnia ogrodu to 33 hektary. Pod koniec 2015 Ogród Zoologiczny we Wrocławiu prezentował ponad 10 500 zwierząt (nie wliczając bezkręgowców) z 1132 gatunków (trzecie pod tym względem zoo na świecie). Jest piątym najchętniej odwiedzanym ogrodem zoologicznym w Europie z dziennym rekordem wejść wynoszącym 28 300 osób',	51.10579,	17.07621),
(3,	'Ogród Japoński',	'Adama Mickiewicza 1, 51-618',	'Założony w latach 1909–1913 wokół dawnego stawu Ludwiga Theodora Moritza-Eichborna w obrębie obecnego Parku Szczytnickiego. W 1995 r. opracowano projekt renowacji ogrodu pod kierunkiem prof. Ikui Nishikawy z Tokio. Następnie w latach 1996–1997, przy współpracy ambasady Japonii oraz ogrodników z Wrocławia i Nagoi, przeprowadzono prace przywracające ogrodowi japoński charakter. Pracami kierował Yoshiki Takamura. Dwa miesiące po uroczystym otwarciu, w lipcu 1997 podczas powodzi stulecia, ogród znajdował się przez trzy tygodnie pod wodą. Zniszczenia były tak duże, że konieczna stała się kolejna renowacja. Przepadło około 70% nowo nasadzonych roślin. Ponowne otwarcie nastąpiło w październiku 1999 r.',	51.10971,	17.07894),
(4,	'Muzeum Narodowe',	'Plac Powstańców Warszawy 5, 50-153',	'Jedno z głównych muzeów Wrocławia i Dolnego Śląska. Zbiory muzeum obejmują przede wszystkim malarstwo i rzeźbę, ze szczególnym uwzględnieniem sztuki całego Śląska. Składa się z gmachu głównego i trzech oddziałów.',	51.11101,	17.04766),
(5,	'Hydropolis',	'Na Grobli 17, 50-421',	'Centrum wiedzy o wodzie. Ośrodek łączy walory edukacyjne z nowoczesną formą wystawienniczą. Jest to jedyny obiekt tego typu w Polsce i jeden z nielicznych na świecie. Wystawa znajduje się w zabytkowym, XIX-wiecznym neogotyckim podziemnym zbiorniku wody czystej o powierzchni 4600 m². Od 2002 roku obiekt znajduje się na liście zabytków. Zbiornik pełnił swą pierwotną funkcję do 2011 roku, gdy został wyłączony z użytku. W grudniu 2015 roku wrocławskie Miejskie Przedsiębiorstwo Wodociągów i Kanalizacji S.A. po przeprowadzeniu niezbędnych remontów i rewitalizacji przekształciło budowlę w Centrum Edukacji Ekologicznej Hydropolis.',	51.10439,	17.05664),
(6,	'Fontanna Multimedialna przy Ha',	'Wystawowa 1, 51-618',	'Otoczona pergolą, znajdująca się niedaleko Hali Stulecia. Jest największą fontanną w Polsce i jedną z największych w Europie. Fontanna została utworzona przy okazji remontu pergoli w roku 2009 r. Składa się z 182 dysz dynamicznych, 88 dysz, które spieniają wodę, a także trzech dysz ogniowych. W wodzie zatopiono 328 lamp podświetlających wodę. W centrum stawu umieszczono gejzer, który wyrzuca wodę na wysokość 40 metrów, czyli o 2m mniej niż wysokość Hali Stulecia. Koszt budowy fontanny wyniósł 10 milionów złotych. Pokazy odbywają się od kwietnia do października w dzień oraz wieczorem – ostatni kończy się o 22:00. Uroczyste zamknięcie sezonu odbywa się pod koniec października, kiedy to pokazom towarzyszą wybrane dzieła muzyki klasycznej i rockowej.',	51.10891,	17.07891),
(7,	'Kolejkowo',	'Powstańców Śląskich 95, 53-332',	'Największe w Polsce makiety kolejowe, oparte o ruch miniaturowego taboru kolejowego, tramwajowego, pojazdów kołowych, statków wodnych i powietrznych. W Na makietach przedstawione zostały zarówno obszary i sceny fikcyjne jak i autentyczne wydarzenia i budowle z terenu Dolnego Śląska. Makiety urozmaica obecność miniaturowych mieszkańców (m.in. kolejarzy, podróżnych, leśniczych, narciarzy, kupców, pracowników budowlanych, cyrkowców i plażowiczów) w różnych sytuacjach dnia codziennego; przedstawione jest życie na wsi, wyprawy wysokogórskie, akcje ratunkowe.',	51.09472,	17.01960),
(8,	'Polinka PWR (Północ)',	'Wybrzeże Stanisława Wyspiańskiego 23, 50-370',	'Całoroczna kolej gondolowa we Wrocławiu, kursująca nad Odrą pomiędzy głównym kampusem Politechniki Wrocławskiej na Wybrzeżu Stanisława Wyspiańskiego, a Geocentrum przy ul. Na Grobli. Kolej wybudował Doppelmayr Garaventa Group, a jej operatorem jest Politechnika Wrocławska. Linia ma długość 373 metry, czas jazdy wynosi 1,95 minuty, maksymalna prędkość jazdy to 5 m/s. Każda gondola zabiera maksymalnie 15 osób. Przepustowość maksymalna wynosi 366 osób na godzinę. Kolej została oddana do użytku 1 października 2013. Od 1 lutego 2014 przejazd koleją jest bezpłatny wyłącznie dla pracowników i studentów Politechniki Wrocławskiej.',	51.10745,	17.05851),
(9,	'Sky Tower',	'Powstańców Śląskich 95, 53-332',	'Neomodernistyczny wieżowiec we Wrocławiu, stanowiący wraz z dwoma sąsiadującymi budynkami kompleks mieszkalny, biurowy, handlowo-usługowy i rekreacyjny. Pierwotnie planowano, że najwyższa jego wieża będzie miała 258 m wysokości. Pod koniec kwietnia 2010 roku wydano ponownie pozwolenie na budowę. Budowę konstrukcji żelbetowej zakończono we wrześniu 2011, a jej ostateczna wysokość wyniosła 205,82 m. Całkowita wysokość budynku wynosi 212 m. Sky Tower zajmuje 4-te miejsce w rankingu najwyższych budynków w Polsce.',	51.09472,	17.01895),
(10,	'Papa Krasnal (Rynek)',	'Świdnicka, 50-067',	'Pomnik z brązu odsłonięty we Wrocławiu w 2001 dla upamiętnienia ruchu Pomarańczowej Alternatywy, działającego w tym mieście w okresie stanu wojennego. Autorem pomnika jest Olaf Brzeski. Pomnik przedstawia 40-centymetrowego krasnala na 80-centymetrowym półkolistym cokole w kształcie czubka ludzkiego palca. Mieści się na deptaku ulicy Świdnickiej, przy zegarze, obok przejścia podziemnego pod ulicą Kazimierza Wielkiego.',	51.10769,	17.03257);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(10) NOT NULL,
  `login` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user` (`id`, `nickname`, `login`, `password`) VALUES
(1,	'test',	'test',	'test');

DROP TABLE IF EXISTS `user_achievements`;
CREATE TABLE `user_achievements` (
  `user_id` int(11) NOT NULL,
  `achievements_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `achievements_id` (`achievements_id`),
  CONSTRAINT `achievements_user-achievements` FOREIGN KEY (`achievements_id`) REFERENCES `achievements` (`id`),
  CONSTRAINT `user_achievements_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_comments_poi`;
CREATE TABLE `user_comments_poi` (
  `user_id` int(11) NOT NULL,
  `poi_id` int(11) NOT NULL,
  `comments_id` int(11) NOT NULL,
  KEY `user_id` (`user_id`),
  KEY `poi_id` (`poi_id`),
  KEY `comments_id` (`comments_id`),
  CONSTRAINT `user_comments_poi_ibfk_1` FOREIGN KEY (`comments_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `user_comments_poi_ibfk_3` FOREIGN KEY (`poi_id`) REFERENCES `poi` (`id`),
  CONSTRAINT `user_comments_poi_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user_poi` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_poi`;
CREATE TABLE `user_poi` (
  `poi_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `poi_id` (`poi_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `poi_user-poi` FOREIGN KEY (`poi_id`) REFERENCES `poi` (`id`),
  CONSTRAINT `user_user-poi` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `user_poi` (`poi_id`, `user_id`) VALUES
(2,	1);

-- 2024-05-20 13:11:58
