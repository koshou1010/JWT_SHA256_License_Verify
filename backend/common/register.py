
import winreg
import hashlib
import setting_base
import jwt,csv
from datetime import datetime
import backend.common.interface as interface
import random
def os_detect():
    if setting_base.OS=="Windows":
        if setting_base.IS64BIT:
            pass
        else:
            raise ValueError("OS not supported")
    elif setting_base.OS=="Darwin":
        raise ValueError("OS not supported")
    elif setting_base.OS=="Linux":
        raise ValueError("OS not supported")
    else:
        raise ValueError("OS not supported")

def get_machineguid():
    os_detect()
    regpath='Software\Microsoft\Cryptography'
    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, regpath, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
        guid = winreg.QueryValueEx(key, "MachineGuid")[0]
        return guid
       

def md5encode(guid):
    m = hashlib.md5()
    m.update((setting_base.HASHADDHEAD+guid+setting_base.HASHADDTAIL).encode("utf-8"))
    h = m.hexdigest()
    return h



def sha256encode(guid):
    m = hashlib.sha256()
    m.update((setting_base.HASHADDHEAD+guid+setting_base.HASHADDTAIL).encode("utf-8"))
    h = m.hexdigest()
    return h


    
def get_access_keys(csv_path:str):
    with open(csv_path, "r", encoding='utf-8') as f:
        filereader=csv.DictReader(f)
        d = {}
        for row in filereader:
            for column, value in row.items():
                d.setdefault(column, []).append(value)
        return {"id":d["Access key ID"][0],"key":d["Secret access key"][0]}
        
def gen_regcode(usersn,aud,start:datetime,exp:datetime,exp_controller,editor,analyser):
    payload = {
        'iss': setting_base.ISS,
        'sub': usersn,
        'aud': aud,
        'exp': exp,   # must use UTC time
        'nbf': start,  #datetime.utcnow(),
        'iat': start,
        'jti': setting_base.JTI,
        'exp_controller':exp_controller,
        'editor':editor,
        'analyser':analyser
    }
    return jwt.encode(payload, setting_base.JWTSECRET, algorithm='HS256').decode("UTF8")

def gen_aws_regcode(usersn,aud,start:datetime,exp:datetime,aws_token_input:interface.AwsTokenInput=None):
    if aws_token_input is not None:
        access_key=get_access_keys(aws_token_input.access_csv_path)
        
        s3={
            'region_name':aws_token_input.region_name,
            'bucket_name':aws_token_input.bucket_name
        }
    else:
        access_key=None
        s3=None
    payload = {
        'iss': setting_base.ISS,
        'sub': usersn,
        'aud': aud,
        'exp': exp,   # must use UTC time
        'nbf': start,  #datetime.utcnow(),
        'iat': start,
        'jti': setting_base.JTI,
        'aws_access_key':access_key,
        's3':s3
    }
    return jwt.encode(payload, setting_base.JWTSECRET, algorithm='HS256').decode("UTF8")

def decode_regcode(regcode,aud):
    
    return jwt.decode(regcode, setting_base.JWTSECRET, algorithms='HS256',
        issuer=setting_base.ISS,
        audience=aud,
        leeway=setting_base.LEEWAY
        )

def valid_license(usersn,regcode,organization,encoded_guid):
    try:
        
        d=decode_regcode(regcode,organization)
    except jwt.ExpiredSignatureError:
        return False,'Signature has expired.',None
    except jwt.InvalidIssuedAtError:
        return False,'This code represents a time in the future',None
    except jwt.ImmatureSignatureError:
        return False,'This code represents a time in the future',None
    except Exception as e:
        return False,'This code is not valid.',None
    else:
        if d['sub'] == encoded_guid:
            return True,None,{'exp_controller':d['exp_controller'],'editor':d['editor'],'analyser':d['analyser']}
        else:
            return False,"This code is not valid.",None
   
def valid_aws_license(usersn,regcode,organization,encoded_guid):
    try:
        
        d=decode_regcode(regcode,organization)
    except jwt.ExpiredSignatureError:
        return False,'Signature has expired.',None
    except jwt.InvalidIssuedAtError:
        return False,'This code represents a time in the future',None
    except jwt.ImmatureSignatureError:
        return False,'This code represents a time in the future',None
    except Exception as e:
        return False,'This code is not valid.',None
    else:
       
        if d['sub'] == encoded_guid:
            access_key=d['aws_access_key']
            s3=d['s3']
            return True,None,{"access_key":access_key,"target":{"s3":s3}}
        else:
            return False,"This code is not valid.",None
