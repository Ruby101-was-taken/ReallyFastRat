import cx_Freeze

executables = [cx_Freeze.Executable("Platforme.py", icon="icon.ico", base = "Win32GUI")]

includedFiles=["player.png", "icon.png", "logo/", "objects/", "levels/", "player/", "tilemap/", "tilemap.png", "font.ttf", "sound/", "extraControllers.py"]

packages=["os", "pygame", "csv", "random", "math"]

cx_Freeze.setup(
    name="Really Fast Rat",
    options={"build_exe": {"packages":packages,
                           "include_files":includedFiles}},
    executables = executables

    )

#python.exe setup.py build