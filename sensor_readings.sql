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

 Date: 26/12/2024 21:28:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sensor_readings
-- ----------------------------
DROP TABLE IF EXISTS `sensor_readings`;
CREATE TABLE `sensor_readings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `temperature` int(11) NULL DEFAULT NULL,
  `pressure` int(11) NULL DEFAULT NULL,
  `air_quality` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of sensor_readings
-- ----------------------------
INSERT INTO `sensor_readings` VALUES (1, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (2, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (3, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (4, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (5, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (6, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (7, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (8, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (9, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (10, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (11, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (12, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (13, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (14, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (15, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (16, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (17, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (18, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (19, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (20, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (21, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (22, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (23, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (24, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (25, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (26, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (27, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (28, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (29, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (30, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (31, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (32, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (33, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (34, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (35, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (36, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (37, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (38, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (39, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (40, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (41, 1978, 20, 10);
INSERT INTO `sensor_readings` VALUES (42, 34, 23, 234);
INSERT INTO `sensor_readings` VALUES (43, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (44, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (45, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (46, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (47, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (48, 1978, 24, 10);
INSERT INTO `sensor_readings` VALUES (49, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (50, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (51, 1978, 0, 10);
INSERT INTO `sensor_readings` VALUES (52, 1978, 0, 10);

SET FOREIGN_KEY_CHECKS = 1;
