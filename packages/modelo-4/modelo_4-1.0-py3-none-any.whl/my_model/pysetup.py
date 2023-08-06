import setuptools

module_name = input("my_model")
setuptools.setup(
    name=module_name,
    py_modules=[module_name],
)