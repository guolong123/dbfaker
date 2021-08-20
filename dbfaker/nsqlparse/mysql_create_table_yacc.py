# coding:utf8
import os, sys
import re
import ply.yacc as yacc
from dbfaker.nsqlparse.mysql_create_table_lex import tokens
import json


def p_error(p):
    print('-------------', p.lineno, dir(p))
    raise SyntaxError(p)


################## 入口

def p_start(p):
    '''
    start : createTable
    '''
    p[0] = [p[1]]


def p_start_empty(p):
    '''
    start : ';'
    '''
    p[0] = []


def p_start_mul(p):
    '''
    start : start ';' createTable
    '''
    p[0] = p[1] + [p[3]]


def p_start_empty1(p):
    '''
    start : start ';'
    '''
    p[0] = p[1]


################## 创建表

def p_createTable_columns(p):
    '''
    createTable : CREATE TABLE tableName '(' tableColumns ')'
    '''
    p[0] = {**p[3], **{'columns': p[5]}}


def p_createTable_keys(p):
    '''
    createTable : CREATE TABLE tableName '(' tableColumns ',' tableKeys ')'
    '''
    p[0] = {**p[3], **{'columns': p[5]}, **{'keys': p[7]}}


def p_createTable_attribute_default_charset(p):
    '''
    createTable : createTable DEFAULT CHARSET '=' iKEYWORD
    '''
    p[0] = {**p[1], **{'default_charset': p[5].lower()}}


def p_createTable_attribute_engine(p):
    '''
    createTable : createTable ENGINE '=' iKEYWORD
    '''
    p[0] = {**p[1], **{'engine': p[4].lower()}}


def p_createTable_attribute_auto_increment(p):
    '''
    createTable : createTable AUTO_INCREMENT '=' iINTEGER
    '''
    p[0] = {**p[1], **{'auto_increment': int(p[4])}}


def p_createTable_attribute_comment(p):
    '''
    createTable : createTable COMMENT '=' str
    '''
    p[0] = {**p[1], **{'comment': p[4]}}


def p_createTable_attribute_collate(p):
    '''
    createTable : createTable COLLATE '=' iKEYWORD
    '''
    p[0] = {**p[1], **{'collate': p[4].lower()}}


def p_createTable_attribute_row_format(p):
    '''
    createTable : createTable ROW_FORMAT '=' iKEYWORD
    '''
    p[0] = {**p[1], **{'row_format': p[4].lower()}}


################## 表索引定义

def p_tableKeys_item(p):
    '''
    tableKeys : tableKey
    '''
    p[0] = [p[1]]


def p_tableKeys_list(p):
    '''
    tableKeys : tableKeys ',' tableKey
    '''
    p[0] = p[1] + [p[3]]


def p_tableKey(p):
    '''
    tableKey : KEY columnName '(' columnNames ')'
    '''
    p[0] = {'columns': p[4], 'name': p[2]['column'], 'type': 'key'}


def p_tableKey_primary(p):
    '''
    tableKey : PRIMARY KEY '(' columnNames ')'
    '''
    p[0] = {'columns': p[4], 'type': 'primary'}


def p_tableKey_unique(p):
    '''
    tableKey : UNIQUE KEY columnName '(' columnNames ')'
    '''
    p[0] = {'columns': p[5], 'name': p[3]['column'], 'type': 'unique'}


def p_tableKey_unique_comment(p):
    '''
    tableKey : tableKey COMMENT columnName
    '''

def p_tableKey_using(p):
    '''
    tableKey : tableKey USING iKEYWORD
    '''
    p[0] = {**p[1], 'using': p[3].upper()}


################## 表字段定义

def p_tableColumns_item(p):
    '''
    tableColumns : tableColumn
    '''
    p[0] = [p[1]]


def p_tableColumns_list(p):
    '''
    tableColumns : tableColumns ',' tableColumn
    '''
    p[0] = p[1] + [p[3]]


def p_tableColumn(p):
    '''
    tableColumn : columnName dataType
    '''
    p[0] = {**p[1], **p[2]}


def p_tableColumn_attribute_notnull(p):
    '''
    tableColumn : tableColumn NOT NULL
    '''
    p[0] = {**p[1], **{'not_null': True}}


def p_tableColumn_attribute_null(p):
    '''
    tableColumn : tableColumn NULL
    '''
    p[0] = {**p[1], **{'not_null': False}}


def p_tableColumn_attribute_comment(p):
    '''
    tableColumn : tableColumn COMMENT str
    '''
    try:
        p[0] = {**p[1], **{'comment': p[3]}}
    except TypeError:
        print(1)


def p_tableColumn_attribute_auto_increment(p):
    '''
    tableColumn : tableColumn AUTO_INCREMENT
    '''
    p[0] = {**p[1], **{'auto_increment': True}}


def p_tableColumn_attribute_collate(p):
    '''
    tableColumn : tableColumn COLLATE iKEYWORD
    '''
    p[0] = {**p[1], **{'collate': p[3].lower()}}


def p_tableColumn_attribute_character_set(p):
    '''
    tableColumn : tableColumn CHARACTER SET iKEYWORD
    '''
    p[0] = {**p[1], **{'character_set': p[3].lower()}}


### 字段默认值

