from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'winboost', ###################################
    packages = setuptools.find_packages(),

    version = '2.1',
    license='MIT',
    description = 'WinBoost: Boost your windows system',
    author = 'Smit Parmar, Sanket Jethava, Dhiraj Beri',
    author_email = 'smitraj333@gmail.com, sanketjethava@gmail.com, dhirajberi.official@gmail.com', #Any valing email address
    url = 'https://github.com/cyborg7898/WinBoost', #Github link
    download_url = 'https://github.com/cyborg7898/WinBoost/archive/refs/tags/2.1.tar.gz',#No need to change
    keywords = ['windows', 'boost','optimize','window 10','os','temp cleaner','cleanup','cache cleaner'],
    install_requires=['pywin32'],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    ],
)
