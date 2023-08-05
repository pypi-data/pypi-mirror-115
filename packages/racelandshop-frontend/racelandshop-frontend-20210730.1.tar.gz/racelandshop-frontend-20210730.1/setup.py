from setuptools import setup, find_packages

setup(
    name="racelandshop-frontend",
    version="20210730.1",
    description="The RACELANDSHOP frontend",
    url="https://github.com/racelandshop/frontend",
    author="Joakim Sorensen",
    author_email="geral@automacaoraceland.pt",
    packages=find_packages(include=["racelandshop_frontend", "racelandshop_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
