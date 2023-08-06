from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name='django-riometrics-middleware',
    version='1.0.2',
    description='Rapyuta.io Metrics Django Middleware',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Rapyuta Robotics',
    author_email='opensource@rapyuta-robotics.com',
    packages=['rio_metrics'],
    python_requires='>=3.6',
    license='Apache 2.0',
    install_requires=[
        'requests>=2.20.0',
        'urllib3>=1.23',
        'pytelegraf==0.3.3',
        'setuptools'
    ],
)
