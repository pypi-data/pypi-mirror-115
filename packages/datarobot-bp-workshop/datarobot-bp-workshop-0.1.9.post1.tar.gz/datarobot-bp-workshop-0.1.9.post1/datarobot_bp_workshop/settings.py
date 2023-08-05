"""
Copyright 2021 DataRobot, Inc. and its affiliates.

All rights reserved.

DataRobot, Inc. Confidential.

This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.

The copyright notice above does not evidence any actual or intended publication of such source code.

Released under the terms of DataRobot Tool and Utility Agreement.
"""

import os


class Settings(object):
    """ Introduce concept of settings """

    force_no_color = False
    force_dev_mode = False

    defaults = {
        "BLUEPRINT_WORKSHOP_DEV_MODE": False,
        "BLUEPRINT_WORKSHOP_ALLOW_COLOR": True,
    }

    @property
    def is_dev_mode(self):
        return self.force_dev_mode or self.get_env_value("BLUEPRINT_WORKSHOP_DEV_MODE")

    @property
    def allow_color(self):
        if self.force_no_color:
            return False
        return self.get_env_value("BLUEPRINT_WORKSHOP_ALLOW_COLOR")

    @classmethod
    def get_env_value(cls, setting):
        return os.environ.get(setting, cls.defaults[setting])
