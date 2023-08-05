#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import glob
import logging
import re
from datetime import datetime

from scutils import Singleton

from sc_retail_email_sender.utils import ConfigUtils, EmailUtils


class EmailSender(metaclass=Singleton):
    """
    Email发送相关工具类
    """

    def __init__(self):
        self._read_config()
        self._date_format = "%Y年%m月%d日"
        today = datetime.now()
        self._current_date = today.strftime(self._date_format)

    def _read_config(self):
        """
        读取配置，初始化相关变量
        """
        config = ConfigUtils.get_config()
        # 邮件主题
        self._subject: str = config.get("email.subject")
        # 模板文件路径
        self._template_filename: str = config.get("email.template_filename")
        # 附件文件名模式
        self._attachment_filename_pattern: str = config.get("email.attachment_filename_pattern")
        attachment_filename_regex = self._attachment_filename_pattern.replace("*", "(.*)")
        self._attachment_filename_regex_pattern = re.compile(attachment_filename_regex)
        # 接收者
        self._receiver_dict: dict = config.get("email.receiver")
        # 抄送人列表
        self._cc_receiver_list: list = config.get("email.cc_receiver")

    def send_email(self):
        # 读取模板文件内容
        with open(self._template_filename, 'r', encoding="utf-8") as f:
            file_content = f.read()

        file_list = glob.iglob(self._attachment_filename_pattern)
        for filename in file_list:
            match_result = self._attachment_filename_regex_pattern.match(filename)
            if match_result is None:
                continue
            branch_name = match_result.group(1)
            html_content = file_content % (filename, self._current_date)
            if branch_name not in self._receiver_dict.keys():
                logging.getLogger(__name__).error("机构%s未配置收件人", branch_name)
                continue
            receivers = self._receiver_dict.get(branch_name)
            EmailUtils.send_email(
                subject=self._subject,
                html_content=html_content,
                receivers=receivers,
                cc_receivers=self._cc_receiver_list,
                attachments=[filename],
            )
