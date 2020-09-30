# dbfaker内置方法

## 前言
在使用dbfaker编写字段生成规则时需要指定engine字段使用的方法名。示例中已有一些相关说明，
但不完整。在这里整理一下当前dbfaker支持的所有方法。

### dbfaker内置方法
|  方法名   | 方法说明 |方法接收参数  | 返回值 | 
|  ----  | ----  |  ----  |  ----  |
| eq  | 直接返回给定的[value]参数 | value | value值原样返回 |
| hans2pinyin  | 给定汉字字符串[hans]返回该汉字的拼音，可通过参数[style(A-全拼，F-首字母)]控制返回全拼或首拼 | hans：str； style:str | str |
| choice  | 给定一个列表[value]，随机返回列表中的某个元素；当给定的value值是字符串是会使用json.loads方法来格式化字符串为列表。 | value：list； | str |
| choice_file  | 从指定目录中随机返回指定数量指定文件后缀的文件全路径 | path（从此目录中开始找）:str, file_match（正则匹配写法）:str=None, recursion(是否从子目录查找):bool=False, number(最多返回文件数量):int=1 | 文件路径的列表 |
| uuid  | 返回uuid格式的随机字符串，可通过参数[underline]控制是否去掉中间的“-”长度32位或36位（带“-”） | underline：bool=True | str |
| from_db  | 指定SQL语句[sql]从数据库中获取数据，可选择对查询结果是多条数据时处理方式[choice_method(random-随机,first-第一个)]，可通过参数来控制从返回的数据中取数据库中字段名为[key]的数据值返回，当key不指定时会返回一个字典 | sql：str, choice_method='random', key=None | str or dict |
| from_db_yield  | 从数据库中查询数据，返回一个迭代器对象，可使用next方法获取下一个值，可通过参数来控制从返回的数据中取数据库中字段名为[key]的数据值返回 | sql：str, key=None| 迭代器 |
| weights_randint  | 给定多个dict类型的参数[args]，返回带权重的随机整数；传参举例：多个dict类型的对象；比如： weights_randint({"weight": 0.8, "value": [1,10]}, {"weight": 0.2, "value": [11,20]})，返回1到10之间的是整数的权重是80%，返回11到20之间的整数的权重是20% | args | int |
| weights_randfloat  | 给定多个dict类型的参数[args]，返回带权重的随机浮点数，可通过参数[round_number]指定返回的浮点数小数点位数；传参举例：多个dict类型的对象；比如： weights_randfloat({"weight": 0.8, "value": [1.0,2.5]}, {"weight": 0.2, "value": [2.5,4]})，返回1到2.5之间的数的权重是80%，返回2.5到4之间的数的权重是20% | args, round_number:int=2 | float |
| weights_choice  | 给定多个dict类型的参数[args], 从给定的列表中带权重返回某个元素; 传参举例： 比如： weights_randint({"weight": 0.8, "value": ['A','B']}, {"weight": 0.2, "value": ['C','D]})，返回A或者B的权重是80%，返回C或者D的权重是20% | args | object |
| multi_choice  | 从指定的列表[value]中随机选择多个，并使用指定的拼接字符[splits]拼起来返回,可指定要拼接字符的数量[rand_number] | value：list, splits="&#124;", rand_number=None | str |
| randint  | 给定一个长度为2的列表[value]返回指定范围的整数 | value: list | int |
| randfloat  | 给定一个长度为2的列表[value]返回指定范围的浮点数，浮点数的小数点长度为[round_num] | value: list，round_num=2 | float |
| order  | 给定一个列表[value]返回一个列表生成器对象，使用next()来调用，可指定列表是否需要乱序[out_of_order] | value: list，out_of_order=False | float |
| date_time_between  | 给定开始的时间点[start_date]和结束时间点[end_date]，从时间范围内返回随机时间；可指定时区[tzinfo]、时间偏移[offset]、返回的时间格式[format],参考faker库中的[date_time_between](https://faker.readthedocs.io/en/stable/providers/faker.providers.date_time.html?highlight=date_time_between#faker.providers.date_time.Provider.date_time_between) | start_date=None, end_date=None, tzinfo=None, offset=None, format=None | str |
| date_time_subtraction  | 给定开始的时间点[start_date]和要调整的时间[sub_time]，从时间范围内返回随机时间；可通过参数[approximate_time]指定时间是否进行随机偏移，指定后返回的时间将不完全按照[sub_time]字段来显示，会随机将[sub_time]加或者减去自身0-1倍来返回。做到模拟更随机的时间。 | start_date, sub_time, format=None, approximate_time=True | float |
| now  | 返回当前时间的指定格式[format],不指定format时返回时间戳 | format:None | float |

### 更多参数可参考[faker标准库方法](https://faker.readthedocs.io/en/stable/providers.html)