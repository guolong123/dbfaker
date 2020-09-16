# dbfaker

#### 介绍
基于数据库层面批量生成有逻辑关联的数据

#### 软件架构
软件架构说明
对于要造大量数据来讲，有几种方式，一是通过开发写的接口来模拟真实用户场景来产生数据，这种方式在某些方面来讲是比较合适的，比如因为是模拟用户场景，业务数据完整，不会丢．但不好的地方就是要处理的地方太多，接口定义，签名，加密等等，还有扩展性也很不好，一个业务场景要写一套代码．另一种方式，是已知业务产生的数据之间的依赖关系后，直接在数据库中插入相关数据，本项目就是通过这种方式来实现，好处就是生成规则通过配置文件来描述即可（yaml文件），不需要额外添加代码（对于某些字段生成规则有可能需要单独编写方法），与测试库testrunner比较类似．现在已知有些库也支持直接在数据库内造数据，但对库表之间的关联关系的处理都做得不太好．

本项目数据处理流程如下：
![处理流程](https://images.gitee.com/uploads/images/2020/0915/183724_40e0141c_1021400.png "屏幕截图.png")


#### 使用说明

１．　生成meta.yml文件，可通过内置工具table2yml.py来一键生成模板，生成后需完善模板中表字段的定义
    
table2yml.py文件使用说明：
```shell
usage: table2yml.py [-h] [--connect [CONNECT]] [--table_names [TABLE_NAMES]]
                    [--sql_file [SQL_FILE]] [--output [OUTPUT]]
                    [type]

数据库表转数据生成yaml文件格式工具

positional arguments:
  type                  数据来源，table_name： 通过输入表名与数据库链接方式，在数据库中获取数据库建表语句；
                        table_statement: 指定数据库建表语句的sql文件路径

optional arguments:
  -h, --help            show this help message and exit
  --connect [CONNECT]   数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.ho
                        melabs.in/pdms_hospital
  --table_names [TABLE_NAMES]
                        数据库表，多个表以“,”分割
  --sql_file [SQL_FILE]
                        数据库建表语句的sql文件路径
  --output [OUTPUT]     输出文件名，默认为数据库表名+meta.yml

```
2, 编辑meta.yml文件，文件格式如下
```yaml
package:
  - datetime  #　导入额外的包，在jinja2模板中使用（下面有用到datetime包，所以要先导入）
env:
  id:
    engine: faker.uuid
    rule: null
  time_format:
    engine: faker.eq
    rule:
      value: "%Y-%m-%d %H:%M:%S"
tables:
- columns:
  - column: id
    comment: 数据主键id
    engine: faker.eq
    rule:
      value: '{{ env.id }}'  # 通过引用环境变量中的值
  - column: name
    comment: 姓名
    engine: faker.name
    rule: null
  - column: idcard
    comment: 身份证号
    engine: faker.ssn
    rule: null
  - column: age
    comment: 年龄
    engine: faker.eq
    rule:
      value: '{{ datetime.datetime.now().year - int(stu.idcard[6:10]) }}'  #　通过jinja２模板直接计算
  - column: sex
    comment: 性别
    engine: faker.eq
    rule:
      value: '{{ "man" if int(stu.idcard[-2]) % 2==1 else "female" }}'  #　通过jinja２模板直接计算
  comment: ''
  table: stu
- columns:
  - column: id
    comment: 数据主键id
    engine: faker.uuid
    rule: null
  - column: stu_id
    comment: 数据主键id
    engine: faker.eq
    rule:
      value: '{{ stu.id }}'  # 通过其他表中的值
  - column: course_name
    comment: 课程名称
    engine: faker.choice # 通过内置方法从列表中随机取一个值
    rule:
      value: [数学,语文,英语,化学,地理]
  - column: course_time
    comment: 上课时间
    engine: faker.now  # 通过内置方法获取当前时间，并按照指定格式返回
    rule:
      format: "{{ env.time_format }}"
  comment: '课程信息 '
  table: course

```
３，创建ｓｑｌ
```shell
guolong@guolong-PC:~/01 Work/07 MyProject/dbfaker$ source venv/bin/activate
(venv) guolong@guolong-PC:~/01 Work/07 MyProject/dbfaker$ python main.py -h
usage: main.py [-h] [-n [NUMBER]] [-i] [-c [CONNECT]] [-o [OUTPUT]]
               [meta_file]

通过ｙｍｌ格式的描述文件来生成数据

positional arguments:
  meta_file             yml文件所在路径

optional arguments:
  -h, --help            show this help message and exit
  -n [NUMBER], --number [NUMBER]
                        生成数据数量
  -i, --insert          是否插入到数据库
  -c [CONNECT], --connect [CONNECT]
                        数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.ho
                        melabs.in/pdms_hospital
  -o [OUTPUT], --output [OUTPUT]
                        数据库连接语法，例如：mysql+mysqldb://pdmsadmin:system001@cpcs.ho
                        melabs.in/pdms_hospital


# 打印输出
python main.py meta.yml --number 10

# 保存到文件
python main.py meta.yml --number 10 -o out.sql

# 插入到数据库
python main.py meta.yml --number 10 -i --connect mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital
```

通过上述模板文件生成出sql:
```sql
insert into stu set id='2c5e318e24eb4bbeb6f0155721d5fa4d', name='郭杨', idcard='450329193605314982', age='84', sex='female';
insert into course set id='980e0c308b904e4d8574c14589b73d6c', stu_id='2c5e318e24eb4bbeb6f0155721d5fa4d', course_name='化学', course_time='2020-09-15 19:26:21';


insert into stu set id='dbd26e53363b4ad0a80d91bf20b58306', name='孙晨', idcard='441500198604185699', age='34', sex='man';
insert into course set id='46dc316ae223411fa0a5169e1cf9c7df', stu_id='dbd26e53363b4ad0a80d91bf20b58306', course_name='语文', course_time='2020-09-15 19:26:21';


insert into stu set id='bc779ca4b55a4216aa21692df798b8a2', name='陈秀华', idcard='321084195409070529', age='66', sex='female';
insert into course set id='0b981403fd4b4cc7afa8f85d7187d3b0', stu_id='bc779ca4b55a4216aa21692df798b8a2', course_name='语文', course_time='2020-09-15 19:26:21';


insert into stu set id='1982c0c518a4434f8bd4bace6baed3e2', name='张建平', idcard='341721194502236759', age='75', sex='man';
insert into course set id='371152b6f02c44f884c85daf1918cf90', stu_id='1982c0c518a4434f8bd4bace6baed3e2', course_name='语文', course_time='2020-09-15 19:26:22';


insert into stu set id='448e3cf1bbe648719b4802196a626efb', name='王瑞', idcard='360281193801017318', age='82', sex='man';
insert into course set id='fda8a3f261134c64b0a0dd516ecf2e0b', stu_id='448e3cf1bbe648719b4802196a626efb', course_name='数学', course_time='2020-09-15 19:26:27';


insert into stu set id='a3d4952faf054c6ba655c2b67e3b4afc', name='陈杨', idcard='640122198510102904', age='35', sex='female';
insert into course set id='8a7e021d765044f784979591f92ec28d', stu_id='a3d4952faf054c6ba655c2b67e3b4afc', course_name='化学', course_time='2020-09-15 19:26:27';


insert into stu set id='4098cc574f6c4fe5a85535a1d9e5002a', name='苏洁', idcard='341225199306268404', age='27', sex='female';
insert into course set id='77cdf72f82fa4d8882b304abbe97f3a4', stu_id='4098cc574f6c4fe5a85535a1d9e5002a', course_name='数学', course_time='2020-09-15 19:26:27';


insert into stu set id='949f3766cdbd417bb3d35858c8022816', name='刘柳', idcard='542133194402097393', age='76', sex='man';
insert into course set id='7ad45cc62c3847be814ef75d5287ecd6', stu_id='949f3766cdbd417bb3d35858c8022816', course_name='地理', course_time='2020-09-15 19:26:27';


insert into stu set id='97786d4eeb674462a1698fd25291d1ba', name='兰欣', idcard='330802194509029887', age='75', sex='female';
insert into course set id='a649370a793c44ac9b743d35afa17df9', stu_id='97786d4eeb674462a1698fd25291d1ba', course_name='数学', course_time='2020-09-15 19:26:27';


insert into stu set id='2534ed0806974511b92c954831a002e3', name='许玉梅', idcard='350401197207148812', age='48', sex='man';
insert into course set id='0d4dfe07fb3640c69afce366d102487d', stu_id='2534ed0806974511b92c954831a002e3', course_name='语文', course_time='2020-09-15 19:26:27';
```

