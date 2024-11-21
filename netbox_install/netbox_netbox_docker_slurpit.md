### 参考文章
```shell
https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins
https://github.com/netbox-community/netbox-napalm
```

### 版本对应
```
https://github.com/netbox-community/netbox              # netbox版本 v4.0.8 （源码）
https://github.com/netbox-community/netbox-docker       # netbox-docker版本 2.9.1 （构建容器的源码）

# netbox-docker镜像版本里边有netbox版本 与 netbox-docker版本对应
https://hub.docker.com/r/netboxcommunity/netbox/tags    # netbox-docker镜像版本 v4.0.8-2.9.1 （构建好的镜像）
```

### https://github.com/netbox-community/netbox-napalm 这个位置可以看到napalm插件的兼容版本

| NetBox Version	 | Plugin Version |
|-----------------|----------------|
| 3.5	            | 0.1.0          |
| 3.5.8	          | 0.1.4          |
| 3.6.0	          | 0.1.5          |
| < 3.7.6	        | 0.1.7          |
| >= 4.0.2	       | 0.2.1          |


### 下载代码, 要与Dockerfile这个部分"FROM netboxcommunity/netbox:v4.0.8-2.9.1"匹配
```shell
cd /
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd /netbox-docker/
git checkout tags/3.0.2

```

###plugin_requirements.txt (pip需要安装的模块),使用下面两个链接查版本对应关系
### https://github.com/netbox-community/netbox-topology-views
### https://github.com/netbox-community/netbox-napalm-plugin
```shell
cat > /netbox-docker/plugin_requirements.txt <<'EOF'
netbox-napalm-plugin==v0.3.0
netbox-topology-views==v4.1.0
slurpit_netbox== 1.0.33
EOF

```

### configuration.py
```shell
vim /netbox-docker/configuration/configuration.py

~~~~ 添加如下内容~~~~
PLUGINS = [
    'netbox_napalm_plugin',
    'netbox_topology_views',
    'slurpit_netbox'
]

PLUGINS_CONFIG = {
    'netbox_napalm_plugin': {
        'NAPALM_USERNAME': 'admin',
        'NAPALM_PASSWORD': 'Cisc0123',
    },
    'netbox_topology_views': {
        'static_image_directory': 'netbox_topology_views/img',
        'allow_coordinates_saving': True,
        'always_save_coordinates': True
    }
}

```

### Dockerfile-Plugins, 要与"git checkout tags/2.8.0"这个部分匹配
### netbox版本必须大于v3.5, 否则不支持plugin
```shell
cat > /netbox-docker/Dockerfile-Plugins <<'EOF'
FROM netboxcommunity/netbox:v4.1-3.0.2

COPY ./plugin_requirements.txt /
RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /plugin_requirements.txt

# These lines are only required if your plugin has its own static files.
COPY configuration/configuration.py /etc/netbox/config/configuration.py
COPY configuration/plugins.py /etc/netbox/config/plugins.py
RUN SECRET_KEY="dummydummydummydummydummydummydummydummydummydummy" /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py collectstatic --no-input
EOF

```

### docker-compose.override.yml
```shell
cat > /netbox-docker/docker-compose.override.yml <<'EOF'
services:
  netbox:
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
    image: netbox:latest-plugins
  
  netbox-worker:
    image: netbox:latest-plugins
    build:
      context: .
      dockerfile: Dockerfile-Plugins

  netbox-housekeeping:
    image: netbox:latest-plugins
    build:
      context: .
      dockerfile: Dockerfile-Plugins
EOF

```
### 删除老的volume
```shell
docker volume ls --format "{{.Name}}" | grep "netbox-docker" | xargs -r docker volume rm
docker compose down -v  如果是之前安装过netbox 需要删除老的数据

```

### 拉起容器
```shell
docker compose build --no-cache
docker compose up -d
~~~启动要多等等, 等到netbox-docker-netbox-1这个容器healthy~~~

~~~ 可以用下面的命令看看容器内部的日志 ~~~
docker logs netbox-docker-netbox-1

```

