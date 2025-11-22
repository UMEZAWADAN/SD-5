-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2025-11-03 15:37:44
-- サーバのバージョン： 10.4.32-MariaDB
-- PHP のバージョン: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `care_system`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `staff_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `client`
--

CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `writer_name` varchar(100) NOT NULL,
  `consultation_date` date NOT NULL,
  `current_status` text NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `birth_date` date NOT NULL,
  `address` text NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  `disability_adl_level` varchar(50) NOT NULL,
  `dementia_adl_level` varchar(50) NOT NULL,
  `certification_info` text NOT NULL,
  `disability_certification` varchar(100) NOT NULL,
  `living_environment` text NOT NULL,
  `economic_status` text NOT NULL,
  `visitor_name` varchar(100) NOT NULL,
  `visitor_contact` text NOT NULL,
  `relation_to_client` varchar(50) NOT NULL,
  `family_composition` text NOT NULL,
  `emergency_contact_name` varchar(100) NOT NULL,
  `emergency_relation` varchar(50) NOT NULL,
  `emergency_contact_info` text NOT NULL,
  `life_history` text NOT NULL,
  `daily_life_pattern` text NOT NULL,
  `time_of_day` varchar(100) NOT NULL,
  `person_content` text NOT NULL,
  `caregiver_content` text NOT NULL,
  `hobbies` text NOT NULL,
  `social_connections` text NOT NULL,
  `disease_onset_date` date DEFAULT NULL,
  `disease_name` varchar(200) DEFAULT NULL,
  `medical_institution` text DEFAULT NULL,
  `medical_history` text DEFAULT NULL,
  `current_condition` text DEFAULT NULL,
  `public_services` text DEFAULT NULL,
  `private_services` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `dasc21`
--

CREATE TABLE `dasc21` (
  `dasc_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `informant_name` varchar(100) NOT NULL,
  `evaluator_name` varchar(100) NOT NULL,
  `assessment_item` text NOT NULL,
  `remarks` text DEFAULT NULL,
  `total_score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `dbd13`
--

CREATE TABLE `dbd13` (
  `dbd_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `respondent_name` varchar(100) NOT NULL,
  `evaluator_name` varchar(100) NOT NULL,
  `entry_date` date NOT NULL,
  `assessment_item` text NOT NULL,
  `remarks` text DEFAULT NULL,
  `subtotal_score` int(11) NOT NULL,
  `total_score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `physical_status`
--

CREATE TABLE `physical_status` (
  `physical_status_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `check_item` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `shared_folder`
--

CREATE TABLE `shared_folder` (
  `folder_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `file_path` text NOT NULL,
  `uploaded_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `support_plan`
--

CREATE TABLE `support_plan` (
  `support_plan_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `visit_record_id` int(11) DEFAULT NULL,
  `keyword` varchar(200) NOT NULL,
  `support_decision` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `visit_record`
--

CREATE TABLE `visit_record` (
  `visit_record_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `physical_status_id` int(11) DEFAULT NULL,
  `visit_datetime` datetime NOT NULL,
  `visitor_name` varchar(100) NOT NULL,
  `visit_purpose` text NOT NULL,
  `visit_condition` text NOT NULL,
  `support_decision` text NOT NULL,
  `future_plan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- テーブルのインデックス `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`client_id`);

--
-- テーブルのインデックス `dasc21`
--
ALTER TABLE `dasc21`
  ADD PRIMARY KEY (`dasc_id`),
  ADD KEY `idx_dasc_client` (`client_id`);

--
-- テーブルのインデックス `dbd13`
--
ALTER TABLE `dbd13`
  ADD PRIMARY KEY (`dbd_id`),
  ADD KEY `idx_dbd_client` (`client_id`);

--
-- テーブルのインデックス `physical_status`
--
ALTER TABLE `physical_status`
  ADD PRIMARY KEY (`physical_status_id`),
  ADD KEY `idx_physical_client` (`client_id`);

--
-- テーブルのインデックス `shared_folder`
--
ALTER TABLE `shared_folder`
  ADD PRIMARY KEY (`folder_id`),
  ADD KEY `idx_folder_client` (`client_id`);

--
-- テーブルのインデックス `support_plan`
--
ALTER TABLE `support_plan`
  ADD PRIMARY KEY (`support_plan_id`),
  ADD KEY `idx_support_client` (`client_id`),
  ADD KEY `idx_support_visit` (`visit_record_id`);

--
-- テーブルのインデックス `visit_record`
--
ALTER TABLE `visit_record`
  ADD PRIMARY KEY (`visit_record_id`),
  ADD KEY `idx_visit_client` (`client_id`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `client`
--
ALTER TABLE `client`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `dasc21`
--
ALTER TABLE `dasc21`
  MODIFY `dasc_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `dbd13`
--
ALTER TABLE `dbd13`
  MODIFY `dbd_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `physical_status`
--
ALTER TABLE `physical_status`
  MODIFY `physical_status_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `shared_folder`
--
ALTER TABLE `shared_folder`
  MODIFY `folder_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `support_plan`
--
ALTER TABLE `support_plan`
  MODIFY `support_plan_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `visit_record`
--
ALTER TABLE `visit_record`
  MODIFY `visit_record_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `dasc21`
--
ALTER TABLE `dasc21`
  ADD CONSTRAINT `dasc21_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;

--
-- テーブルの制約 `dbd13`
--
ALTER TABLE `dbd13`
  ADD CONSTRAINT `dbd13_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;

--
-- テーブルの制約 `physical_status`
--
ALTER TABLE `physical_status`
  ADD CONSTRAINT `physical_status_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;

--
-- テーブルの制約 `shared_folder`
--
ALTER TABLE `shared_folder`
  ADD CONSTRAINT `shared_folder_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;

--
-- テーブルの制約 `support_plan`
--
ALTER TABLE `support_plan`
  ADD CONSTRAINT `support_plan_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `support_plan_ibfk_2` FOREIGN KEY (`visit_record_id`) REFERENCES `visit_record` (`visit_record_id`) ON DELETE SET NULL;

--
-- テーブルの制約 `visit_record`
--
ALTER TABLE `visit_record`
  ADD CONSTRAINT `visit_record_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
