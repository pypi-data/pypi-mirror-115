from setuptools import setup, find_packages

setup(

    name='iTesting20210802',

    version='0.1',

    description='This is a demo framework',

    author='wuyi',

    author_email='testertalk@outlook.com',

    zip_safe=False,

    include_package_data=True,

    packages=find_packages(),

    license='MIT',

    url='https://www.helloqa.com',

    entry_points={

        'console_scripts': [

            'iTesting = iTesting.main:main'

        ]

    }

)
