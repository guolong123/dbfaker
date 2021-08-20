#coding:utf8
"""
总结：
1. 变量形式定义的token，正则表达式的长度越长，优先级越高
2. 函数形式定义的token，优先级根据函数的定义顺序由上至下
"""
import os, sys
import re
import ply.lex as lex

literals = [',', '.', '(', ')', ';', '=']

reserved = [
	'CREATE','TABLE','UNSIGNED','NOT','NULL','DEFAULT','COMMENT','AUTO_INCREMENT','PRIMARY','UNIQUE','KEY','ENGINE',
	'CHARSET','CHARACTER','SET','USING','COLLATE','ROW_FORMAT', 'CURRENT_TIMESTAMP', 'ON', 'UPDATE'
]

tokens = [
	'iKEYWORD',
	'iINTEGER',
	'iFLOAT',

	'iCHAR', 
	'iESCAPE',
	'iLBRACE',
	'iRBRACE'
] + reserved

states = (
	('str', 'inclusive'),
	('name', 'inclusive'),
)

t_ignore = " \t\r"
t_ignore_comment_sig = r'--(\s[^\n]*)??\n'
t_ignore_comment_mul = r'\/\*(.|\n)+?\*\/'
t_str_ignore = ''
t_name_ignore = ''

t_iINTEGER = r'\d+'
t_iFLOAT = r'\d+\.\d+'

def t_iKEYWORD(t):
	r'[a-zA-Z][a-zA-Z0-9_]+'
	
	if t.value.upper() in reserved:
		t.type = t.value.upper()
	else:
		t.type = 'iKEYWORD'

	return t

########### 单引号的字符串

def t_begin_str(t):
	r'\''
	t.lexer.push_state('str')
	t.type = 'iLBRACE'
	return t

def t_str_escape(t):
	r'\'\''
	t.type = 'iESCAPE'
	return t

def t_str_iCHAR(t):
	r'[^\']'
	return t

def t_str_end(t):
	r'\''
	t.lexer.pop_state()
	t.type = 'iRBRACE'
	return t
	
########### 反引号的对象名称

def t_begin_name(t):
	r'`'
	t.lexer.push_state('name')
	t.type = 'iLBRACE'
	return t

def t_name_escape(t):
	r'``'
	t.value = '`'
	t.type = 'iESCAPE'
	return t

def t_name_iCHAR(t):
	r'[^`]'
	return t

def t_name_end(t):
	r'`'
	t.lexer.pop_state()
	t.type = 'iRBRACE'
	return t

def t_newline(t):
	r'\n'
	t.lexer.lineno += 1

########### 错误处理
	 
def t_error(t):
	raise SyntaxError(t)

lexer = lex.lex(debug=False)

