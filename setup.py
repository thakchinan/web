from setuptools import setup, find_packages

setup(
    name="traffic-predictor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "joblib==1.3.2",
        "scikit-learn==1.6.1",
        "jinja2==3.1.2",
        "numpy==1.26.4",
        "pandas==2.1.3",
        "openpyxl==3.1.2",
        "python-multipart==0.0.6",
        "gunicorn==21.2.0",
    ],
    python_requires=">=3.10",
)
