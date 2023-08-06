#setup.py
"""MLFlow Google Cloud Vertex AI integration package."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google_cloud_mlflow",
    version="0.0.1",
    author="Alexey Volkov",
    author_email="alexey.volkov@ark-kun.com",
    description="MLFlow Google Cloud Vertex AI integration package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ark-kun/google_cloud_mlflow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["google-cloud-aiplatform>=1.3.0", "mlflow~=1.19"],
    entry_points={"mlflow.deployments": "google_cloud=google_cloud_mlflow"},
)
