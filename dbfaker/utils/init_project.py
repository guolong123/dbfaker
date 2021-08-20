import os

SAMPLE_YAML_DATA = '''package:
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
- table: stu
  comment: '学生表'
  columns:
    id:
      comment: 数据主键id
      engine: faker.eq(value='{{ env.id }}') # 通过引用环境变量中的值
    name:
      comment: 姓名
      engine: faker.name
    idcard:
      comment: 身份证号
      engine: faker.ssn
    age:
      comment: 年龄
      engine: faker.eq(value='{{ datetime.datetime.now().year - int(stu.idcard[6:10]) }}')  #　通过jinja２模板直接计算
    sex:
      comment: 性别
      engine: faker.eq(value='{{ "man" if int(stu.idcard[-2]) % 2==1 else "female" }}')  #　通过jinja２模板直接计算
- table: course
  comment: '课程信息 '
  columns:
    id:
      comment: 数据主键id
      engine: faker.uuid
    stu_id:
      comment: 数据主键id
      engine: faker.eq(value='{{ stu.id }}')  # 通过其他表中的值
    course_name:
      comment: 课程名称
      engine: faker.choice(value=['数学','语文','英语','化学','地理']) # 通过内置方法从列表中随机取一个值
    course_time:
      comment: 上课时间
      engine: faker.now(format="{{ env.time_format }}")  # 通过内置方法获取当前时间，并按照指定格式返回

extraction:  # 从已生成的数据中提取字段
  stu_id:
    value: '{{ stu.id }}'
    default: null
  course_id:
    value: '{{ course.id }}'
  stu_name:
    value: '{{ stu.name }}'
    default: '测试用户'

'''

SAMPLE_FUNCTION = '''from faker.providers import BaseProvider
import hashlib


class MProvider(BaseProvider):
    def md5(self, value: bytes):
        if isinstance(value, str):
            value = value.encode()
        return hashlib.md5(value).hexdigest()
'''


README = '''# 目录结构说明
```
.
├── data    # yaml文件存放位置
├── log     # 执行日志
└── script  # 自定义方法的Python文件存放位置；在此路径中的所有py结尾的文件中的继承faker.BaseProvider类的子类会被动态加载到faker执行方法中。
```
'''

def scaffold(project_name='dbfaker-project', path=None):
    '''
    初始化dbfaker项目
    '''
    if not path:
        path = os.path.curdir
    if not os.path.isdir(path):
        raise OSError('目录错误')
    cur_dir = os.path.join(path, project_name)
    os.mkdir(cur_dir) if not os.path.exists(cur_dir) else None
    os.chdir(cur_dir)
    os.mkdir('data') if not os.path.exists('data') else None
    os.mkdir('log') if not os.path.exists('log') else None
    os.mkdir('script') if not os.path.exists('script') else None
    with open(os.path.join('data', 'example.yml'), 'w', encoding='utf-8') as f:
        f.write(SAMPLE_YAML_DATA)
    with open(os.path.join('script', 'example.py'), 'w', encoding='utf-8') as f:
        f.write(SAMPLE_FUNCTION)
    with open(os.path.join('readme.md'), 'w', encoding='utf-8') as f:
        f.write(README)
    print('项目初始化完成')
