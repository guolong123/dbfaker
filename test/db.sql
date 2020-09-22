CREATE TABLE `stu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(20) NOT NULL COMMENT '学生名字',
  `school` varchar(20) NOT NULL COMMENT '学校名字',
  `nickname` varchar(20) NOT NULL COMMENT '学生小名',
  `age` int(11) NOT NULL COMMENT '学生年龄',
  `class_num` int(11) NOT NULL COMMENT '班级人数',
  `score` decimal(4,2) NOT NULL COMMENT '成绩',
  `phone` int(20) NOT NULL COMMENT '电话号码',
  `email` varchar(64) DEFAULT NULL COMMENT '家庭网络邮箱',
  `ip` varchar(32) DEFAULT NULL COMMENT 'IP地址',
  `address` text COMMENT '家庭地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;