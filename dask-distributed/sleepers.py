
# %%
import json
from pathlib import Path
from typing import Callable, Dict, Optional
import yaml
from dask.base import visualize

import types


def get_meta(filename: str) -> Dict:
    return yaml.safe_load( Path(filename).read_text() )


def create_function( meta ) -> Callable:
    func_name = meta["name"]
    key_name = meta["key"]
    input_params = meta["inputs"]
    output_params = meta["output"]

    def template_func(*args, **kwargs):
        # here we would use CWL?
        # bind inputs
        # call container 
        # parse artifacts and bind outputs
        return 

    service_func = types.FunctionType(template_func.func_code, template_func.func_globals, func_name)



# sleeper-metadata.yml defines the service, i.e. the function
# https://github.com/ITISFoundation/osparc-services/blob/master/services/sleeper/metadata/metadata.yml
meta = get_meta("sleeper-metadata.yml")
#sleeper = create_function(meta)

def sleeper(input_1:int, input_2: Optional[int]=None):
    print(input_1, input_2)


workbench = json.loads(Path("project.json").read_text())["workbench"]


# convert to dsk
dsk = { }


def get_input(name, value):
    if isinstance(value, dict):
        return value["nodeUuid"][:4]
    return value


for node_id in workbench:
    nid = node_id[:4] 
    dsk[nid] = ( sleeper, *[get_input(name, bind) for name, bind in workbench[node_id]["inputs"].items()] )

visualize(dsk , filename="dsk", format="svg", verbose=True)

# %%
