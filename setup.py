from setuptools import setup, find_packages

setup(
    name="cryptoenv",
    version="0.1.0",
    description="Cryptoenv is a simple app to handle config files in a secure way.",
    url="https://github.com/savleez/cryptoenv/",
    author="Sergio Velez",
    author_email="svleez@gmail.com",
    packages=[
        "cryptoenv",
        "cryptoenv.core",
        "cryptoenv.crypto",
        "cryptoenv.web",
    ],
    install_requires=[
        "cryptography==41.0.3",
        "fastapi==0.103.0",
        "uvicorn==0.23.2",
        "Jinja2==3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "cryptoenv-web = cryptoenv.web.app:run_web_app",
        ],
    },
)
