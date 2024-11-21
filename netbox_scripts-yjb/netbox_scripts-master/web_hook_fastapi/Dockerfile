FROM        rockylinux:9.3.20231119
USER        root
RUN         /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN         yum install -y python3.11 python3.11-devel python3.11-pip gcc openssh-clients git
RUN         mkdir /qytangfastapi
WORKDIR     /qytangfastapi
COPY        requirements.txt .
RUN         pip3.11 install -r requirements.txt
COPY        main.py .
COPY        tools ./tools
CMD         uvicorn main:app --host 0.0.0.0 --port=8066 --workers 10