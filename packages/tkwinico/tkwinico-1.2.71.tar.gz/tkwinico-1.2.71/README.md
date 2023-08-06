# tkwinico
为Windows系统提供开发系统托盘的功能。

![PyPI](https://img.shields.io/pypi/v/tkwinico?color=07c160&label=winico)
![PyPI - Downloads](https://img.shields.io/pypi/dw/tkwinico?color=0f5fff)
![PyPI - License](https://img.shields.io/pypi/l/tkwinico?color=red)
---
## 方法
### load_winico
> 加载winico库
    
### taskbar
用于创建、删除、修改托盘图标。
> 参数: 
>> id 
>>> add 添加托盘图标  
>>> delete 删除托盘图标  
>>> modify 修改托盘图标  
>>> `id="add"`   
> 
>> procname
>>> 程序名称，可通过`load`、`createform`、`setwindow`的值得到。  
>>> `procname=load("application")`
> 
>> callback
>>> 事件回调，可以设置为`($root.register($func))`，`$root`为Tk窗口，`$func`为事件函数。
>
>> text
>>> 工具提示，需设置为任意字串符

### info
> 参数
>> id
>>> 程序名称，可通过`load`、`createform`、`setwindow`的值得到。  


## 示例
```python
from tkwinico import *
import tkinter as tk


Window = tk.Tk()


def CallBack(Message, X, Y):
    if Message == WM_RBUTTONDOWN:
        Menu = tk.Menu(tearoff=False)
        Menu.add_command(label="Quit", command=Window.quit)
        Menu.tk_popup(X, Y)


taskbar(ADD, load(APPLICATION), (Window.register(CallBack), MESSAGE, X, Y))

Window.mainloop()
```