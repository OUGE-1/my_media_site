# My Media Site

这是一个基于 Django 框架开发的媒体资源管理网站，用于展示和管理视频、音频集合。

## 项目简介

My Media Site 提供了一个简洁的媒体资源管理平台，支持视频和音频内容的分类展示。用户可以通过网页浏览不同的媒体集合，查看视频和音频的详细信息。

## 技术栈

- **后端**: Django 4.x
- **前端**: HTML/CSS/JavaScript
- **数据库**: SQLite（默认）

## 项目结构

```
my_media_site/
├── manage.py              # Django 管理脚本
├── my_media_site/         # 项目主目录
│   ├── settings.py        # 项目配置
│   ├── urls.py            # URL 路由配置
│   ├── wsgi.py            # WSGI 配置
│   └── asgi.py            # ASGI 配置
└── player/                # 媒体播放应用
    ├── models.py          # 数据模型
    ├── views.py           # 视图函数
    ├── urls.py            # 应用路由
    ├── admin.py           # 管理后台配置
    └── templates/         # 模板文件
```

## 数据模型

项目包含以下核心模型：

- **Collection**: 媒体集合，用于对视频和音频进行分组管理
- **Video**: 视频资源，存储视频标题、描述、文件路径等信息
- **Audio**: 音频资源，存储音频标题、描述、文件路径等信息

## 功能特性

- 媒体集合分类管理
- 视频资源展示
- 音频资源展示
- Django 管理后台集成
- 响应式网页设计

## 快速开始

### 环境要求

- Python 3.8+
- Django 4.x

### 安装步骤

1. 克隆项目到本地

```bash
git clone https://gitee.com/xiaotu20/my_media_site.git
cd my_media_site
```

2. 创建虚拟环境（可选）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖

```bash
pip install django
```

4. 运行数据库迁移

```bash
python manage.py migrate
```

5. 创建管理员账户

```bash
python manage.py createsuperuser
```

6. 启动开发服务器

```bash
python manage.py runserver
```

7. 访问应用

- 网站主页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/

## 使用说明

### 管理后台

1. 登录管理后台创建 Collection（集合）
2. 在集合中添加 Video（视频）和 Audio（音频）资源
3. 填写相关标题、描述和文件路径

### 前端展示

访问网站主页即可查看所有媒体资源和集合列表。

## 开发指南

### 运行测试

```bash
python manage.py test
```

### 创建应用

如需扩展功能，可以创建新的 Django 应用：

```bash
python manage.py startapp new_app
```

## 许可证

本项目仅供学习参考使用。