from setuptools import setup

setup(
    name='pytelebirr',
    version='0.2.0',
    packages=['pytelebirr', 'pytelebirr.errors'],
    url='https://github.com/telebirrapi/pytelebirr',
    license='GPL-3.0',
    author='wizkiye',
    author_email='wizkiye@gmail.com',
    description='Telebirr with python ',
    install_requires=[
        "asyncio",
        "requests",
        "websocket-client"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
