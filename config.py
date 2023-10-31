import os
from typing import Literal

import pydantic_settings
from appium.options.android import UiAutomator2Options
from utils import file
from dotenv import load_dotenv


class AppConfig(pydantic_settings.BaseSettings):
    context: Literal['local', 'bstack'] = 'local'

    remote_url: str
    app: str
    appWaitActivity: str
    timeout: float = 10.0

    bstack_userName: str = ''
    bstack_accessKey: str = ''
    deviceName: str = ''
    platformVersion: str = ''

    def runs_on_bstack(self):
        return self.app.startswith('bs://')

    def bstack_creds(self):
        return {
            'userName': self.bstack_userName,
            'accessKey': self.bstack_accessKey,
        }

    def bstack_deviceName_and_platformVersion(self):
        load_dotenv(file.abs_path_from_file('.env.credentials'))
        return {
            'deviceName', self.android_deviceName,
            'platformVersion', self.platformVersion,
        }

    def to_driver_options(self):
        options = UiAutomator2Options()
        options.set_capability('app', (
            self.app if (self.app.startswith('/') or self.runs_on_bstack())
            else file.abs_path_from_file(self.app)
        ))

        if self.deviceName:
            options.set_capability('deviceName', self.deviceName)

        if self.appWaitActivity:
            options.set_capability('appWaitActivity', self.appWaitActivity)

        if self.runs_on_bstack():
            options.load_capabilities({
                **self.bstack_deviceName_and_platformVersion,

                'bstack:options': {
                    'projectName': 'First Python project',
                    'buildName': 'browserstack-android-build-1',
                    'sessionName': 'BStack first_android_test',

                    **self.bstack_creds
                }
            })

        return options


path = file.abs_path_from_file(f'.env.{AppConfig().context}')
app_config = AppConfig(_env_file=path)
