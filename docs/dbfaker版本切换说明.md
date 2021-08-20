# dbfaker版本切换说明

dbfaker 由于最初的yaml文件格式处理得不够优雅，视觉效果不太好，影响观感，容易出错。
所以修改了yaml文件的格式，使其看起来更易于辨析。

新的版本（v1.0.0及以上）与老的版本（v0.0.5及以下）配置文件不能通用。故提供了配置文件转换功能。
可使用table2yml直接将老的配置文件转换为新的配置文件。转换方式如下：
```shell script
table2yml ymlcov --yml_file ./test.yml [--hide_comment]
```
转换成功后将在原文件目录输出`test_new.yml`文件。