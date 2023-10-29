import os
from typing import Literal

import pydantic_settings
from appium.options.android import UiAutomator2Options
from utils import file
from dotenv import load_dotenv


class AppConfig(pydantic_settings.BaseSettings):
    context: Literal['local', 'bstack'] = 'bstack'

    remote_url: str
    app: str
    appWaitActivity: str

    timeout: float = 10.0

    def runs_on_bstack(self):
        return self.app.startswith('bs://')

    def bstack_creds(self):
        return {
            'userName': os.getenv('bstack_userName'),
            'accessKey': os.getenv('bstack_accessKey'),
        }

    def bstack_deviceName_and_platformVersion(self):
        return {
            'deviceName', os.getenv('deviceName'),
            'platformVersion', os.getenv('platformVersion'),
        }

    def to_driver_options(self):
        options = UiAutomator2Options()
        options.set_capability('app', (
            self.app if (self.app.startswith('/') or self.runs_on_bstack())
            else file.abs_path_from_file(self.app)
        ))

        if os.getenv('deviceName'):
            options.set_capability('deviceName', os.getenv('deviceName'))

        if self.appWaitActivity:
            options.set_capability('appWaitActivity', self.appWaitActivity)

        if self.runs_on_bstack():
            print('I runs on bstack')
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


app_config = AppConfig(load_dotenv(f'.env.{AppConfig().context}'))
