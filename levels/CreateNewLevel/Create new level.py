worldX, worldY = input("Enter the world X: "), input("Enter the world Y: ")

import shutil, os

print("Copying level tmx")

src = "sample.tmx"
dest = f"../tmx/{worldX}-{worldY}.tmx"

shutil.copyfile(src, dest)


print("Copying level json")

src = "sample.json"
dest = f"../levels/{worldX}-{worldY}.json"

shutil.copyfile(src, dest)

print("Copying level info")

src = "sampleInfo.json"
dest = f"../levelInfo/{worldX}-{worldY}.json"

shutil.copyfile(src, dest)

