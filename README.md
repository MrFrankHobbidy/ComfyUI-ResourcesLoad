# ComfyUI-ResourcesLoad
load the Comfyui nodes variables from a file.<br>
从文件中加载Comfyui节点变量。

ComfyUI change the limit of file size for upload(ComfyUI更改上传文件大小限制):<br>
add --max-upload-size argument, the default is 100MB( --max-upload-size 100)

Notice注意:<br>
The "RsaveImage" node should be placed at the end of the workflow; otherwise, it will add additional metadata to other output files.
RsaveImage节点要留在工作流最后输出，否则会对其他输出文件添加额外的元数据。

Related node 相关节点: <a href="https://github.com/MrFrankHobbidy/ComfyUI-ResourcesSave">https://github.com/MrFrankHobbidy/ComfyUI-ResourcesSave</a>
