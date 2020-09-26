import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db =  sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据
    return g.db


def close_db(e=None):
    db=g.pop('db', None)

    if db is not None:
        db.close()



# 在 db.py 文件中添加 Python 函数，用于运行这个 SQL 命令：
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new talbes."""
    init_db()
    click.echo('Initialized the databases.')


# 写一个函数，把应用作为参数，在函数中进行注册
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)