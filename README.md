# SHBMS
## Second-Hand Book Management System

基于Django和MySQL的二手图书交易管理系统

运行需要的必要软件包括

-MySQL Server 8.0
-Connector for Python 8.0
-Python 3.7
-Django 3.0
-mysqlclient

Django和mysqlclient可通过pip安装

>	python -m pip install django

>	python -m pip install mysqlclient

需要在MySQL中创建名为'shbms_db'的数据库，创建名为'SHBMS_USER'的用户，此用户有访问'shbms_db'数据库的权限，'SHBMS_USER'用户所设的密码需要在./SHBMS/settings.py文件中修改
