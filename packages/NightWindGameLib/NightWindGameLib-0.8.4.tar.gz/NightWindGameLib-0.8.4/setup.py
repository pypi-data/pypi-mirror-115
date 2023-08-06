import setuptools as st

st.setup(
    name="NightWindGameLib",
    author="Nova_NightWind0311",
    version="0.8.4",
    author_email="nova_nightwind0311@qq.com",
    description="Some little games",
    url="https://github.com",
    include_package_data=True,
    packages=st.find_packages(),
    install_requires=[
        "arcade >= 2.5.5",
        "pygame >= 2.0.1",
        "PySide2 >= 5.14",
        "sympy >= 1.7.0",
        "Pillow >= 8.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
