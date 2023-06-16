Totk-Cooking-simulator
====
[![中文](https://img.shields.io/badge/lang-中文-red.svg)](https://github.com/KingFooZQ/Totk-Cooking-Simulator/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/KingFooZQ/Totk-Cooking-Simulator/blob/main/i18n/README.en.md)


## 简介

一个简单的Python王国之泪料理模拟器或者说计算器。

## 示例

```python
from simulator import TotkCookSim

sim = TotkCookSim()
result = sim.cook(['天空蘑菇'], area_lang='CNzh')
print(result)
result = sim.cook(['Apple', 'Apple','Apple','Apple','Apple'], area_lang='USen')
print(result)
```

## UI

ui.py 写了一个简单的tkinter ui程序

## 进度

还没进行大量测试,目前处于 至少能工作 的状态

## 作者

b站主页[King_Foo](https://space.bilibili.com/19892384)

