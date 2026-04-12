from setuptools import setup, find_packages

setup(
    name="debet-scorer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        # "google-generativeai",
        "pandas",
        "openpyxl",
        "python-dotenv",
        "fastapi",
        "uvicorn"
    ],
)