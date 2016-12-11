# AutoScaler

Upscales images in a folder to a desired minimum resolution using waifu2x. Images already above the minimum resolution will just be copied.

## Requirements
* Python 3.5
* Pillow
* [waifu2x-converter-cpp](https://github.com/tanakamura/waifu2x-converter-cpp)

## Usage
    python AutoScaler.py -s [source] -d [destination] -p [patterns] -r [recursive] -o [overwrite] -x <minX> -y <minY> -ar [minr] -AR [maxr] -w [w2x-bin] -m [w2x-models] -pu [processor]
    
    --source, -s
        Optional, string
        Directory containing images to be upscaled.
        Default: "./input"
        
    --destination, -d
        Optional, string
        Directory to put upscaled images in.
        Default: "./output"
        
    --prefix, -pr
        Optional, string
        String to prepend to the output filenames.
        Default: ""
        
    --suffix, -su
        Optional, string
        String to append to the output filenames.
        Default: ""
        
    --patterns, -p
        Optional, string
        File patterns to match. 
        Default: "**/*.jpg" "**/*.jpeg" "**/*.png"
        
    --recursive, -r
        Optional, boolean
        Whether to search within subdirectories.
        Default: True
        
    --overwrite, -o
        Optional, boolean
        Whether to overwrite existing files in the destination directory.
        Default: False
        
    --minx, -x
        Required, integer
        Minimum resolution in the x axis to upscale to.
        
    --miny, -y
        Required, integer
        Minimum resolution in the y axis to upscale to.
        
    --minr, -ar
        Optional, float
        Minimum aspect ratio to upscale. 0 to ignore.
        Default: 0
        
    --maxr, -AR
        Optional, float
        Maximum aspect ratio to upscale. 0 to ignore.
        Default: 0
        
    --w2x-bin, -w
        Optional, string
        Path to waifu2x-converter-cpp
        Default: "waifu2x-converter_x64"
        
    --w2x-models, -m
        Optional, string
        Path to waifu2x-converter-cpp model directory
        Default: "models_rgb"
        
    --processor, -pu
        Optional, integer
        Select processor to use. -1 for auto.
        Default: -1
        
## Example
    python AutoScaler.py -s "G:/Libraries/Pictures/Awwnime/" -d "G:\Libraries\Pictures\Wallpapers\Upscaled\Landscape/" -p "**/*.jpg" "**/*.jpeg" "**/*.png" -r True -o False -x 2560 -y 1440 -ar 0.35 -AR 0.65 -w "./waifu2x-converter_x64_1130/waifu2x-converter_x64.exe" -m "./waifu2x-converter_x64_1130/models_rgb" -pu 1
    
Upscales jpg, jpeg, and png files from G:/Libraries/Pictures/Awwnime/ and its subdirectories. If an image has an aspect ratio between 0.35 and 0.65, it will be upscaled to a minimum resolution of 2560x1440.

To get a list of available processors, on waifu2x-converter-cpp, run just the waifu2x binary with the `--list-processor` flag. A dedicated GPU will be the fastest.

## Aspect ratios
Setting the minimum aspect ratio to 0 will mean there's no limit to how narrow the image can be.
Setting the maximum aspect ratio to 0 will mean there's no limit to how wide tha image can be.
Setting both flags to zero will mean that all images will be upscaled.

Common aspect ratios are
* 16:9 = ~1.778
* 4:3 = ~1.333
* 16:10 = 1.6
* 5:4 = 1.25
* 9:16 = 0.5625
* 3:4 = 0.75
* 10:16 = 0.625
* 4:5 = 0.8