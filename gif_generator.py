from PIL import Image, ImageDraw
from os import path, listdir, mkdir


class Generator:
    def __init__(self, filepath, duration=200, max_size=300, debug=False):
        self.file_path = filepath
        self.duration = duration
        self.MAX_SIZE = max_size
        self.original_size = False
        self.images = []
        self.gif = None
        self.__debug = debug

    def debug(self, text):
        if self.__debug:
            print(text)

    def get_images(self):
        self.images = []
        images_names = listdir(self.file_path)
        valid_names = []
        self.debug("Generating Gif....")
        for name in images_names:
            if ".jpg" in name or ".png" in name or ".jpeg" in name:
                valid_names.append(name)

        for name in valid_names:
            self.images.append(Image.open(f"{self.file_path}/{name}", "r"))
        for i, image in enumerate(self.images):
            self.images[i] = image.rotate(-90, expand=True)
            if (self.images[i].height>=self.MAX_SIZE or self.images[i].width>=self.MAX_SIZE) and not self.original_size:
                s = self.images[i].size
                ratio = self.MAX_SIZE / max(s[0], s[1])
                self.images[i] = self.images[i].resize((int(s[0] * ratio), int(s[1] * ratio)), Image.LANCZOS)
            self.debug(f"    Image {i} processed. Height: {self.images[i].height}; Width: {self.images[i].width}")
        return self.images

    def generate_gif(self):
        self.debug("Now Saving...")
        if not path.exists(f"{self.file_path}/generated"):
            mkdir(f"{self.file_path}/generated")
            self.debug(f"Directory Created: {self.file_path}/generated")
        if path.exists(f"{self.file_path}/generated/generated_0.gif"):
            files = listdir(f"{self.file_path}/generated/")
            new_file_num = int(files[-1].split(".")[0].split("_")[1]) + 1
            filepath = f"{self.file_path}/generated/generated_{new_file_num}.gif"
            self.images[0].save(filepath,
                                save_all=True, append_images=self.images[1:],
                                optimize=False, duration=self.duration, loop=0)
            self.gif = filepath
        else:
            filepath = f"{self.file_path}/generated/generated_0.gif"
            self.images[0].save(filepath, save_all=True, append_images=self.images[1:],
                                optimize=False, duration=self.duration, loop=0)
            self.gif = filepath
        self.debug(f"Gif saved as: {filepath}")
        self.debug("GIF GENERATED!")
        return filepath


'''
# ------------------- OLD CODE
MAX_SIZE = 300


print(f"Pillow Version: {Image.__version__}")
valid = False
while not valid:
    input_path = input("Enter path: ")
    if "\\" in input_path:
        input_path = input_path.replace("\\", "/")
    if path.exists(input_path):
        valid = True
    else:
        print("Path does not exist.")
valid = False
while not valid:
    max_size = input(f"Enter max size (Default {MAX_SIZE}): ")
    if max_size.isnumeric():
        MAX_SIZE = int(max_size)
        valid = True
    elif max_size.strip() == "":
        valid = True
images_names = listdir(input_path)
valid_names = []
print("Generating Gif....")
for name in images_names:
    if ".jpg" in name or ".png" in name or ".jpeg" in name:
        valid_names.append(name)

images = []

for name in valid_names:
    images.append(Image.open(f"{input_path}/{name}", "r"))

for i, image in enumerate(images):
    images[i] = image.rotate(-90, expand=True)
    if images[i].height >= MAX_SIZE or images[i].width >= MAX_SIZE:
        s = images[i].size
        ratio = MAX_SIZE / s[0]
        images[i] = images[i].resize((int(s[0] * ratio), int(s[1] * ratio)), Image.ANTIALIAS)
    print(f"    Image {i} processed.")
print("Saving...")
if not path.exists(f"{input_path}/generated"):
    mkdir(f"{input_path}/generated")
if path.exists(f"{input_path}/generated/generated_0.gif"):
    files = listdir(f"{input_path}/generated/")
    newFileNum = int(files[-1].split(".")[0].split("_")[1])+1
    images[0].save(f"{input_path}/generated/generated_{newFileNum}.gif",
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=200, loop=0)
else:
    images[0].save(f"{input_path}/generated/generated_0.gif",
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=200, loop=0)
print("GIF GENERATED!")
'''
