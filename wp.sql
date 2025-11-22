-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2025-06-05 16:08:53
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
-- データベース: `wp`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `授業`
--

CREATE TABLE `授業` (
  `授業id` int(10) NOT NULL,
  `授業名` varchar(20) NOT NULL,
  `教員` varchar(10) NOT NULL,
  `曜日` varchar(1) NOT NULL,
  `時間` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `授業`
--

INSERT INTO `授業` (`授業id`, `授業名`, `教員`, `曜日`, `時間`) VALUES
(1, 'プロジェクト演習B', '櫻井・池辺', '火', 3),
(2, 'オフィスソフトウェア入門', '池辺', '火', 4),
(3, 'サブカルチャー論', '五島', '水', 3),
(4, 'ゲーム企画論', '利波', '水', 4),
(5, '化学(湘南)', '宮本', '水', 5),
(6, 'システム開発技法', '佐藤(孝)', '木', 3),
(7, 'Webプログラミング', '池辺', '木', 4),
(8, '生活と広告(湘南)', '浅川', '木', 5),
(9, 'デザイン論', '藤掛', '金', 3),
(10, '情報英語I(ｵﾝﾃﾞﾏﾝﾄﾞ)', '岐部', 'オ', 0),
(11, '作曲法', '近藤', 'オ', 0),
(12, 'Webデザイン', '門屋', 'オ', 0),
(13, 'サウンドデザイン', '近藤', 'オ', 0);

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `授業`
--
ALTER TABLE `授業`
  ADD PRIMARY KEY (`授業id`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `授業`
--
ALTER TABLE `授業`
  MODIFY `授業id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
