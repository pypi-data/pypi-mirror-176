

__dict = lambda __map:__map if isinstance(__map,dict) else __map.__dict__
__items = lambda __map:__dict(__map).items()
__kv = lambda __item:f"    {str(__item[0])} : {str(__item[1])}"
__dicts = lambda __map:"\n".join(__kv(kv) for kv in __items(__map))
__module_dict = lambda __module:{k:v for k,v in __items(__module) if not "__" in k}
__modulestr = lambda __module:__dicts(__module_dict(__module))
def items(__map):
    return __items(__map)

def  module_dict(__module):
    return __module_dict(__module)

def modulestr(__module):
    return __modulestr(__module)