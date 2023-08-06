import setuptools

setuptools.setup(
    name="tdrawer",
    version="0.0.1",
    author="Terry Qi",
    description="A simple OpenGL drawer",
    packages=setuptools.find_packages('tdrawer'),
    include_package_data=True,
    python_requires=">=3.7",
    py_modules=["tdrawer"],
    package_dir={'': 'tdrawer'},
    install_requires=['cffi'],

)
