import cx_Freeze

executables = [cx_Freeze.Executable("Platforme.py", icon="icon.ico", base = "Win32GUI")]

includedFiles=["player.png", "icon.png", "tilemap.png", "font.ttf",
               "logo/", "objects/", "levels/", "player/", "tilemap/", "sound/", "backgrounds/", "ui/", "entities",
               "extraControllers.py", "colours.py", "jsonParse.py", "resources.py", "sign.py", "tiles.py", "entity.py", "settings.py", "profiler.py"
               ]

packages=["os", "pygame", "csv", "random", "math", "time"]

cx_Freeze.setup(
    name="Really Fast Rat",
    options={"build_exe": {"packages":packages,
                           "include_files":includedFiles}},
    executables = executables

    )

#python.exe setup.py build