/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50643
 Source Host           : localhost:3306
 Source Schema         : renren_fast

 Target Server Type    : MySQL
 Target Server Version : 50643
 File Encoding         : 65001

 Date: 26/12/2024 21:28:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for wlgj_qidong
-- ----------------------------
DROP TABLE IF EXISTS `wlgj_qidong`;
CREATE TABLE `wlgj_qidong`  (
  `id` int(11) NOT NULL,
  `arp` int(11) NULL DEFAULT NULL,
  `dos` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of wlgj_qidong
-- ----------------------------
INSERT INTO `wlgj_qidong` VALUES (1, 0, 1);

SET FOREIGN_KEY_CHECKS = 1;
