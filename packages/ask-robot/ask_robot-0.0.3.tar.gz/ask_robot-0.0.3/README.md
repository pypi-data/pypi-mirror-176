
# Ask robot

**using cloud functions to do soma daily things**

# todo

**main todo**

- [ ] update docs to use cloud functions to connect wechat platform
- [ ] delete local operations, like files


# install python


## build from source

```shell
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz
tar -xzvf Python-3.9.7.tar.xz

cd Python-3.9.7
./configure --prefix=/opt/idlepig/apps/python397
make
make altinstall

cd ~/code/venv
/opt/idlepig/apps/python397/bin/python3.9 -m venv wx
source ~/code/venv/wx/bin/activate

cd ~/code/wx
pip install -r requirements.txt
```


## create environment

in centos

```shell
yum install python36u
```

create virtual environment and source

```shell
mkdir -p ~/code/venv
cd ~/code/venv
python3 -m venv wx
source ~/code/venv/wx/bin/activate
```

copy files in this project to server.

firstly, login in your server, then, clone github repository

**todo: push code to github**

```shell
mkdir -p ~/code
cd ~/code
git clone https://github.com/idlepig/wx.git
cd wx
```

install third requirement
```shell
pip install -r requirements.txt
```

## start flask service

you need set actual info for token, aes_key, appid

if you are in plaintext mode, just set token is ok.

```shell
export token=''
export app_id=''
export aes_key=''
export secret=''
export email_from=''
export email_password=''
export email_to=''
```

```shell
sh auto.sh
```

the http://0.0.0.0:8081 will work

# install nginx


```shell
yum install nginx
```

vi /etc/nginx/nginx.conf

```shell
http {
...
upstream idlepig {
    server 127.0.0.1:8081;
  }
...
}
```

vi /etc/nginx/conf.d/default.conf

```shell
server {
    listen 80;
    server_name _;
    location / {
      proxy_pass http://idlepig;
    }
}
```

so, we map 80 port to 8081 port

start nginx

```shell
nginx
```

# for WeChat platform

[article_for_wx.py](article_for_wx.py) has chinese comment is only for WeChat platform

这个脚本是微信公众号里面都脚本文件

# logs file location

/opt/idlewith/logs/output.log
