##### 11月11日
字段生成语法支持直接在jinja2模板中调用字段生成方法，举例：
```yaml
package: []
env:
  name: '{{ faker.name() }}'
tables:
- table: stu
  comment: null
  columns:
    # 新增字段生成描述，可直接在jinja2模板中调用生成方法，调用方式参考Python语法
    id: '{{ faker.uuid() }}'
# 老的生成方式，通过engine字段描述字段生成方法
#   id:
#     engine: faker.uuid()
```
##### 11月16日
支持在数据库建表语句的comment字段中描述字段生成规则；详见：[使用comment字段来描述生成规则](https://gitee.com/guojongg/dbfaker/blob/develop/docs/使用comment字段来描述生成规则.md)
