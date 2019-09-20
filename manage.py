#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db


app = create_app()
# app = create_app('product')

# # 初始化manager
manager = Manager(app)

# # 绑定app和数据库，以便进行操作
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
