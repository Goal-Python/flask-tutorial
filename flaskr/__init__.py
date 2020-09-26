import os

from flask import Flask

# __init__.py 有两个作用：一是包含应用工厂；二是 告诉 Python flaskr 文件夹应当视作为一个包


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # print(app.config['DATABASE'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        # print(app.instance_path)
        # Result: /Users/dangwg/Documents/Project/flask-tutorial/flaskr/instance
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!', 400

    # 在工厂中导入并调用 init-db 命令行。调用 init_db() 函数 用于运行 SQL 命令：
    from . import db
    db.init_app(app)

    # 注册认证蓝图：认证蓝图将包括注册新用户、登录和注销视图。
    from . import auth
    app.register_blueprint(auth.bp)

    # 注册博客蓝图：
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

# a=create_app()
# print(a.instance_path)
