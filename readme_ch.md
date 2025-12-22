# 图像局部放大

💬 [🌟 [English Version] 🌟](readme.md) 

- **多种模式** 🔍
  
<div style="display: flex;">
    <img src="doc/mode.jpg" width="500">
</div>
<br>

- **任意ROI数量** ➕

<div style="display: flex;">
    <img src="doc/number.jpg" width="500">
</div>
<br>

- **灵活的放置** 📍

<div style="display: flex;">
    <img src="doc/location.jpg" width="500">
</div>
<br>

## 用法 🚀
1. 只需要安装```python```和```opencv-python```
2. 将需要画框的图像都放入同一文件夹 (支持不同格式和分辨率的图像)
3. 设置参数（```zoomTool.py```中的```CONFIGS```），详见 <*参数说明*>
4. 运行 ```zoomTool.py``` 

## 参数说明 ⚙️
| 参数 | 说明 |
| :- | :- |
| images_dir       | 图像所在的目录  | 
| roi_number       | 放大框的数量    | 
| mode             | "inside"：内置放大框；"outside"：外置放大框； "only_roi"：只框ROI而不缩放 | 
| outside_position | 外置放大框的位置 （只适用于"outside"模式）| 
| inside_position  | 内置放大框的位置 （只适用于"inside"模式） | 
| scale            | 缩放倍率（只适用于"inside"模式）         | 
| if_dash_box      | 需要ROI虚线框时置为True     |   


- 以下 参数↓ 可以保持默认即可

| 参数(可选) | 说明 |
| :- | :- |
| thickness        | 放大框线条粗细（建议"auto"） |   
| colors           | 放大框线条颜色  |   
| dash_length      | 虚线长度        |   
| save_folder      | 图像保存路径    |   
| roi_folder       | ROI保存路径     |  
| reference_img    | 用于标注ROI和对齐分辨率  |   
