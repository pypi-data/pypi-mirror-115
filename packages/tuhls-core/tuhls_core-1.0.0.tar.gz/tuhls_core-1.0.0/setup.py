from setuptools import find_namespace_packages, setup

import versioneer

setup(
    name="tuhls_core",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["django"],
    license_files=("LICENSE",),
    url="https://gitlab.com/tuhls/tuhls_core",
    author="Herbert Rusznak (tlb)",
    author_email="herbert.rusznak@gmail.com",
    license="MIT",
    python_requires=">=3.8",
)
