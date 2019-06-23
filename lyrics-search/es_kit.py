# -*- encoding: utf8 -*-
from __future__ import print_function
import sys
import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch import helpers

logging.basicConfig(level = logging.INFO,
	format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_index = "lyrics"
_url = "http://127.0.0.1:9200/"

class ESKit(object):
	"""docstring for ESKit"""
	def __init__(self, index_name=_index, url=_url):
		""" ES 初始化 """
		super(ESKit, self).__init__()
		self.index_name = index_name
		self.mappings = None
		self.es = Elasticsearch([url])

	def create_index(self, mappings=None):
		""" ES 创建索引 """
		if mappings:
			self.mappings = json.load(open(mappings,'r'))
			print(self.mappings)

		if self.es.indices.exists(index=self.index_name) is not True:
			res = self.es.indices.create(index=self.index_name, body=self.mappings, ignore=400)
			print(res)

	def bulk_data(self, actions):
		""" ES bulk 批量操作 """
		res, _ = helpers.bulk(self.es, actions, index=self.index_name, raise_on_error=True)
		print(res)

	def insert_data(self, filename):
		""" ES 灌库
		:param filename: json数据文件, 每行一条数据
		"""
		actions = []
		bulk_num = 2000
		with open(filename) as fin:
			for line in fin:
				src = json.loads(line.strip())
				action = {
					"_index": self.index_name,
					"_source": src
				}
				actions.append(action)
				if len(actions) == bulk_num:
					self.bulk_data(actions)
					actions = []
			if len(actions) > 0:
				self.bulk_data(actions)
		logging.info("Insert data done!")

	def delete_index(self):
		""" ES 删除索引 """
		logging.info('Delete index %s' % self.index_name)
		self.es.indices.delete(self.index_name)


if __name__ == '__main__':
	eskit = ESKit()
	eskit.create_index(mappings='mappings.json')
	eskit.insert_data('./data/test.json')
	#eskit.delete_index()
					

		
