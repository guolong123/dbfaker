# dbfaker

#### 介绍
基于数据库层面批量生成有逻辑关联的数据

#### 软件架构
软件架构说明
对于要造大量数据来讲，有几种方式，一是通过开发写的接口来模拟真实用户场景来产生数据，这种方式在某些方面来讲是比较合适的，比如因为是模拟用户场景，业务数据完整，不会丢．但不好的地方就是要处理的地方太多，接口定义，签名，加密等等，还有扩展性也很不好，一个业务场景要写一套代码．另一种方式，是已知业务产生的数据之间的依赖关系后，直接在数据库中插入相关数据，本项目就是通过这种方式来实现，好处就是生成规则通过配置文件来描述即可（ymal文件），不需要额外添加代码（对于某些字段生成规则有可能需要单独编写方法），与测试库testrunner比较类似．现在已知有些库也支持直接在数据库内造数据，但对库表之间的关联关系的处理都做得不太好．

本项目数据处理流程如下：
![处理流程](https://images.gitee.com/uploads/images/2020/0915/183724_40e0141c_1021400.png "屏幕截图.png")

#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

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
meta.yml文件格式：
```yaml
pakages:
  - datetime　＃　导入额外的包，在jinja2模板中使用（下面有用到datetime包，所以要先导入）
env:
  id:
    engine: faker.uuid
    rule: null
  time_format: "%Y-%m-%d %H:%M:%S"
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
        value: '{{ datetime.datetime.now().year - int(information_sick.idcard[6:10]) }}'　＃　通过jinja２模板直接计算
    - column: sex
      comment: 性别
      engine: faker.eq
      rule: 
        value: '{{ "man" if int(information_sick.idcard[-2]) % 2==1 else "female" }}'　＃　通过jinja２模板直接计算
    comment: '病人资料 '
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
      engine: faker.choice　　＃ 通过内置方法从列表中随机取一个值
      rule: 
        value: [数学,语文,英语,化学,地理]
    - column: course_time
      comment: 上课时间
      engine: faker.now　　＃ 通过内置方法从列表中随机取一个值
      rule: 
        format: "{{ env.time_format }}"
    comment: '课程信息 '
    table: course


```
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 码云特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5.  码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
