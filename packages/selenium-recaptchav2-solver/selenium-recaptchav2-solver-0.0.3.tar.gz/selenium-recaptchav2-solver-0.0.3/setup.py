from setuptools import setup, find_packages


setup(
    name='selenium-recaptchav2-solver',
    version='0.0.3',
    license='MIT',
    author='Tomás Perestrelo',
    author_email='tomasperestrelo21@gmail.com',
    packages=find_packages(exclude=('tests*', 'testing*')),
    url='https://github.com/thicccat688/selenium-recaptchav2-solver',
    download_url='https://pypi.org/project/selenium-recaptchav2-solver',
    keywords='python, captcha, speech recognition, selenium, web automation',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    install_requires=['requests'],
)
