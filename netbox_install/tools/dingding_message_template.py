from jinja2 import Template

# --------------------jinja2读取模板---------------------
# 接口激活通知模板
with open("./templates/notification_interface_enabled.template") as f:
    message_interface_enabled_template = Template(f.read())

# 接口更正IP地址通知模板
with open("./templates/notification_interface_ip.template") as f:
    message_interface_ip_template = Template(f.read())