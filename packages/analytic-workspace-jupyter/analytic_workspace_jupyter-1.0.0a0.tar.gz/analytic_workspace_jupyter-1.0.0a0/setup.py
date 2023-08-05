from setuptools import setup, find_packages


setup(
    name="analytic_workspace_jupyter",
    version="1.0.0a",
    description='Библиотека для подключения JupyterHub к Analytic Workspace',

    author='Analytic Workspace',
    author_email='aw_help@analyticworkspace.ru',
    url='https://analyticworkspace.ru/',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],

    install_requires=[
        "oauthenticator",
        "dockerspawner",
        "python-dotenv",
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    setup_requires=['wheel'],
    python_requires=">=3.8, <4"
)