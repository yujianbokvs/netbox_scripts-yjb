from extras.scripts import Script, StringVar, IntegerVar, BooleanVar, ChoiceVar
from dcim.models import Device, Interface
from ipam.models import VLAN
from dcim.choices import InterfaceTypeChoices, InterfaceModeChoices
from django.core.exceptions import ValidationError


class BulkCreateInterfaces(Script):
    class Meta:
        name = "批量创建Access接口"
        description = "根据设备名称、接口前缀和编号范围批量创建接口"
        commit_default = True

    device_name = StringVar(
        description="设备名称"
    )

    interface_type = ChoiceVar(
        choices=InterfaceTypeChoices.CHOICES,
        description="选择接口类型",
        default=InterfaceTypeChoices.TYPE_10GE_FIXED
    )

    interface_prefix = StringVar(
        description="接口前缀，例如 10GE1/0/"
    )

    interface_enabled = BooleanVar(
        description="接口是否激活",
        default=True
    )

    start_number = IntegerVar(
        description="接口起始编号",
        min_value=1
    )
    end_number = IntegerVar(
        description="接口结束编号",
        min_value=1
    )
    vlan_name = StringVar(
        description="VLAN 名称",
        required=False  # 设置为可选
    )

    def run(self, data, commit):
        device_name = data['device_name']
        interface_prefix = data['interface_prefix']
        start_number = data['start_number']
        end_number = data['end_number']
        vlan_name = data.get('vlan_name')  # 使用 get 方法获取可选字段
        interface_enabled = data['interface_enabled']
        selected_type = data['interface_type']

        # 检查设备是否存在
        try:
            device = Device.objects.get(name=device_name)
        except Device.DoesNotExist:
            self.log_failure(f"设备 {device_name} 不存在！")
            return

        # 如果提供了 VLAN 名称，检查 VLAN 是否存在
        vlan = None
        if vlan_name:
            try:
                vlan = VLAN.objects.get(name=vlan_name)
            except VLAN.DoesNotExist:
                self.log_failure(f"VLAN {vlan_name} 不存在！")
                return

        # 批量创建接口
        for i in range(start_number, end_number + 1):
            interface_name = f"{interface_prefix}{i}"

            # 检查接口是否已存在
            if Interface.objects.filter(device=device, name=interface_name).exists():
                self.log_warning(f"接口 {interface_name} 已存在，跳过。")
                continue

            # 创建接口
            interface = Interface(
                device=device,
                name=interface_name,
                type=selected_type,
                mode=InterfaceModeChoices.MODE_ACCESS,  # 设置为访问模式
                enabled=interface_enabled,
            )

            # 如果提供了 VLAN，则设置 untagged_vlan
            if vlan:
                interface.untagged_vlan = vlan

            try:
                interface.full_clean()  # 验证接口数据
                interface.save()  # 保存到数据库
                vlan_info = f"，绑定 VLAN {vlan_name}" if vlan else ""
                self.log_success(f"成功创建接口 {interface_name}{vlan_info}")
            except ValidationError as e:
                self.log_failure(f"接口 {interface_name} 数据验证失败：{e}")
            except Exception as e:
                self.log_failure(f"创建接口 {interface_name} 时发生错误：{e}")
