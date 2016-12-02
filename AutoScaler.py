import glob
import subprocess
import shutil
import os
from PIL import Image

sourceDir = "D:/Libraries/Pictures/Awwnime"
sinkDir = "G:/Libraries/Pictures/Wallpapers/Upscaled/Landscape"
patterns = ["**/*.jpg", "**/*.jpeg", "**/*.png"]
recursive = True

# Target resolution
minX = 2560
minY = 1440

# Aspect ratios to consider. Set both to 0 to ignore.
# 16:9 = ~1.778 || 9:16 = 0.5625
# 4:3 = ~1.333 || 3:4 = 0.75
# 16:10 = 1.6 || 10:16 = 0.625
# 5:4 = 1.25 || 4:5 = 0.8
minRatio = 1.5
maxRatio = 2

w2xBin = "./waifu2x-converter_x64_1130/waifu2x-converter_x64.exe"
w2xModels = "./waifu2x-converter_x64_1130/models_rgb" # Don't append last /

# Run waifu2x in seperate terminal. Annoying if trying to use the PC.
# Otherwise it'll run in the same terminal, and I have no idea how to surpress the output.
annoy = False
        
def upscale(source, sink, factor, nr):
    # Scale ratios below 2 are not supported.
    if (factor < 2):
        factor = 2
        
    if nr:
        mode = "noise_scale"
        if annoy:
            subprocess.call("start /wait %s -m %s -i \"%s\" -o \"%s\" --processor 1 --scale_ratio %f --noise_level %d --model_dir \"%s\"" % (w2xBin, mode, source, sink, factor, nr, w2xModels), shell = True)
        else:
            subprocess.run([w2xBin, "-m %s" % mode, "-i %s" % source, "-o %s" % sink, "--processor 1", "--scale_ratio %f" % factor, "--noise_level %d" % nr, "--model_dir %s" % w2xModels])
    else:
        mode = "scale"
        if annoy:
            subprocess.call("start /wait %s -m %s -i \"%s\" -o \"%s\" --processor 1 --scale_ratio %f --model_dir \"%s\"" % (w2xBin, mode, source, sink, factor, w2xModels), shell = True)
        else:
            subprocess.run([w2xBin, "-m %s" % mode, "-i %s" % source, "-o %s" % sink, "--processor 1", "--scale_ratio %f" % factor, "--model_dir %s" % w2xModels])
    pass
        
def copy(source, sink):
    shutil.copyfile(source, sink)
    
def getRelativeDir(image):
    image = image.replace(sourceDir, "")
    print(image)
    return "".join(image.split("/")[:-1])
        
def main():
    
    imgList = []
    
    for pattern in patterns:
        pattern = pattern.replace("\\", "/")
        imgList += glob.glob("%s/%s" % (sourceDir, pattern), recursive=recursive)
    
    imgCount = len(imgList)
    doneCount = 0
    
    for image in imgList:
        image = image.replace("\\", "/")
        doneCount += 1
        filename = image.split("/")[-1]
        print(image)
        if not os.path.isdir("%s/%s/" % (sinkDir, getRelativeDir(image))):
            os.makedirs("%s/%s/" % (sinkDir, getRelativeDir(image)))
        sink = "%s/%s/%s" % (sinkDir, getRelativeDir(image), filename.replace('.jpg', '.png').replace('.jpeg', '.png'))
        # print(sink)
        size = Image.open(image).size
        ratio = size[0] / size[1]
        print("%d/%d %s (%dx%d)" % (doneCount, imgCount, filename, size[0], size[1]), end="")
        if (minRatio and maxRatio):
            if ((ratio < maxRatio) and (ratio > minRatio)):
                if (size[1] < minY) or (size[0] < minX):
                    deltaX = minX - size[0];
                    deltaY = minY - size[1];
                    if (deltaX > deltaY):
                        factor = minX / size[0]
                    else:
                        factor = minY / size[1]
                    nr = 0
                    if (image[-3:] == "jpg" or image[-4:] == "jpeg"):
                        nr = 1
                    print(" -> (%dx%d)" % (size[0] * factor, size[1] * factor))
                    upscale(image, sink, factor, nr)
                else:
                    copy(image, sink)
                    print(" - Meets size contraints (copied)")
            else:
                print(" - Aspect ratio out of bounds (skipped)")
                    
        else:
            deltaX = minX - size.width;
            deltaY = minY - size.height;
            
            if (deltaX > 0) or (deltaY > 0):
                if (deltaX > deltaY):
                    factor = minX / size.width
                else:
                    factor = minY / size.height
                nr = 0
                if (image[-3:] == "jpg" or image[-4:] == "jpeg"):
                    nr = 1
                print(" -> (%dx%d)" % (size[0] * factor, size[1] * factor))
                upscale(image, factor, nr)
            else:
                copy(image, sink)
                print(" - Meets size contraints (copied)")
            
NAME = "AutoScaler"
VERSION = "0.1"

sourceDir = sourceDir.replace("\\", "/")
sinkDir = sinkDir.replace("\\", "/")
w2xBin = w2xBin.replace("\\", "/")
w2xModels = w2xModels.replace("\\", "/")
                
if (__name__ == "__main__"):
    main()
