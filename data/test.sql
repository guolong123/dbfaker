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


CREATE TABLE `course` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(20) NOT NULL COMMENT '课程名称',
  `grade` varchar(20) NOT NULL COMMENT '年级',
  `teacher` varchar(20) NOT NULL COMMENT '授课老师',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `choice_course` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `stu_id` varchar(20) NOT NULL COMMENT '学生ID',
  `course_id` varchar(20) NOT NULL COMMENT '课程ID',
  `time` varchar(20) NOT NULL COMMENT '上课时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;