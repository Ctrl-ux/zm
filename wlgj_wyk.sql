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

 Date: 26/12/2024 21:27:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for wlgj_wyk
-- ----------------------------
DROP TABLE IF EXISTS `wlgj_wyk`;
CREATE TABLE `wlgj_wyk`  (
  `id` int(11) NOT NULL,
  `temperature` int(11) NULL DEFAULT NULL COMMENT '温度',
  `pressure` int(11) NULL DEFAULT NULL COMMENT '压力',
  `air_quality` int(11) NULL DEFAULT NULL COMMENT '空气质量',
  `loag` int(11) NULL DEFAULT NULL COMMENT '标志',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of wlgj_wyk
-- ----------------------------
INSERT INTO `wlgj_wyk` VALUES (1, 0, 0, 0, 0);

SET FOREIGN_KEY_CHECKS = 1;
