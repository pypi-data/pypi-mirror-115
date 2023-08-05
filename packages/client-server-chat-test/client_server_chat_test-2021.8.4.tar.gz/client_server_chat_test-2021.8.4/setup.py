# -*- coding: UTF-8 -*-
import os
import setuptools
 
setuptools.setup(
    name='client_server_chat_test',
    version='2021.08.04',
    keywords='chat',
    description='Client-server chat for test.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'IrrationalDude',
    author_email='painkillerfizz@gmail.com',
    packages=setuptools.find_packages(),
    license='GNU'
)