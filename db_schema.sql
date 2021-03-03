-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 02, 2021 at 03:24 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `one-portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `account_id` int(11) UNSIGNED NOT NULL,
  `account_sfdc` varchar(255) DEFAULT NULL,
  `account_name` varchar(255) DEFAULT NULL,
  `account_email` varchar(255) NOT NULL DEFAULT '',
  `account_pass` varchar(255) DEFAULT NULL,
  `account_salt` varchar(255) DEFAULT NULL,
  `account_reset` varchar(255) DEFAULT NULL,
  `account_reset_datetime` datetime DEFAULT NULL,
  `account_data` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `account_sfdc`, `account_name`, `account_email`, `account_pass`, `account_salt`, `account_reset`, `account_reset_datetime`, `account_data`) VALUES
(26, '0036D00000Hq11GQAR', 'Chou', 'hdeadmin@365cons004.onmicrosoft.com', '', '', NULL, NULL, '{\"phone\": null}'),
(27, '0036D00000HqVkOQAV', 'General', 'general@hennge.com', '', '', NULL, NULL, '{\"phone\": \"0909314818\"}'),
(28, '0036D000001S2OqQAK', 'Choui', 'ted.chou@hennge.com', '0803bcff5f472cc802e1dc7015e66092', 'ijsev9ex', '', NULL, '{\"phone\": \"+88690941888\", \"lang\": \"en\"}'),
(29, '0036D000001S8MFQA0', 'Kevin', 'kevin@hennge.com', '', '', NULL, NULL, '{\"phone\": null}'),
(30, '0036D000001S8XGQA0', 'Test', 'test@hennge.com', '', '', NULL, NULL, '{\"phone\": null}'),
(31, '0036D00000HbHNzQAN', 'Satya Nadella', 'satya_nadella@microsoft.com', '', '', NULL, NULL, '{\"phone\": null}'),
(32, '0036D00000HbL1OQAV', 'Page', 'larry_page@google.com', '', '', NULL, NULL, '{\"phone\": null}'),
(33, '0036D00000HbziFQAR', 'Yamamoto', 'yohei.yamamoto@hennge.com', '', '', NULL, NULL, '{\"phone\": \"+81 80-3518-3061\"}'),
(34, '0036D00000HbxMOQAZ', 'Jobs', 'steve@apple.com', '', '', NULL, NULL, '{\"phone\": null}'),
(35, '0036D00000Hbzj8QAB', 'Imaizumi', 'imaizumi.takeru@hennge.com', '', '', NULL, NULL, '{\"phone\": \"+81 80-3518-3062\"}'),
(36, '0036D00000HqgSRQAZ', '周', 'ted.chou@g.hde.co.jp', '', '', NULL, NULL, '{\"phone\": null}'),
(37, '0036D00000HqgkOQAR', '謙', 'chouchou@hennge.com', '', '', NULL, NULL, '{\"phone\": null}'),
(38, '0036D00000Ilt8nQAB', 'BBb', 'bbb@gmail.com', '', '', NULL, NULL, '{\"phone\": \"+886123123123\"}');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `contact_id` int(11) NOT NULL,
  `contact_sfdc` varchar(255) NOT NULL,
  `contact_account` int(11) NOT NULL,
  `contact_tenant` varchar(255) NOT NULL,
  `contact_dc` varchar(255) NOT NULL,
  `contact_contact` int(1) NOT NULL DEFAULT '0',
  `contact_renew` int(1) NOT NULL DEFAULT '0',
  `contact_emergency` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `contact`
--
-- --------------------------------------------------------

--
-- Table structure for table `security`
--

CREATE TABLE `security` (
  `security_id` int(11) NOT NULL,
  `security_hash` varchar(255) NOT NULL,
  `security_time` datetime NOT NULL,
  `security_used` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `session` (
  `session_id` int(11) UNSIGNED NOT NULL,
  `session_hash` varchar(255) DEFAULT NULL,
  `session_user` int(11) DEFAULT NULL,
  `session_time` datetime DEFAULT NULL,
  `session_logout` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `security`
--

-- --------------------------------------------------------

--
-- Table structure for table `tenant`
--

CREATE TABLE `tenant` (
  `tenant_id` varchar(255) NOT NULL,
  `tenant_sfdc` varchar(255) NOT NULL,
  `tenant_domain` varchar(255) NOT NULL,
  `tenant_name` varchar(255) NOT NULL,
  `tenant_status` varchar(255) NOT NULL,
  `tenant_domains` text,
  `tenant_licenses` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tenant`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_id`),
  ADD UNIQUE KEY `account_email` (`account_email`),
  ADD UNIQUE KEY `account_sfdc` (`account_sfdc`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`contact_id`),
  ADD UNIQUE KEY `contact_sfdc` (`contact_sfdc`);

--
-- Indexes for table `security`
--
ALTER TABLE `security`
  ADD PRIMARY KEY (`security_id`),
  ADD UNIQUE KEY `security_hash` (`security_hash`);

--
-- Indexes for table `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`session_id`);

--
-- Indexes for table `tenant`
--
ALTER TABLE `tenant`
  ADD PRIMARY KEY (`tenant_id`),
  ADD UNIQUE KEY `tenant_sfdc` (`tenant_sfdc`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `contact_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `security`
--
ALTER TABLE `security`
  MODIFY `security_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=238;

--
-- AUTO_INCREMENT for table `session`
--
ALTER TABLE `session`
  MODIFY `session_id` int(1) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;
