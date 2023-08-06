from setuptools import setup

setup(name='upmcore',
      version='0.3',
      description='A universal package manager',
      url='http://github.com/apollyon9/upm',
      author='Apollyon9/Sakurai07',
      author_email='blzzardst0rm@gmail.com',
      license='MIT',
      packages=['upmcore',"upmcore.core","upmcore.guess","upmcore.index"],
      zip_safe=False)