# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrunjvm']

package_data = \
{'': ['*'], 'pyrunjvm': ['config/tomcat/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['pyrunjvm = pyrunjvm:cli.main']}

setup_kwargs = {
    'name': 'pyrunjvm',
    'version': '0.5.1',
    'description': '',
    'long_description': '# pyrunjvm\n以 debug 模式启动 jvm， 并启动常见应用服务，目前支持通过 tomcat 容器来启动 exploded war , 下一步要支持启动多个 spring boot flat jar 包\n\n## 原因\n  在 intellij/Eclispe 等 IDE 里可以很方便通过 tomcat 容器来启动服务, 这样就可以很方便调试；\n但这样做法有个缺点，tomcat 服务运行时间一长，就会影响到 IDE 的使用，出现 IDE 卡顿等，严重影响代码开发。\n\n所以开发了这个工具，可以在命令行里方便启动 tomcat 服务，需要调试时，可以在 IDE 里使用 remote debug 来调试\n\n\n## 使用\n\n### 安装\n `TODO`\n\n### 配置文件\n  配置文件 `.pyrunjvm.toml` 定义了如何运行服务以及默认环境变量,\n  因为每个用户的工具路径或者端口都不一样的，pyrunjvm 是通过定义环境变量来更改这些配置\n  可在系统的环境变量里定义，或者在当前目录下建立配置文件 `.env` 来定义具体的环境变量\n\n  在项目的根目录下新建文件 `.pyrunjvm.toml`, 下面是一个配置文件的例子\n  ```\napp_type = "tomcat"\n\n[build]\nclear_cmds = []\nbuild_cmds = [\n    "${GRADLE_BIN} explodedWar",\n]\n\n[tomcat]\nproxy.enable = true\n\n\n[[projects]]\npath="test-mgr"\ncontext_path = "test-mgr"\nexploded_war_path = "${WORK_DIR}/test-mgr/build/exploded"\n\n[[projects]]\npath="test-api"\ncontext_path = "test-api"\nexploded_war_path = "${WORK_DIR}/test-api/build/exploded"\n\n# default env\n[env]\nJVM_DEBUG_PORT = "50899"\nTOMCAT_PORT = "8080"\nSHUTDOWN_PORT =  "8005"\nREDIRECT_PORT = "8443"\nAJP_PORT = "8009"\nGRADLE_BIN = "gradle"\nJAVA_BIN = "java"\n\n  ```\n\n  环境变量配置文件 `.env` 例子\n\n  ```\nJVM_DEBUG_PORT = 50859\nTOMCAT_PORT = 8080\n\nGRADLE_BIN = ".\\gradlew.bat"\nTOMCAT_HOME="G:\\\\devel\\\\apache-tomcat-8.5.16"\n\nJAVA_BIN="C:\\\\Users\\\\riag\\\\.jabba\\\\jdk\\\\zulu@1.8\\\\bin\\\\java.exe"\n \n  ```\n\n  ### 运行\n  在命令行里 cd 到项目的根目录下，然后直接执行 `pyrunjvm` 命令就可以\n',
    'author': 'riag',
    'author_email': 'riag@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
