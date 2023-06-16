Totk-Cooking-simulator
====
[![中文](https://img.shields.io/badge/lang-中文-red.svg)](https://github.com/KingFooZQ/Totk-Cooking-Simulator/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/KingFooZQ/Totk-Cooking-Simulator/blob/main/i18n/README.en.md)


## Intro

A simply Totk cooking simulator or calculator in python.

## Example

```python
from simulator import TotkCookSim

sim = TotkCookSim()
result = sim.cook(['天空蘑菇'], area_lang='CNzh')
print(result)
result = sim.cook(['Apple', 'Apple','Apple','Apple','Apple'], area_lang='USen')
print(result)
```

## UI

ui.py write a simple tkinter ui for program.

## Update
not enough testing, for now it just work.

## Developer
* Bilibili [King_Foo](https://space.bilibili.com/19892384)
* Discord Gespenst#3856

