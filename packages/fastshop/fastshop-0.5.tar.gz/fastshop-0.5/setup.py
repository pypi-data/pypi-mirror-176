import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastshop",
    version="0.5",
    author="fengchuan",
    author_email="fengchuanhn@gmail.com",
    description="fastshop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fengchuan1021",
    #packages=['fastshop/*'],
    packages=setuptools.find_packages(),
    package_dir={'fastshop':'fastshop'},
    package_data={'fastshop':['*.*','Models/*']},
    install_requires=['sqlalchemy','pydantic','orjson','XTTOOLS','python-multipart','alembic','elasticsearch-dsl','elasticsearch','celery-redbeat','azure-storage-blob','uvicorn','typing_extensions','typer','sse-starlette','redis',
                      'python-jose','python-dotenv','PyMySQL','passlib','fastapi==0.82.0','fastapi-code-generator==0.3.5','aiohttp','alembic-autogen-check','celery','sqlalchemy2-stubs','websockets'
                      ],
    entry_points={
        'console_scripts': [
            'fastshop = fastshop.fastshop:main'
        ]
    },

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)