### 创建超级用户
```shell
[root@jiaozhu-rocky netbox-docker]# docker exec -it netbox-docker-netbox-1 ./manage.py createsuperuser

🧬 loaded config '/etc/netbox/config/configuration.py'
🧬 loaded config '/etc/netbox/config/extra.py'
🧬 loaded config '/etc/netbox/config/logging.py'
🧬 loaded config '/etc/netbox/config/plugins.py'

Username (leave blank to use 'unit'): admin
Email address: admin@qytang.com
Password: Cisc0123
Password (again): Cisc0123
Superuser created successfully.


```

### 拷贝数据库文件到容器内
```shell
docker cp /netdevops2023/netbox_install/netbox_db_file/ipam_backup.json netbox-docker-netbox-1:/tmp/ipam_backup.json
docker cp /netdevops2023/netbox_install/netbox_db_file/dcim_backup.json netbox-docker-netbox-1:/tmp/dcim_backup.json
docker cp /netdevops2023/netbox_install/netbox_db_file/netbox_napalm_plugin_backup.json netbox-docker-netbox-1:/tmp/netbox_napalm_plugin_backup.json
docker cp /netdevops2023/netbox_install/netbox_db_file/netbox_topology_views_backup.json netbox-docker-netbox-1:/tmp/netbox_topology_views_backup.json
docker cp /netdevops2023/netbox_install/netbox_db_file/users_backup.json netbox-docker-netbox-1:/tmp/users_backup.json
docker cp /netdevops2023/netbox_install/netbox_db_file/extras_backup.json netbox-docker-netbox-1:/tmp/extras_backup.json

```
### 恢复数据库， 需要严格按照下面的顺序
```shell
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/ipam_backup.json
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/users_backup.json
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/extras_backup.json
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/dcim_backup.json
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/netbox_napalm_plugin_backup.json
docker exec -it netbox-docker-netbox-1 /opt/netbox/netbox/manage.py loaddata /tmp/netbox_topology_views_backup.json

```

### 导出数据库
```shell
~~~ 容器内 ~~~
/opt/netbox/netbox/manage.py dumpdata dcim --output /tmp/dcim_backup.json
/opt/netbox/netbox/manage.py dumpdata ipam --output /tmp/ipam_backup.json
/opt/netbox/netbox/manage.py dumpdata netbox_napalm_plugin --output /tmp/netbox_napalm_plugin_backup.json
/opt/netbox/netbox/manage.py dumpdata netbox_topology_views --output /tmp/netbox_topology_views_backup.json
/opt/netbox/netbox/manage.py dumpdata users --output /tmp/users_backup.json
/opt/netbox/netbox/manage.py dumpdata extras --output /tmp/extras_backup.json

~~~ 容器外 ~~~
docker cp netbox-docker-netbox-1:/tmp/dcim_backup.json ~/dcim_backup.json
docker cp netbox-docker-netbox-1:/tmp/ipam_backup.json ~/ipam_backup.json
docker cp netbox-docker-netbox-1:/tmp/netbox_napalm_plugin_backup.json ~/netbox_napalm_plugin_backup.json
docker cp netbox-docker-netbox-1:/tmp/netbox_topology_views_backup.json ~/netbox_topology_views_backup.json
docker cp netbox-docker-netbox-1:/tmp/users_backup.json ~/users_backup.json
docker cp netbox-docker-netbox-1:/tmp/extras_backup.json ~/extras_backup.json
```

### 恢复数据只需要再配置Plugins --- Napalm即可

### 配置C8Kv1 LLDP
```shell
lldp run
interface gigabitEthernet 3
  lldp receive
  lldp transmit

```

### 配置C8Kv2 LLDP
```shell
lldp run 
interface gigabitEthernet 2
  lldp receive
  lldp transmit

```
