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

 Date: 26/12/2024 21:28:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for wlgj_print_tgzm
-- ----------------------------
DROP TABLE IF EXISTS `wlgj_print_tgzm`;
CREATE TABLE `wlgj_print_tgzm`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iron_water` int(11) NULL DEFAULT NULL COMMENT '铁水温度',
  `steel_plate` int(11) NULL DEFAULT NULL COMMENT '钢板厚度',
  `roller` int(11) NULL DEFAULT NULL COMMENT '轧辊间距',
  `mold` int(11) NULL DEFAULT NULL COMMENT '模具温度单位为K',
  `conveyor_belt1` int(11) NULL DEFAULT NULL COMMENT '传送带1速度单位为cm/s',
  `conveyor_belt2` int(11) NULL DEFAULT NULL COMMENT '传送带2速度单位为cm/s',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of wlgj_print_tgzm
-- ----------------------------
INSERT INTO `wlgj_print_tgzm` VALUES (1, 3000, 50, 30, 300, 0, 65536);
INSERT INTO `wlgj_print_tgzm` VALUES (2, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (3, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (4, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (5, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (6, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (7, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (8, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (9, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (10, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (11, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (12, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (13, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (14, 23, 45, 23, 12, 234, 23);
INSERT INTO `wlgj_print_tgzm` VALUES (15, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (16, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (17, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (18, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (19, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (20, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (21, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (22, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (23, 3000, 50, 30, 300, 0, 65336);
INSERT INTO `wlgj_print_tgzm` VALUES (24, 3000, 50, 30, 300, 0, 65336);

SET FOREIGN_KEY_CHECKS = 1;
