# dbfaker

#### 介绍
基于数据库层面批量生成有逻辑关联的数据

[![star](https://gitee.com/guojongg/dbfaker/badge/star.svg?theme=dark)](https://gitee.com/guojongg/dbfaker/stargazers)
[![Downloads](https://pepy.tech/badge/dbfaker)](https://pepy.tech/project/dbfaker)
[![pypi version](https://img.shields.io/pypi/v/dbfaker.svg)](https://pypi.python.org/pypi/dbfaker)

#### 软件架构
对于要造大量数据来讲，有几种方式，一是通过开发写的接口来模拟真实用户场景来产生数据，这种方式在某些方面来讲是比较合适的，比如因为是模拟用户场景，业务数据完整，不会丢．但不好的地方就是要处理的地方太多，接口定义，签名，加密等等，还有扩展性也很不好，一个业务场景要写一套代码．另一种方式，是已知业务产生的数据之间的依赖关系后，直接在数据库中插入相关数据，本项目就是通过这种方式来实现，好处就是生成规则通过配置文件来描述即可（yaml文件），不需要额外添加代码（对于某些字段生成规则有可能需要单独编写方法），与测试库testrunner比较类似．现在已知有些库也支持直接在数据库内造数据，但对库表之间的关联关系的处理都做得不太好．

另外对于测试人员进行自动化接口测试时，前置数据是个问题，是通过业务接口一条条跑完作为前置数据产生条件还是直接在数据库里面插入需要的数据呢？前面一种方式在业务场景复杂的时候用例的维护可能会变得极其麻烦。比如：
> 你要测试一个用户加入商品到购物车的一个接口；前置数据有哪些？
>1. 用户账号
>2. 商品
>
>通过接口来造数据的流程如下：
>1. 通过用户端注册接口来创建账号
>2. 通过管理端接口登录，拿到token（预设管理端账号是已经存在了，如果不存在你还得注册管理端账号）
>3. 登陆后通过管理端接口创建商品信息
>
>这三个步骤看起来简单，但实际上针对某些业务场景还有接口加密、签名、而且几乎每一条测试用例都需要用到N个前置条件，这些通过接口来调用的前置条件只要有一个失败就会影响你真正要测试的接口。做过接口测试的同学应该深有体会；
>
实际上实现上述接口测试，真正要测的只是商品是否能正常加入到购物车；真正依赖的就只有两个数据，用户账号和商品信息。我们只需要在用户表和商品表里面各插入一条数据就可以了。通过本工具，只需要描述两个表的每个字段的生成规则就可以直接在数据库中插入两条“十分真实”的数据。用这种方式来解决测试用例前置条件的问题不说是最好的方式，但肯定是比上面的前置用例的方式好很多。

本项目数据处理流程如下：
![处理流程](https://images.gitee.com/uploads/images/2020/0915/183724_40e0141c_1021400.png "屏幕截图.png")

#### 安装
```shell script
git clone https://gitee.com/guojongg/dbfaker.git
cd dbfaker
# 可先创建虚拟环境后再安装
python3 setup.py install
# 使用pip直接安装
pip3 install dbfaker

# 卸载
pip uninstall dbfaker

```

#### 使用说明

１．　生成meta.yml文件，可通过内置工具table2yml.py来一键生成模板，生成后需完善模板中表字段的定义
    
table2yml.py文件使用说明：
```shell
usage: table2yml [-h] [--connect [CONNECT]] [--table_names [TABLE_NAMES]]
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
PC:~/01 Work/07 MyProject/dbfaker$ source venv/bin/activate
(venv) PC:~/01 Work/07 MyProject/dbfaker$ dbfaker -h
usage: dbfaker [-h] [-n [NUMBER]] [-i] [-c [CONNECT]] [-o [OUTPUT]] [-p]
               [--project_name PROJECT_NAME]
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
                        指定文件名，输出内容到文件
  -p, --_print          是否打印到控制台
  --project_name PROJECT_NAME
                        初始化项目时的项目名称


# 打印输出
dbfaker data/test.yml --number 10 -p

# 保存到文件
dbfaker data/test.yml --number 10 -o out.sql

# 插入到数据库
dbfaker data/test.yml --number 10 -i --connect mysql+mysqldb://pdmsadmin:system001@cpcs.homelabs.in/pdms_hospital
```

通过上述模板文件生成出sql:
```sql
(venv) guolong@guolong-PC:~/01Work/07MyProject/dbfaker$ dbfaker data/test.yml -p -n 10
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 121.26条/s]
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('873ebda283ad418681427eee33599d88','常斌','320311197109145812','49','man');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('c642936a6a3d4067a0bdeaa738e777f7','873ebda283ad418681427eee33599d88','英语','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('975a595bdbe44bca9066e899cf095fdf','朱超','371403194412033153','76','man');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('e7fce0bd705d407d82365c5078e18e9f','975a595bdbe44bca9066e899cf095fdf','语文','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('c7a35fc6034b416b84633aba68f948a5','谭桂花','220881193603124667','84','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('9ec067ab61384b82839f037d19046d54','c7a35fc6034b416b84633aba68f948a5','地理','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('ec50b43857894724a8520fe4267cdb1c','黄颖','430424200102150376','19','man');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('a82ca7d9dfb14084ac59f3eef81c397d','ec50b43857894724a8520fe4267cdb1c','语文','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('ada7f3efbd6c44cbbb2b4e97f1e2192e','崔芳','110102197508318809','45','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('09068ec48e344513aa13248afc2a6c9a','ada7f3efbd6c44cbbb2b4e97f1e2192e','语文','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('c7be9316a52d4ce6813e2522c06ec244','伍建','530424195111204807','69','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('b525533bd784470898075b6c3c98e319','c7be9316a52d4ce6813e2522c06ec244','化学','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('ab8156d118ce47388ec080d4ca182324','张杰','430722199410179304','26','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('df802e97f23e43c6b8329f3bc80532b4','ab8156d118ce47388ec080d4ca182324','化学','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('dc508ae92cd14c2b8b44f881e9a2a9dc','温玲','361030193711149093','83','man');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('37a72421f0ec419aa181cb38f3216866','dc508ae92cd14c2b8b44f881e9a2a9dc','语文','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('48ddceaacddf43fd850a750c003f65e4','杨芳','530322197311251166','47','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('083d692d6a35483a9f4c77d99cb74abc','48ddceaacddf43fd850a750c003f65e4','语文','2020-10-21 16:39:07');
INSERT INTO `stu` (`id`,`name`,`idcard`,`age`,`sex`) VALUES ('f1e6ff166e504f4b9a1c4ef5c2791e2d','万帅','321323197507311448','45','female');
INSERT INTO `course` (`id`,`stu_id`,`course_name`,`course_time`) VALUES ('47e6cbb2999c433fb15f2102eec95295','f1e6ff166e504f4b9a1c4ef5c2791e2d','地理','2020-10-21 16:39:07');
执行完成，共生成10组数据
```

#### 更多例子
[usage example(使用举例)](https://gitee.com/guojongg/dbfaker/blob/master/docs/%E4%BD%BF%E7%94%A8%E4%B8%BE%E4%BE%8B.md)

#### 内置方法一览
[dbfaker内置方法速览](https://gitee.com/guojongg/dbfaker/blob/master/docs/dbfaker%E5%86%85%E7%BD%AE%E6%96%B9%E6%B3%95.md)

#### 自定义方法使用说明
[dbfaker自定义方法使用说明](https://gitee.com/guojongg/dbfaker/blob/master/docs/%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E6%B3%95%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)

__觉得还可以，帮忙点个赞！！！__

__如果有意见或建议或者遇到相关问题需要探讨解决方案欢迎给我提：[Issue](https://gitee.com/guojongg/dbfaker/issues)__
