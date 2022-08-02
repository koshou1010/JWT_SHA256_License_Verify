import attr,enum,string
from typing import List, TypeVar,Callable,Union,Tuple,Dict,Any
import cattr
T = TypeVar("T")

@attr.s(auto_attribs=True) 
class CanAcessObject:
    exp_controller:bool=False
    editor:bool=False
    analyser:bool=False
    aws:bool=False

@attr.s(auto_attribs=True)    
class RegCodeObject:
    usersn:Union[ str,None]=None
    regcode:Union[ str,None]=None
    organization:Union[ str,None]=None
class RegResponseObject:
    code:RegCodeObject=None
    can_access:Union[ CanAcessObject,None]=None
class AwsTokenInput:
    access_csv_path:str=None
    region_name:str="ap-southeast-1"
    bucket_name:str=None

        
DictEncoder=cattr.Converter()
    

