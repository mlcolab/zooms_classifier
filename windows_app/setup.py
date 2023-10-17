from cx_Freeze import setup, Executable

setup(
    name="AI_ZooMS",
    version="0.0.1",
    description="Find homininis with AI",
    executables=[Executable("src/main.py")]
)
