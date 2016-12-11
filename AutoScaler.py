import glob
import subprocess
import shutil
import os
from PIL import Image
import argparse
        
        
def upscale(source, sink, factor, nr):
    # Scale ratios below 2 are not supported.
    if (factor < 2):
        factor = 2
        
    if nr:
        mode = "noise_scale"
    else:
        mode = "scale"
        
    command = [w2xBin, "-m %s" % mode, "-i %s" % source, "-o %s" % sink, "--scale_ratio %f" % factor, "--model_dir %s" % w2xModels]
    
    if processor != -1:
        command += "--processor %d" % processor
        
    if nr:
        command += "--noise_level %d" % nr
        
    subprocess.run([w2xBin, "-m %s" % mode, "-i %s" % source, "-o %s" % sink, "--processor %d" % processor, "--scale_ratio %f" % factor, "--model_dir %s" % w2xModels])
        
        
def copy(source, sink):
    shutil.copyfile(source, sink)
    
    
def getRelativeDir(image):
    image = image.replace(sourceDir, "")
    return "/".join(image.split("/")[:-1])
        
        
def main():
    
    imgList = []
    
    for pattern in patterns:
        pattern = pattern.replace("\\", "/")
        print("Scanning %s/%s" % (sourceDir, pattern))
        imgList += glob.glob("%s/%s" % (sourceDir, pattern), recursive=recursive)
    
    imgCount = len(imgList)
    doneCount = 0
    
    for image in imgList:
        image = image.replace("\\", "/")
        doneCount += 1
        filename = image.split("/")[-1]
        relativeDir = getRelativeDir(image)
        if not os.path.isdir("%s/%s/" % (sinkDir, relativeDir)):
            os.makedirs("%s/%s/" % (sinkDir, relativeDir))
        sink = "%s/%s/%s" % (sinkDir, relativeDir, filename.replace('.jpg', '.png').replace('.jpeg', '.png'))
        size = Image.open(image).size
        ratio = size[0] / size[1]
        print("%d/%d .%s/%s (%dx%d)" % (doneCount, imgCount, relativeDir, filename, size[0], size[1]), end="")
        if (minRatio and maxRatio):
            if ((ratio < maxRatio) and (ratio > minRatio)):
                if not (os.path.isfile(sink) and not overwrite):
                    if os.name == "nt":
                        os.system("title %d/%d %s %s - .%s/%s (%dx%d)" % (doneCount, imgCount, NAME, VERSION, relativeDir, filename, size[0], size[1]))
                    if (size[1] < minY) or (size[0] < minX):
                        tempSize = [size[0], size[1]]
                        factor = 1
                        while (tempSize[1] < minY) or (tempSize[0] < minX):
                            deltaX = minX - tempSize[0];
                            deltaY = minY - tempSize[1];
                            if (deltaX > deltaY):
                                factor = factor * minX / tempSize[0]
                            else:
                                factor = factor * minY / tempSize[1]
                            tempSize[0] = tempSize[0] * factor
                            tempSize[1] = tempSize[1] * factor
                        nr = 0
                        if (image[-3:] == "jpg" or image[-4:] == "jpeg"):
                            nr = 1
                        print(" -> (%dx%d)" % (size[0] * factor, size[1] * factor))
                        upscale(image, sink, factor, nr)
                    else:
                        copy(image, sink)
                        print(" - Meets size contraints (copied)")
                else:
                    print(" - Image already exists (skipped)")
            else:
                print(" - Aspect ratio out of bounds (skipped)")
                    
        else:
            if not (os.path.isfile(sink) and overwrite):
                
                if os.name == "nt":
                    os.system("title %d/%d %s %s - %s/%s (%dx%d)" % (doneCount, imgCount, NAME, VERSION, relativeDir, filename, size[0], size[1]))
                
                if (deltaX > 0) or (deltaY > 0):
                    tempSize = [size[0], size[1]]
                    factor = 1
                    while (tempSize[1] < minY) or (tempSize[0] < minX):
                        deltaX = minX - tempSize[0];
                        deltaY = minY - tempSize[1];
                        if (deltaX > deltaY):
                            factor = factor * minX / tempSize[0]
                        else:
                            factor = factor * minY / tempSize[1]
                        tempSize[0] = tempSize[0] * factor
                        tempSize[1] = tempSize[1] * factor
                    nr = 0
                    if (image[-3:] == "jpg" or image[-4:] == "jpeg"):
                        nr = 1
                    print(" -> (%dx%d)" % (size[0] * factor, size[1] * factor))
                    upscale(image, factor, nr)
                else:
                    copy(image, sink)
                    print(" - Meets size contraints (copied)")
            else:
                print(" - Image already exists (skipped)")
            
            
NAME = "AutoScaler"
VERSION = "1.0.1"

parser = argparse.ArgumentParser(description="Upscale images to a minimum resolution within a certain aspect ratio.")
parser.add_argument("--source", "-s", type = str, required = True, help = "Directory containing images to be upscaled.")
parser.add_argument("--destination", "-d", type = str, required = True, help = "Directory to put upscaled images in.")
parser.add_argument("--patterns", "-p", type = str, default = ["**/*.jpg", "**/*.jpeg", "**/*.png"], nargs = "+", help = "File patterns to match. Default are \"**/*.jpg\" \"**/*.jpeg\" \"**/*.png\"")
parser.add_argument("--recursive", "-r", type = bool, default = True, choices = [True, False], help = "Whether to search within subdirectories. Default = True")
parser.add_argument("--overwrite", "-o", type = bool, default = False, choices = [True, False], help = "Whether to overwrite existing files in the destination directory. Default = False")
parser.add_argument("--minx", "-x", type = int, required = True, help = "Minimum resolution in the x axis to upscale to.")
parser.add_argument("--miny", "-y", type = int, required = True, help = "Minimum resolution in the y axis to upscale to.")
parser.add_argument("--minr", "-ar", type = float, default = 0, help = "Minimum aspect ratio to upscale. 0 to ignore. Default = 0")
parser.add_argument("--maxr", "-AR", type = float, default = 0, help = "Maximum aspect ratio to upscale. 0 to ignore. Default = 0")
parser.add_argument("--w2x-bin", "-w", type = str, required = True, help = "Path to waifu2x binary.")
parser.add_argument("--w2x-models", "-m", type = str, required = True, help = "Path to waifu2x model directory.")
parser.add_argument("--processor", "-pu", type = int, default = -1, help = "Select processor to use. Default: -1 (auto)")

args = parser.parse_args()
args = vars(args)

sourceDir = args["source"]
sinkDir = args["destination"]
patterns = args["patterns"]
recursive = args["recursive"]
overwrite = args["overwrite"]

# Target resolution
minX = args["minx"]
minY = args["miny"]

minRatio = args["minr"]
maxRatio = args["maxr"]

w2xBin = args["w2x_bin"]

w2xModels = args["w2x_models"] # Don't append last /
if w2xModels.endswith("/") or w2xModels.endswith("\\"):
    w2xModels = w2x-models[:-1]

processor = args["processor"]

sourceDir = sourceDir.replace("\\", "/")
sinkDir = sinkDir.replace("\\", "/")
w2xBin = w2xBin.replace("\\", "/")
w2xModels = w2xModels.replace("\\", "/")
                
                
if (__name__ == "__main__"):
    if os.name == "nt":
        os.system("chcp 65001")
    main()
