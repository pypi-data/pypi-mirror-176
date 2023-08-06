from distutils.core import setup
import setuptools
packages = ['parascore']# 唯一的包名，自己取名
setup(
    name="parascore",
    version="1.0.4",
    author="Lingfeng Shen",
    author_email="lshen30@jh.edu",
    description="Parascore toolkit",
    keywords="Paraphrase metric",
    license="MIT",
    install_requires=[
        "torch>=1.0.0",
        "pandas>=1.0.1",
        "transformers>=3.0.0",
        "numpy",
        "requests",
        "tqdm>=4.31.1",
        "matplotlib",
        "packaging>=20.9",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    packages=packages,
    package_dir={'requests': 'requests'},
)
