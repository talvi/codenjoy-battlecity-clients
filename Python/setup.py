from distutils.core import setup

setup(name='battlecityclient',
      version='0.1',
      description='BattleCity Dojo game client',
      author='',
      author_email='',
      packages=['battlecityclient'],
      install_requires=['websocket-client', 'click'],
      entry_points={
          'console_scripts': [
              'battlecityclient=battlecityclient.Main:main']})
