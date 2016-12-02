import glob
import subprocess
import shutil
from PIL import Image

sourceDir = "D:/Libraries/Pictures/Awwnime"
sinkDir = "G:/Libraries/Pictures/Wallpapers/Upscaled/Landscape"
patterns = ["*.jpg", "*.jpeg", "*.png"]

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
w2xModels = "./waifu2x-converter_x64_1130/models" # Don't append last /
        
def upscale(source, sink, factor, nr):
    # Scale ratios below 2 are not supported.
    if (factor < 2):
        factor = 2
        
    if nr:
        mode = "noise_scale"
        subprocess.call("start /wait %s -m %s -i \"%s\" -o \"%s\" --processor 1 --scale_ratio %f --noise_level %d -- --model_dir \"%s\"" % (w2xBin, mode, source, sink, factor, nr, w2xModels), shell = True)
    else:
        mode = "scale"
        subprocess.call("start /wait %s -m %s -i \"%s\" -o \"%s\" --processor 1 --scale_ratio %f -- --model_dir \"%s\"" % (w2xBin, mode, source, sink, factor, w2xModels), shell = True)
    pass
        
def copy(source, sink):
    shutil.copyfile(source, sink)
        
def main():
    imgList = glob.glob("%s/*.png" % sourceDir)
    imgList += glob.glob("%s/*.jpg" % sourceDir)
    imgList += glob.glob("%s/*.jpeg" % sourceDir)
    
    imgCount = len(imgList)
    doneCount = 0
    
    for image in imgList:
        image = image.replace("\\", "/")
        doneCount += 1
        filename = image.split("/")[-1]
        sink = "%s/%s" % (sinkDir, filename.replace('.jpg', '.png').replace('.jpeg', '.png'))
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
                
if (__name__ == "__main__"):
    main()
