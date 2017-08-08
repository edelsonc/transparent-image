from cx_Freeze import setup, Executable

setup(
    name="transparent-image",
    version="0.0.1",
    description="A simple commandline application to make image backgrounds transparent",
    executables = [Executable("transparent-image.py")]
)
