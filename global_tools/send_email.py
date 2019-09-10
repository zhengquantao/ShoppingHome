from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
import random
import string

# mail_server = 'smtp.qq.com'


def get_mail_server(sender):
    key = sender[sender.index('@')+1:]
    return "smtp." + key


def sender_email(receiver):
    mail_server = 'smtp.qq.com'
    port = '25'
    sender = '1483906080@qq.com'
    sender_pass_code = 'cewotngmphloijab'
    mail_msg = random.sample(string.digits, 5)
    check_email_code = ''  # 要发送的内容
    for item in mail_msg:
        check_email_code += str(item)
    msg = MIMEText(check_email_code, 'plain', 'utf-8')  # 正文 ， MIME的subtype纯文本， 编码
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header('From zhengquanTao person computer', 'utf-8')
    try:
        server = SMTP(mail_server, port)
        # server.set_debuglevel(1)  # 打印出SMTP服务器的交互信息
        server.login(sender, sender_pass_code)
        server.sendmail(sender, (receiver), msg.as_string())  # 发送者, 接收人(可以是多个人，用list群发), 正文转成str
        server.quit()
        return check_email_code
    except:
        server.quit()
        return