from setuptools import setup

setup(name='upmcore',
      version='0.4',
      description='A universal package manager',
      url='http://github.com/apollyon9/upm',
      author='Apollyon9/Sakurai07',
      author_email='blzzardst0rm@gmail.com',
      license='MIT',
      packages=['upmcore',"upmcore.core.python","upmcore.core.njs","upmcore.guess","upmcore.index.python","upmcore.index.njs"],
      zip_safe=False)