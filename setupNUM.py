import cx_Freeze

executables = [cx_Freeze.Executable("getButtonNum.py", icon="icon.ico", base = "Win32GUI")]

includedFiles=[]

packages=["sys", "pygame"]

cx_Freeze.setup(
    name="TEST",
    options={"build_exe": {"packages":packages,
                           "include_files":includedFiles}},
    executables = executables

    )

#python.exe setupNUM.py build