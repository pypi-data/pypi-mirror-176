# Windoz

## Example code

+ -: don't execute, just take the first argument as residual
+ r: repeat next time
+ j: jump in line
+ s: spawn


Frame controlling
``` python
from windoz.windoz import *

print(get_fps(100))
data = World(30)
data.add_event(('r', print_average, [data]))
data.add_event(('s', spawn_timer,[], []))
data.run()
```

