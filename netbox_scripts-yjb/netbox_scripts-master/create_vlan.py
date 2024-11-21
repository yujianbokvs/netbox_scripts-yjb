from extras.scripts import Script, StringVar, IntegerVar
from ipam.models import VLAN
from ipam.choices import VLANStatusChoices
from django.core.exceptions import ValidationError

class CreateVLAN(Script):
    class Meta:
        name = "创建 VLAN"
        description = "创建一个新的 VLAN"
        commit_default = True  # 默认提交数据库更改

    vlan_id = IntegerVar(
        description="VLAN ID（1-4094）",
        min_value=1,
        max_value=4094
    )
    vlan_name = StringVar(
        description="VLAN 名称"
    )

    def run(self, data, commit):
        vlan_id = data['vlan_id']
        vlan_name = data['vlan_name']

        # 检查 VLAN ID 是否已存在
        if VLAN.objects.filter(vid=vlan_id).exists():
            self.log_failure(f"VLAN ID {vlan_id} 已存在。")
            return

        # 创建新的 VLAN
        vlan = VLAN(
            vid=vlan_id,
            name=vlan_name,
            status=VLANStatusChoices.STATUS_ACTIVE
        )

        try:
            vlan.full_clean()  # 验证数据
            vlan.save()        # 保存到数据库
            self.log_success(f"成功创建 VLAN：ID={vlan_id}, 名称={vlan_name}")
        except ValidationError as e:
            self.log_failure(f"数据验证失败：{e}")
        except Exception as e:
            self.log_failure(f"保存 VLAN 时发生错误：{e}")
