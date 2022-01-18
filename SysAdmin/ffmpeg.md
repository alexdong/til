# Find all `.MOV` files in the current folder, 
# Extract the key frames in the video's resolution/aspect ratio
find . *.MOV -exec ffmpeg -i {} -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 {}-%02d.jpeg \;
