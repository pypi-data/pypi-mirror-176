# visor

Makes background process management easy.

## Installation
```sh
pip3 install -U visor
```

## Usage
```py
from visor import Visor

visor = Visor()

visor.add("sleep 20")
visor.add("sleep 20 && echo done")

visor.show() # print all added processes

visor.kill_all() # send SIGKILL to all running processed

visor.terminate_all() # send SIGTERM to all running processed

visor.active # List of all `added` processes

# Get log files for first added process (sleep 20)
stdout_path, stderr_path = visor.get_log_files(visor.active[0]) 

# Wait for all processes to exit
visor.wait()

```