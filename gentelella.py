#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
from os.path import abspath, dirname

from flask_migrate import Migrate

from app import create_app, db
from configs.config import config_dict

sys.path.insert(0, abspath(dirname(__file__)))

get_config_mode = os.environ.get("GENTELELLA_MODE", "Debug")
config_mode = config_dict[get_config_mode.capitalize()]

app = create_app(config_mode)
Migrate(app, db)

if __name__ == "__main__":
    app.run(port=8000)
