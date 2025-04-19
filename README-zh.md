# ComfyUI-Prompt-Wildcards

ComfyUI中通过选项使用的Wildcards

[简体中文|[English](README.md)]

# 描述

通过选项的方式使用Prompt Wildcards。

类似于[stable-diffusion-webui-wildcards](https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards)在ComfyUI中的用处，但不使用 `__name__`。

![image](./example_workflows/ComfyUI-Prompt-Wildcards1.jpg)
![image](./example_workflows/ComfyUI-Prompt-Wildcards2.jpg)

2025/03/20: 为了保证同种子下每个不同count即使使用同一文件也调取不同内容，修改了randoms的随机方式，未来复刻时同种子将与 `2025/03/20`前的内容不同。

Wildcards文件夹路径：

* 在 ComfyUI 安装的根目录中创建一个名为 “wildcards” 的目录（/ComfyUI/wildcards）
* 本插件目录下的“wildcards”（/ComfyUI/custom_nodes/ComfyUI-Prompt-Wildcards/wildcards）

节点参数解释：

* makiwildcards:
  * wildcards_count:选择使用的wildcard数量
  * randoms:是否保持种子随机，调整为false时按照种子的数值选择行数，true是为了复刻原先内容（2025/1/8前未添加该参数），即随机行
  * seed:随机种子，根据 `randoms`的模式选择txt文件中的某行
  * wildcard_name_{n}:选择wildcard文件
  * text:这里的内容将会添加到wildcards前面并以英文逗号相隔
* makitextwildcards:
  * `randoms`,`seed`与 `makiwildcards`中的用法均相同，`text`为需要随机的文本内容，根据 `randoms`与 `seed`选取某行文本输出，即与wildcards使用的txt中的内容同性质
* textconcatenate
  * text_count:选择使用的text数量
  * delimiter:间隔符
  * clean_whitespace:移除两端空白字符
  * replace_underscors:将下划线替换为空格
  * text_{n}:文本内容

## 安装

打开 `ComfyUI`根目录下的 `custom_nodes`：

```
git clone https://github.com/MakkiShizu/ComfyUI-Prompt-Wildcards.git
```

节点名称：

- utils/Prompt-Wildcards/makiwildcards
- utils/Prompt-Wildcards/makitextwildcards
- utils/Prompt-Wildcards/textconcatenate
- utils/Prompt-Wildcards/textconcatenate_v2

### 许可证

本项目遵循MIT许可证。

<hr>
