---
title: docker命令
date: 2025-11-13 14:55:05
tags:
---

docker.hub.com



## 镜像相关命令

```bash
# 先拿root权限
su -i
# 如果用的是su root，这样进入的 root shell 没有继承完整的环境变量（尤其是 XDG_RUNTIME_DIR、PATH），所以 docker CLI 无法正确找到 /var/run/docker.sock。
su root
```

运行了sudo -i之后，~代表的就是/root，而不是/home/daomo了。

```bash
$ sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        8.2       466e5b1da2ef   4 weeks ago   137MB
redis        latest    466e5b1da2ef   4 weeks ago   137MB

```



```bash
# 查看镜像
docker images

# 从网络搜索镜像
docker search redis

# 拉取镜像
docker pull redis
docker pull redis:8.2

# 删除本地镜像
docker rmi IMAGE ID

# 查看所有镜像ID
docker images -q

# 删除本地所有镜像
docker rmi `docker images -q`
```



## 容器相关命令

Linux称为宿主机，容器运行在宿主机上。

-it，交互式容器，exit关闭。

-id，守护式容器，需要使用exec进入容器，exit不会关闭。

```bash
# 创建并启动一个新的容器
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
-d: 后台运行容器并返回容器 ID。
-i: 保持运行，即使没有客户端连接也不会关闭。
-t: 交互式容器，给容器分配一个伪终端。
--name: 给容器指定一个名称。
-d: 后台运行容器并返回容器 ID。

root@daomo-VMware-Virtual-Platform:~# docker run -it --name c1 centos:7 /bin/bash
[root@59a1aed61352 /]# 

root@daomo-VMware-Virtual-Platform:~# docker run -id --name c2 centos:7
a52e95908b085f463fd6fec90c981bb66ad22e857fe0f06fa9afba4419461a66
root@daomo-VMware-Virtual-Platform:~# 


# 退出容器
exit 

# 查看容器
# 查看正在运行的容器
docker ps	
# 查看所有的容器
docker ps -a

CONTAINER ID   IMAGE      COMMAND       CREATED          STATUS                     PORTS     NAMES
a52e95908b08   centos:7   "/bin/bash"   23 seconds ago   Up 22 seconds                        c2
59a1aed61352   centos:7   "/bin/bash"   6 minutes ago    Exited (0) 4 minutes ago             c1



# 在运行的容器中执行命令
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

-d: 在后台运行命令
-i: 保持标准输入打开
-t: 分配一个伪终端

docker exec -it c2 /bin/bash
```



```bash
# 关闭容器
docker stop c2
# 启动容器
docker start c2
# 删除容器
docker rm 容器ID/容器名称
docker rm c1
# 删除所有容器
docker rm `docker ps -aq`
# 查看容器信息
docker inspect c2

```





# Docker容器的数据卷

{% asset_img image-20251105000548805.png %}

```bash
docker run ... -v 宿主机目录（文件）:容器内目录（文件）...
```

注意事项：

1. 目录必须是绝对路径
2. 如果目录不存在，会自动创建
3. 可以挂载多个数据卷

```bash
docker run -it --name c1 -v /root/data:/root/data_container centos:7 /bin/bash

docker run it --name c2 \
-v ~/data2:/root/data2 \
-v ~/data3:/root/data3 \
centos:7

```

### 数据卷容器

多容器进行数据交换

1. 多个容器挂载同一个数据卷
2. 数据卷容器



{% asset_img image-20251105001301589.png %}

{% asset_img image-20251105001318234.png %}



{% asset_img image-20251105001656823.png %}

### **数据卷小结**

1. 数据卷概念
   - 宿主机的一个目录或文件

2. 数据卷作用

   - 容器数据持久化


   - 客户端和容器数据交换


   - 容器间数据交换


3. 数据卷容器

   - 创建一个容器，挂载一个目录，让其他容器继承自该容器( --volume-from )。


   - 通过简单方式实现数据卷配置

## Dockerfile

### Docker镜像原理

{% asset_img image-20251105004936667.png %}

{% asset_img image-20251105005036124.png %}

{% asset_img image-20251105005049586.png %}





### Dockerfile概念及作用



### Dockerfile关键字





### 案例

