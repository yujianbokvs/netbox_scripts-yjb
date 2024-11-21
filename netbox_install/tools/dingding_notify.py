from dingtalkchatbot.chatbot import DingtalkChatbot
from netbox_install.netbox_0_login_info import qyt_webhook


# dingding组群发MarkDown
def send_group_msg(webhook, title, text, is_at_all=True):
    dingdingbot = DingtalkChatbot(webhook)
    dingdingbot.send_markdown(title=title, text=text, is_at_all=is_at_all)


# 封装了一层, 成功和失败的判断
def notify_team(message):
    try:
        send_group_msg(qyt_webhook, title='QYT', text=message)
        return True

    except Exception as e:
        print("Unable to send message")
        return False


# 最终封装, 提供fail_list清单, 模板, 就能发出钉钉群通知
def fail_notification(fail_list, message_template, **kwargs):
    if len(fail_list) > 0 or kwargs:
        message = message_template.render(
            failed=fail_list,
            **kwargs
        )
        m = notify_team(message)
        return m


if __name__ == "__main__":
    send_group_msg(qyt_webhook, 'title', 'text')
