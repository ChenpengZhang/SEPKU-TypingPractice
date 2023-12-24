# SEPKU-TypingPractice
* 北京大学地球与空间科学学院2023年软件工程大作业。一个线上的打字练习软件，主要基于RESTful API, Agile Developing, SaaS. 
* 线上运行
    * <b>现在已经支持线上运行！！！（好耶）直接访问网站即可： </b>
    ```
    https://sepku-typingpractice.onrender.com
    ```
* 本地运行 
    * 本地运行此软件需要提前安装虚拟环境维护系统pipenv，请提前检查你是否在电脑上安装了pip python包管理软件。
    ```bash
    $ which pip
    $ pip install pipenv
    ```
    * 安装完毕后，依次运行：
    ```bash
    $ pipenv install -r requirements.txt
    $ pipenv run gunicorn app:app
    ```
    * 并在本地浏览器访问：
    ```http
    http://127.0.0.1:5000
    ```
    (也可能是其它端口，具体可以查看你的命令行提示)
* 联系开发人员：QQ：1352877410