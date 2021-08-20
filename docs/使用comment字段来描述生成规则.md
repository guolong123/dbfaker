# dbfaker使用comment字段来描述生成规则

-------
#### 前言
>有时候如果我们可以在定义数据库字段的时候就考虑到有造数据需求，
那么直接在设计数据库的时候就将字段的生成规则描述在建表语句里面，这是个非常棒的需求。
数据库中可以定义生成规则的字段就只有comment字段，只有这个字段是跟逻辑无关的，所以我们可以将字段生成规则写在comment里面。

#### 规则定义
sql建表语句的写法是在comment本身字段中添加“||”来分割本身的comment和规则字段。
使用时在原有的命令基础上添加`--use_comment`即可，程序会自动分割comment字段，
并将"||"后面的内容作为engine字段来写入到yml文件中

##### sql举例
```sql
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
```
##### 转换命令
```shell script
table2yml table_statement --sql_file ../data/test.sql --use_comment
```

##### 转换结果
```yaml
package: []
env: {}
tables:
- table: stu
  comment: null
  columns:
    id:
      comment: 自增id
      engine: uuid
    name:
      comment: 学生名字
      engine: name
    school:
      comment: 学校名字
      engine: eq("二小学校")
    nickname:
      comment: 学生小名
      engine: hans2pinyin("{{ stu.name }}")
    age:
      comment: 学生年龄
      engine: randint([6,12])
    class_num:
      comment: 班级人数
      engine: randint([30,50])
    score:
      comment: 成绩
      engine: randint([30,100])
    phone:
      comment: 电话号码
      engine: phone_number
    email:
      comment: 家庭网络邮箱
      engine: email
    ip:
      comment: IP地址
      engine: ipv4
    address:
      comment: 家庭地址
      engine: address
    create_time:
      comment: 修改时间
      engine: address
```