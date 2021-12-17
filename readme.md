# 简单介绍
这是一个用flask+sqlite3实现的一个简单的服务器程序，该服务器
管理有关covid-19各地区感染人数的一些数据，并且提供一些api接
口，通过这些接口可以访问一些经过整理的数据。
# 如何部署
本项目部署在云端的一台centos机器上，使用systemd命令将项目
运行为一个守护进程，service脚本如sendData.service。

环境搭建：
- nginx
- python3
- pip3
- git

在linux服务器端打开终端，输入
```
sudo pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r theSensorEnd/requirements.txt
git clone https://github.com.cnpmjs.org/zhuohuashiyi/theSensorEnd
sudo cp theSensorEnd/sendData.service /etc/systemd/system/sendData.service
sudo cp theSensorEnd/sendData /etc/nginx/sites-enabled/sendData
sudo nginx -s reload
sudo systemctl start sendData
```
即成功部署
这时在本地访问`49.234.26.34:5000/list`（此处替换为你自己的服务器ip地址）
