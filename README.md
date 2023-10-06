🌐 [English](https://github.com/UFervor/Smart-Mixin/blob/main/README.md) | [简体中文](https://github.com/UFervor/Smart-Mixin/blob/main/README.sc.md)
# Smart-Mixin

## An open-source Python interface to operate Clash configuration.
## Install dependencies
`pip3 install requests pyyaml`
## User-Agent
```python
Default = f"Clash/{ClashCoreVersion}"
Stash = f"StashCore/{StashVersion} Stash/{StashVersion} Clash/{ClashCoreVersion}"
ClashforWindows = f"ClashforWindows/{ClashforWindowsVersion}"
```
## `Config`
```Python
Config(
  Url:str, # Download configuration file from URL
  YAML:str, # Load from YAML string
  File:object = open() # Load from file object
)
```
```Python
def Config.getProxies(
  groups = False, # Whether to include proxy groups
  embedded = False # Whether to include built-in policies
) -> [Proxy]
```
```Python
def Config.mixin( # Append
  YAML:str, # YAML String
  DICT:dict # YAML Dictionary
) -> None
```
```Python
def Config.strip() -> None # Remove the empty proxy group
```
```Python
# Modify these properties to edit the configuration file
Config.Proxies # [<PreProcessor.Proxy object>]
Config.ProxyGroups # [<PreProcessor.ProxyGroup object>]
Config.Rules # [<PreProcessor.Rule object>]
Config.DICT # Config file YAML dictionary
Config.YAML # Config file YAML string
```
## `Proxy`
```Python
Proxy(
  DICT:dict, # YAML Dictionary
  YAML:str # YAML String
)
```
```Python
def Proxy.delete( # Delete itself
  global=False # Whether to delete globally (from the proxy list and all proxy groups)
) -> None
```
```Python
def Proxy.BATCH(
  YAML:str # Batch instantiation
) -> [Proxy]
```
```Python
# Modify these properties to edit the configuration file
Proxy.name # Proxy name
Proxy.DICT
```
## `ProxyGroup`
```Python
ProxyGroup(
  DICT: dict, # YAML Dictionary
  YAML:str # YAML String
)
```
```Python
def ProxyGroup.delete() -> None # Delete itself
```
```Python
def ProxyGroup.BATCH(
  YAML:str # Batch instantiate
) -> [ProxyGroup]
```
```Python
# Modify these properties to edit the configuration file
ProxyGroup.proxies # [<PreProcessor.Proxy>]
ProxyGroup.name # Proxy group name
ProxyGroup.DICT
```
## `Rule`
```Python
Rule(
  YAML:str, # YAML String
  type:str, # e.g. DOMAIN
  matchedTraffic:str, # e.g. google.com
  strategy:str, # e.g. Proxy
  resolve:bool # True / False(no-resolve)
)
```
```Python
def Rule.delete() -> None # Delete itself
```
```Python
def Rule.BATCH(
  YAML:str # Batch instantiate
) -> [Rule]
```
```Python
# Modify these properties to edit the configuration file
Rule.type # e.g. DOMAIN
Rule.matchedTraffic # e.g. google.com
Rule.strategy # e.g. Proxy
Rule.resolve # True / False(no-resolve)
Rule.YAML # DOMAIN,google.com,Proxy
```
## `Embedded`
```Python
# Embedded proxy
Embedded.DIRECT # <PreProcessor.Proxy>
Embedded.REJECT # <PreProcessor.Proxy>
```
## Filter
```Python
def select_all( # Match all elements that match
  obj, # Container
  reverse = False, # Reverse the selection
  **kwargs 
  # re_* Regular_match_property
  # * Direct match attribute
) -> SELECT_ALL(list) # Returns a class list container with all matching elements
```

### Special Tips
```Python
select_all(obj, reverse, **kwargs).method(*args, **kwargs)
```
is equivalent to
```Python
for i in select_all(obj, reverse, **kwargs).
  i.method(*args, **kwargs)
```

```Python
def select( # Match the first element
  obj, # Container
  reverse = False, # Reverse the selection
  **kwargs 
  # re_* Regular match attribute
  # * Direct match attribute
) -> item:any # Return the first matching element
```
## Insert into container
```Python
def pop_front(obj, item) -> None # Insert an element into the front of the list
```
```Python
def pop_back(obj, item) -> None # Insert an element to the back end of the list
```
```Python
def extend_back(obj, iterable) -> None # Insert a sequence into the front of the list
```
```Python
def extend_front(obj, iterable) -> None # Insert a sequence into the back end of the list
```
## Deep copy
```Python
def deepcopy(obj: Config) -> Config # Create a deep copy of the Config instance
```
## Pickle-based serialization
```Python
PreProcessor.loadsConfig(bytes: bytes) -> Config
```
```Python
PreProcessor.dumpsConfig(obj: Config) -> bytes
```
