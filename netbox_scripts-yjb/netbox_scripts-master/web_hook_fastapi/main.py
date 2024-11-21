from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from deepdiff import DeepDiff
import json
from tools.netmiko_change_interface_enabled import change_interface_enabled
from tools.netmiko_create_interface_sync import sync_device_interface_info
from pprint import pprint

app = FastAPI()
bearer_scheme = HTTPBearer()


@app.get("/", summary='首页摘要', description='首页描述')
async def root():
    return {"message": "Hello World"}


@app.post("/netbox_update_interface_webhook")
async def netbox_update_interface_webhook(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    # 验证 Bearer Token
    if credentials.credentials != "qytangccies":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取请求的 JSON 数据
    payload = await request.json()

    # 提取接口名称
    interface_name = payload.get("data", {}).get("name", "Unknown Interface")
    interface_id = payload.get("data", {}).get("id")
    device_info = payload.get("data", {}).get("device")
    device_name = device_info.get("display", "")
    device_id = device_info.get("id", "")
    # 提取更新前后的快照
    snapshots = payload.get("snapshots", {})
    prechange = snapshots.get("prechange", {})
    postchange = snapshots.get("postchange", {})

    # 使用 DeepDiff 比较差异，忽略 last_updated 字段
    diff = DeepDiff(prechange, postchange, exclude_paths=["root['last_updated']"])

    # 解析差异，构建结果列表
    changes = []
    for change_type, changes_dict in diff.items():
        if change_type == "values_changed":
            for key, change in changes_dict.items():
                # 提取字段名称
                field_name = key.split("root['")[-1].rstrip("']")
                changes.append({
                    "value": field_name,
                    "old_value": change["old_value"],
                    "new_value": change["new_value"]
                })

    # 构建最终结果
    result = {
        "interface_name": interface_name,
        "interface_id": interface_id,
        "device_name": device_name,
        "device_id": int(device_id),
        "changed_values": changes
    }

    # 打印结果
    print(json.dumps(result, indent=4, ensure_ascii=False))
    """
    {
        "interface_name": "10GE1/0/6",
        "interface_id": 20,
        "device_name": "SW_l3-1",
        "device_id": 1,
        "changed_values": [
            {
                "value": "enabled",
                "old_value": true,
                "new_value": false
            }
        ]
    }
    """
    changed_interface_name = result["interface_name"]
    for c in result["changed_values"]:
        if c["value"] == "enabled":
            change_interface_enabled(result["device_id"], changed_interface_name, c["new_value"])
    return {"status": "success"}


@app.post("/netbox_create_interface_webhook")
async def netbox_create_interface_webhook(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    # 验证 Bearer Token
    if credentials.credentials != "qytangccies":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取请求的 JSON 数据
    payload = await request.json()
    pprint(payload)

    # 提取需要的字段
    data = payload.get('data', {})
    device = data.get('device', {})
    device_name = device.get('name')
    device_id = int(device.get('id'))
    interface_name = data.get('name')
    interface_id = data.get('id')

    # 打印提取的数据
    print(f"Device Name: {device_name}, "
          f"Device ID: {device_id}, "
          f"Interface Name: {interface_name}, "
          f"Interface ID: {interface_id}")
    sync_device_interface_info(device_id, interface_name)
    return {"status": "success"}