import django
django.setup()
from django.utils.text import slugify
from extras.scripts import *

from dcim.models import Interface
from django.db.models.fields.related import RelatedField

def get_set_attributes(instance):
    """
    获取实例中已设置值的属性。
    """
    set_attributes = {}
    unset_attributes = {}

    for attr in dir(instance):
        # 排除内置属性和方法
        if attr.startswith('_') or callable(getattr(instance, attr, None)):
            continue

        try:
            value = getattr(instance, attr)
            # 过滤掉 RelatedManager 类的字段（如 ManyToMany 关系）
            if isinstance(value, RelatedField):
                continue

            if value is not None:
                set_attributes[attr] = value
            else:
                unset_attributes[attr] = None
        except Exception:
            # 某些属性可能会引发错误，安全忽略
            pass

    return set_attributes, unset_attributes


# 示例用法
for i in Interface.objects.all():  # 获取一个 Interface 实例
    set_attrs, unset_attrs = get_set_attributes(i)

    print("已设置的属性:")
    for key, value in set_attrs.items():
        print(f"{key}: {value}")

    print("\n未设置的属性:")
    for key in unset_attrs.keys():
        print(key)
