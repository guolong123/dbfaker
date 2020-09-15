# coding:utf8
import os, sys
import hashlib
import json
import re
from nsqlparse.mysql_create_table_yacc import parser

databases = []
indexes = {}

for i in range(1, len(sys.argv)):
	with open(sys.argv[i]) as f:
		sql = f.read()

	tables = parser.parse(sql)

	for table in tables:
		k = table['table'].lower()
		if not k in indexes:
			indexes[k] = []
		indexes[k].append(table)
		
	databases.append(tables)

if len(databases) == 0:
	sys.exit(0)

tables = []
categories = {}
at = {}

for table in databases[0]:
	# 找到表注释中的 @table.field 加入到 at 中
	columns = list(filter(lambda column: True if 'comment' in column else False, table['columns']))
	comments = list(map(lambda column: column['comment'], columns))
	if 'comment' in table:
		comments.append(table['comment'])

	for comment in comments:
		r = re.findall('@(\w+)(\.(\w+))*', comment) # [('tablename', '.column', 'column'), ...]
		if not r:
			continue

		for s in r:
			t = s[0].lower()
			if t in at:
				continue

			# 检查 @table 是否存在
			if not t in indexes:
				sys.stderr.write(f"ERROR:\"@{t}\" not found at table \"{table['table']}\"\n")
				continue

			at[t] = indexes[t]

	# 分隔表注释，提取出模块名称

	if 'comment' in table:
		t = table['comment'].split('-', 1)
		if len(t) == 2:
			if not t[0] in categories:
				categories[t[0]] = {'name': t[0], 'children': []}
			categories[t[0]]['children'].append({**table, **{'comment': t[1]}})
			continue

	tables.append(table)
	
print(json.dumps({'table_tree': list(categories.values()) + tables, 'table_at': at}, indent=4))