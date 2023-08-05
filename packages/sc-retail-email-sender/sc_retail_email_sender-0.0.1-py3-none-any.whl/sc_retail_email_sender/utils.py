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


__all__ = {
    "ConfigUtils",
    "EmailUtils",
}

import logging
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config42
from scconfig.config import Config
from scutils import Singleton

from .configs.default import DEFAULT_CONFIG
from .exceptions import EmailSendException


class ConfigUtils(metaclass=Singleton):
    """
    配置文件相关工具类
    """

    _config = None

    def __init__(self):
        pass

    @classmethod
    def clear(cls) -> None:
        """
        清除配置信息
        :return:
        """
        cls._config = None

    @classmethod
    def load_configurations(cls) -> None:
        """
        加载配置文件
        :return:
        """
        try:
            # load configurations
            cls._config = Config.create(project_name="sc-retail-email-sender", defaults=DEFAULT_CONFIG)
        except Exception as error:
            cls._config = {}
            logging.getLogger(__name__).exception("failed to read configuration", exc_info=error)

    @classmethod
    def get_config(cls) -> config42.ConfigManager:
        """
        获取配置信息
        :return: 配置信息字典
        """
        if cls._config is None:
            cls.load_configurations()
        return cls._config


class EmailUtils:
    """
    Email操作相关工具类
    """

    # SMTP服务器
    _smtp_server: str = None
    # 发件人账号
    _username: str = None
    # 发件人账号密码
    _password: str = None

    @classmethod
    def read_config(cls):
        """
        读取配置，初始化相关变量
        """
        config = ConfigUtils.get_config()
        # SMTP服务器
        cls._smtp_server = config.get("email.smtp")
        # 发件人账号
        cls._username = config.get("email.username")
        # 发件人账号密码
        cls._password = config.get("email.password")

    @classmethod
    def send_email(
            cls, *,
            subject: str,
            html_content: str,
            receivers: list,
            cc_receivers: list = None,
            attachments: list = None
    ):
        """
        发送邮件

        :param subject: 邮件主题
        :param html_content: HTML格式的邮件内容
        :param receivers: 邮件接收人列表
        :param cc_receivers: 邮件抄送人列表
        :param attachments: 附件列表
        :return:
        """
        if subject is None or subject == "":
            raise EmailSendException("未指定主题")
        if receivers is None or len(receivers) == 0:
            raise EmailSendException("未指定收件人")
        if html_content is None or html_content == "":
            raise EmailSendException("未指定邮件内容")
        all_receivers = list()
        try:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 添加邮件内容
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            # 添加附件
            if attachments is not None and len(attachments) > 0:
                for attachment in attachments:
                    with open(attachment, mode='rb') as f:
                        part = MIMEApplication(f.read())
                        part.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=('utf-8', '', attachment)
                        )
                        msg.attach(part)

            # 添加邮件头
            msg['to'] = ",".join(receivers)
            all_receivers.extend(receivers)
            if cc_receivers is not None and len(cc_receivers) > 0:
                msg['Cc'] = ",".join(cc_receivers)
                all_receivers.extend(cc_receivers)
            msg['from'] = cls._username
            msg['subject'] = subject
            server = smtplib.SMTP(cls._smtp_server)
            server.starttls()
            server.login(cls._username, cls._password)
            server.sendmail(cls._username, all_receivers, msg.as_string())
            logging.getLogger(__name__).info("邮件发送成功，收件人：%s，抄送：%s", receivers, cc_receivers)
            server.close()
        except smtplib.SMTPException as e:
            logging.getLogger(__name__).error("发送邮件失败，收件人：%s，原因：%s", all_receivers, e)
            raise EmailSendException(e)
