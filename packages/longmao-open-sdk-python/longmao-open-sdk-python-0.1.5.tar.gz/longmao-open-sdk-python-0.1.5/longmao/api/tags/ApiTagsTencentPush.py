# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022-11-15
@author: nayuan
'''

from longmao.api.Api import Api
from longmao.core.exception.Exception import RequestException

class ApiTagsTencentPush(Api):

    def __init__(self):
        super(ApiTagsTencentPush, self).__init__('longmao.tags.tencent.push', '20221115')

        self._task_id = None
        self._task_type = None
        self._title = None
        self._task_level = None
        self._file_path = None

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def task_level(self):
        return self._task_level

    @task_level.setter
    def task_level(self, value):
        self._task_level = value

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, value):
        self._task_type = value

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def get_params(self):

        if not self._title or not self._title.strip():
            raise RequestException("任务备注[title]不能为空")
        if not self._task_id or not self._task_id.strip():
            raise RequestException("标注任务ID[task_id]不能为空")
        if not self._task_type or not self._task_type.strip():
            raise RequestException("任务类型[task_type]不能为空")
        if not self._task_level or not self._task_level.strip():
            raise RequestException("任务类型[task_level]不能为空")
        if not self._file_path or not self._file_path.strip():
            raise RequestException("文件路径[file_path]不能为空")

        data = dict()
        data['title'] = self._title
        data['task_id'] = self._task_id
        data['task_type'] = self._task_type
        data['task_level'] = self._task_level
        data['file_path'] = self._file_path
        return data
