<div align="center">
  <img src="https://raw.githubusercontent.com/ReedKrawiec/DaMa/main/docs/header.png" />
</div>

# About

DaMa is a tool to help you generate data for your computer vision projects. 

Create a "provider" that generates Pillow images and annotations. These
annotations are in the format of (class_index,x,y,width,height) with x and y being
in the center. Class index is the index of the correct label within dama.json. Look at
the provider folder, it contains an example provider. Look at dama.json for all configuration.

To Execute
```
python3 dama.py 
```
To Execute with labels highlighted with a box 
```
python3 dama.py --draw-labels
```