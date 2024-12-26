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

 Date: 26/12/2024 21:28:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for wlgj_read_tgzm
-- ----------------------------
DROP TABLE IF EXISTS `wlgj_read_tgzm`;
CREATE TABLE `wlgj_read_tgzm`  (
  `id` int(11) NOT NULL,
  `iron_water` int(11) NULL DEFAULT NULL,
  `steel_plate` int(11) NULL DEFAULT NULL,
  `roller` int(11) NULL DEFAULT NULL,
  `mold` int(11) NULL DEFAULT NULL,
  `conveyor_belt1` int(11) NULL DEFAULT NULL,
  `conveyor_belt2` int(11) NULL DEFAULT NULL,
  `loag` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of wlgj_read_tgzm
-- ----------------------------
INSERT INTO `wlgj_read_tgzm` VALUES (1, 12, 12, 123, 123, 123, 124, 1);

SET FOREIGN_KEY_CHECKS = 1;
