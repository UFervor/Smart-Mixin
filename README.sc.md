🌐 [English](https://github.com/UFervor/Smart-Mixin/blob/main/README.md) | [简体中文](https://github.com/UFervor/Smart-Mixin/blob/main/README.sc.md)
# Smart-Mixin

## 一个开源的 Clash 配置文件 Python 界面。
## 安装依赖
`pip3 install requests pyyaml`
## `Config`
```Python
Config(
  Url:str, # 从URL下载配置文件
  YAML:str, # 从YAML字符串加载
  File:object = open() # 从文件对象加载
)
```
```Python
def Config.getProxies(
  groups = False, # 是否包括代理组
  embedded = False # 是否包括内置策略
) -> [Proxy]
```
```Python
def Config.mixin( # 追加
  YAML:str, # YAML字符串
  DICT:dict # YAML字典
) -> None
```
```Python
def Config.strip() -> None # 去除空的代理组
```
```Python
# 修改这些属性以编辑配置文件
Config.Proxies # [<PreProcessor.Proxy object>]
Config.ProxyGroups # [<PreProcessor.ProxyGroup object>]
Config.Rules # [<PreProcessor.Rule object>]
Config.DICT # 配置文件YAML字典
Config.YAML # 配置文件YAML字符串
```
## `Proxy`
```Python
Proxy(
  DICT:dict, # YAML字典
  YAML:str # YAML字符串
)
```
```Python
def Proxy.delete( # 删除自身
  globally=False # 是否全局（从代理列表和全部代理组中）删除
) -> None
```
```Python
def Proxy.BATCH(
  YAML:str # 批量实例化
) -> [Proxy]
```
```Python
# 修改这些属性以编辑配置文件
Proxy.name # 代理名称
Proxy.DICT
```
## `ProxyGroup`
```Python
ProxyGroup(
  DICT: dict, # YAML字典
  YAML:str # YAML字符串
)
```
```Python
def ProxyGroup.delete() -> None # 删除自身
```
```Python
def ProxyGroup.BATCH(
  YAML:str # 批量实例化
) -> [ProxyGroup]
```
```Python
# 修改这些属性以编辑配置文件
ProxyGroup.proxies # [<PreProcessor.Proxy>]
ProxyGroup.name # 代理组名称
ProxyGroup.DICT
```
## `Rule`
```Python
Rule(
  YAML:str, # YAML 字符串
  type:str, # e.g. DOMAIN
  matchedTraffic:str, # e.g. google.com
  strategy:str, # e.g. Proxy
  resolve:bool # True / False(no-resolve)
)
```
```Python
def Rule.delete() -> None # 删除自身
```
```Python
def Rule.BATCH(
  YAML:str # 批量实例化
) -> [Rule]
```
```Python
# 修改这些属性以编辑配置文件
Rule.type # e.g. DOMAIN
Rule.matchedTraffic # e.g. google.com
Rule.strategy # e.g. Proxy
Rule.resolve # True / False(no-resolve)
Rule.YAML # DOMAIN,google.com,Proxy
```
## `Embedded`
```Python
# 内置代理
Embedded.DIRECT # <PreProcessor.Proxy>
Embedded.REJECT # <PreProcessor.Proxy>
```
## 筛选
```Python
def select_all( # 匹配所有符合的元素
  obj, # 容器
  reverse = False, # 反转选择
  **kwargs 
  # re_* 正则匹配属性
  # * 直接匹配属性
) -> SELECT_ALL(list) # 返回类列表容器，包含所有符合的元素
```

### Special Tips
```Python
select_all(obj, reverse, **kwargs).method(*args, **kwargs)
```
等价于
```Python
for i in select_all(obj, reverse, **kwargs):
  i.method(*args, **kwargs)
```

```Python
def select( # 匹配第一个元素
  obj, # 容器
  reverse = False, # 反转选择
  **kwargs 
  # re_* 正则匹配属性
  # * 直接匹配属性
) -> item:any # 返回第一个匹配的元素
```
## 插入到容器
```Python
def pop_front(obj, item) -> None # 将一个元素插入到列表前端
```
```Python
def pop_back(obj, item) -> None # 将一个元素插入到列表后端
```
```Python
def extend_back(obj, iterable) -> None # 将一个序列插入到列表前端
```
```Python
def extend_front(obj, iterable) -> None # 将一个序列插入到列表后端
```
## 深拷贝
```Python
def deepcopy(obj: Config) -> Config # 创建 Config 实例的深拷贝
```
## 基于 Pickle 的序列化
```Python
PreProcessor.loadsConfig(bytes: bytes) -> Config
```
```Python
PreProcessor.dumpsConfig(obj: Config) -> bytes
```
