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

-- 更新数据
UPDATE wlgj_qidong
SET arp = 1
WHERE id = 1;

-- 查看修改后的数据（可选）
SELECT * FROM wlgj_qidong WHERE id = 1;
