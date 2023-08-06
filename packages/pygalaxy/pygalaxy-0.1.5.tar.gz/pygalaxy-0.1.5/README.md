# PyGalaxy

This is a simple common package. 

Github: https://github.com/patrickxu1986/pygalaxy

1. logger

```python
from pygalaxy import logger

logger.debug('log message') 
logger.info('log message') 
```

2. time_master

```python
from pygalaxy import time_master

time_master.get_current_date_str()
time_master.get_current_unix_time()
```

3. consistent hash

```python
from pygalaxy.consistent_hash import Node, ConsistentHash

node = Node(node_name='192.1.1.4')
consistent_hash = ConsistentHash()
consistent_hash.add_node(node)
n = consistent_hash.get_node('test content')

```