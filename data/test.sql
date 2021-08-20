CREATE TABLE `stu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id||uuid',
  `name` varchar(20) NOT NULL COMMENT '学生名字||name',
  `school` varchar(20) NOT NULL COMMENT '学校名字||eq("二小学校")',
  `nickname` varchar(20) NOT NULL COMMENT '学生小名||hans2pinyin("{{ stu.name }}")',
  `age` int(11) NOT NULL COMMENT '学生年龄||randint([6,12])',
  `class_num` int(11) NOT NULL COMMENT '班级人数||randint([30,50])',
  `score` decimal(4,2) NOT NULL COMMENT '成绩||randint([30,100])',
  `phone` int(20) NOT NULL COMMENT '电话号码||phone_number',
  `email` varchar(64) DEFAULT NULL COMMENT '家庭网络邮箱||email',
  `ip` varchar(32) DEFAULT NULL COMMENT 'IP地址||ipv4',
  `address` text COMMENT '家庭地址||address',
  `create_time`  timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `course` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id{{ uuid }}',
  `name` varchar(20) NOT NULL COMMENT '课程名称{{ choice(["语文","数学","英语","化学","生物","地理"]) }}',
  `grade` varchar(20) NOT NULL COMMENT '年级||choice(["一年级","二年级","三年级","四年级","五年级","六年级"])',
  `teacher` varchar(20) NOT NULL COMMENT '授课老师||name',
  `create_time`  timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `choice_course` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id||uuid',
  `stu_id` varchar(20) NOT NULL COMMENT '学生ID||eq("{{ stu.id }}")',
  `course_id` varchar(20) NOT NULL COMMENT '课程ID||eq("{{ course.id }}")',
  `time` varchar(20) NOT NULL COMMENT '上课时间||choice(["星期一","星期二","星期三","星期四","星期五"])',
  `create_time`  timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;