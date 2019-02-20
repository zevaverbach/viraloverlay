from setuptools import setup, find_packages


with open('README.md') as file:
    long_description = file.read()

setup(
    name="viraloverlay",
    version="0.173",
    py_modules=['viraloverlay'],
    url='https://github.com/zevaverbach/viraloverlay',
    install_requires=[
        'Click',
        ],
    include_package_data=True,
    packages=find_packages(),
    description='A CLI to create videos overlaid with text.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    entry_points='''
        [console_scripts]
        vo=viraloverlay.vo:cli
    ''',
        )