def p_tableColumn_attribute_default_int(p):
    '''
    tableColumn : tableColumn DEFAULT iINTEGER
    '''
    p[0] = {**p[1], **{'default': int(p[3])}}


def p_tableColumn_attribute_default_float(p):
    '''
    tableColumn : tableColumn DEFAULT iFLOAT
    '''
    p[0] = {**p[1], **{'default': float(p[3])}}


def p_tableColumn_attribute_default_str(p):
    '''
    tableColumn : tableColumn DEFAULT str
    '''
    p[0] = {**p[1], **{'default': '\'' + p[3] + '\''}}


def p_tableColumn_attribute_default_keyword(p):
    '''
    tableColumn : tableColumn DEFAULT iKEYWORD
                | tableColumn DEFAULT NULL
    '''
    p[0] = {**p[1], **{'default': p[3].upper()}}

def p_tableColumn_attribute_default_current_timestamp(p):
    '''
    tableColumn : tableColumn DEFAULT CURRENT_TIMESTAMP '(' iINTEGER ')'
                | tableColumn DEFAULT CURRENT_TIMESTAMP
    '''
    if len(p) >= 5:
        p[0] = {**p[1], **{'default': 'CURRENT_TIMESTAMP({})'.format(p[5])}}
    else:
        p[0] = {**p[1], **{'default': 'CURRENT_TIMESTAMP'}}

def p_tableColumn_attribute_default_update_current_timestamp(p):
    '''
    tableColumn : tableColumn ON UPDATE CURRENT_TIMESTAMP '(' iINTEGER ')'
                | tableColumn ON UPDATE CURRENT_TIMESTAMP
    '''
    p[0] = {**p[1]}


### 字段数据类型定义

def p_dataType_normal(p):
    '''
    dataType : iKEYWORD
    '''
    p[0] = {'type': p[1]}


def p_dataType_len(p):
    '''
    dataType : iKEYWORD '(' iINTEGER ')'
    '''
    p[0] = {'type': p[1], 'length': p[3]}




def p_dataType_decimal(p):
    '''
    dataType : iKEYWORD '(' iINTEGER ',' iINTEGER ')'
    '''
    p[0] = {'type': p[1], 'length': p[3] + ',' + p[5]}


def p_dataType_enum(p):
    '''
    dataType : iKEYWORD '(' dataTypeEnum ')'
    '''
    p[0] = {'type': p[1], 'length': p[3]}


def p_dataTypeEnum_item(p):
    '''
    dataTypeEnum : str
    '''
    p[0] = [p[1]]


def p_dataTypeEnum_list(p):
    '''
    dataTypeEnum : dataTypeEnum ',' str
    '''
    p[0] = p[1] + [p[3]]


def p_dataType_unsigned(p):
    '''
    dataType : dataType UNSIGNED
    '''
    p[0] = {**p[1], **{'unsigned': True}}


################## 数据库、数据表、字段名称定义

def p_name_char(p):
    '''
    name : iCHAR
    '''
    p[0] = p[1]


def p_name_escape(p):
    '''
    name : iESCAPE
    '''
    p[0] = '`'


def p_name_str(p):
    '''
    name : name iCHAR
    '''
    p[0] = p[1] + p[2]


def p_name_str_escape(p):
    '''
    name : name iESCAPE
    '''
    p[0] = p[1] + '`'


def p_name_safe(p):
    '''
    name : iLBRACE name iRBRACE
    '''
    p[0] = p[2]


def p_databaseName(p):
    '''
    databaseName : name
    '''
    p[0] = p[1]


def p_tableName(p):
    '''
    tableName : name
    '''
    p[0] = {'table': p[1]}


def p_tableName_for_db(p):
    '''
    tableName : databaseName '.' name
    '''
    p[0] = {'database': p[1], 'table': p[3]}


def p_columnName(p):
    '''
    columnName : name
    '''
    p[0] = {'column': p[1]}


def p_columnName_for_table(p):
    '''
    columnName : tableName '.' name
    '''
    p[0] = {**p[1], **{'column': p[3]}}


def p_columnName_len(p):
    '''
    columnName : columnName '(' iINTEGER ')'
    '''
    p[0] = {**p[1], **{'length': int(p[3])}}


def p_columnNames_item(p):
    '''
    columnNames : columnName
    '''
    p[0] = [p[1]]


def p_columnNames_list(p):
    '''
    columnNames : columnNames ',' columnName
    '''
    p[0] = p[1] + [p[3]]


################## 字符串定义

def p_str_char(p):
    '''
    str : iCHAR
    '''
    p[0] = p[1]


def p_str_escape(p):
    '''
    str : iESCAPE
    '''
    p[0] = '\''


def p_str_str(p):
    '''
    str : str iCHAR
    '''
    p[0] = p[1] + p[2]


def p_str_str_escape(p):
    '''
    str : str iESCAPE
    '''
    p[0] = p[1] + '\''


def p_str(p):
    '''
    str : iLBRACE str iRBRACE
    '''
    p[0] = p[2]


def p_str_empty(p):
    '''
    str : iLBRACE iRBRACE
    '''
    p[0] = ''


parser = yacc.yacc(start='start', debug=False, write_tables=False)

if __name__ == '__main__':
    d = '''CREATE TABLE `stu` (
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
	
	'''
    r = parser.parse(d)
    print(r)
