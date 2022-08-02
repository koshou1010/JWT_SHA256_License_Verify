import json,time,os
from datetime import datetime,timezone,timedelta
import tkinter as tk
import backend.common.register as com_register
import backend.common.interface as com_interface

class NoFileError(Exception):
    pass
class ExistedFileError(Exception):
    pass
class JSONLoadError(Exception):
    pass
class JSONWriteError(Exception):
    pass

def jsonload(path):
    if os.path.isfile(path): 
        try:
            with open(path,'rb') as f:
                return json.load( f, encoding='utf-8')
        except Exception as e:
            raise JSONLoadError(e)
    else:
        raise NoFileError("")
def jsondump(path,folder,d):
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        with open(path,'w' , encoding='utf-8') as f:
            f.write( json.dumps(d, ensure_ascii=False) )
    except Exception as e:
        raise JSONWriteError(e)
    

def register_aws(input_path):
    inputD=jsonload(input_path)
    days=int(inputD["life_days"])
    sn=inputD["usersn"]
    aud=inputD["organization"]
    access_csv_path=inputD["aws_access_csv_path"]
    region_name=inputD["region_name"]
    bucket_name=inputD["bucket_name"]
    def gen_regcode()->dict:
        start=datetime.utcnow()
        exp= start+ timedelta(days=days)
        #aud='enosim'
        #sn='9366d0eb90a06ff067dfdef6c3eca8f339f72ddd4fa21cf6e376177f3ed1a547'
        aws_token=com_interface.AwsTokenInput()
        aws_token.access_csv_path=access_csv_path #'D:\\pyServer\\S3-breath-care-research-robot.csv'
        aws_token.region_name=region_name #"ap-southeast-1"
        aws_token.bucket_name=bucket_name #"s3-any-test"
        code=com_register.gen_aws_regcode(sn,aud,start,exp,  aws_token_input=aws_token)
        return {"aws_access_key":code,"organization":aud,"usersn":sn}
    d=gen_regcode()
    is_pass,msg,access_key=com_register.valid_aws_license( d["usersn"], d["aws_access_key"],d["organization"],d["usersn"])
    path='./output/aws_access.key'
    folder='./output'
    if is_pass:
        jsondump(path,folder,d)
    return is_pass
def register_license(input_path):
    inputD=jsonload(input_path)
    days=int(inputD["life_days"])
    sn=inputD["usersn"]
    aud=inputD["organization"]
    exp_controller=inputD["exp_controller"]
    editor=inputD["editor"]
    analyser=inputD["analyser"]
    def gen_regcode()->dict:
        start=datetime.utcnow()
        exp= start+ timedelta(days=days)
        #aud='enosim'
        #sn='9366d0eb90a06ff067dfdef6c3eca8f339f72ddd4fa21cf6e376177f3ed1a547'
        code=com_register.gen_regcode(sn,aud,start,exp,exp_controller,editor,analyser)
        return {"regcode":code,"organization":aud,"usersn":sn}
    d=gen_regcode()
    is_pass,msg,can_access=com_register.valid_license(d["usersn"],d["regcode"],d["organization"],d["usersn"])
    path='./output/license.key'
    folder='./output'
    if is_pass:
        jsondump(path,folder,d)
        return is_pass
    else:
        raise Exception


def main():
    reg_path='./input/reg_ini.json'
    aws_path='./input/aws_ini.json'
    master = tk.Tk()
    master.iconbitmap('.\\img\\favicon.ico')
    master.title("Keys generator")
    result=tk.StringVar()
    result.set('')
    lb=tk.Label(master, textvariable=result).grid(row=3, sticky=tk.W,padx=(10, 10))
    def var_states():
        msg=''
        if var1.get()==1:
            try:
                is_pass=register_license(reg_path)
            except:
                msg=msg+  "license.key generate failed\n"
            else:
                msg=msg+  "license.key generate succeed\n"
        if var2.get()==1:
            try:
                is_pass=register_aws(aws_path)
            except:
                msg=msg+ "aws_access.key generate failed\n"
            else:
                msg=msg+  "aws_access.key generate succeed\n"
        

        result.set(msg)
    
        

    tk.Label(master, text="What do you want to do output (multiple):").grid(row=0, sticky=tk.W,padx=(10, 10))
    var1 = tk.IntVar()
    tk.Checkbutton(master, text="license.key", variable=var1).grid(row=1, sticky=tk.W,padx=(10, 10))
    var2 = tk.IntVar()
    tk.Checkbutton(master, text="aws_access.key", variable=var2).grid(row=2, sticky=tk.W,padx=(10, 10))

    tk.Button(master, text='output', command=var_states).grid(row=4, sticky=tk.W, pady=4,padx=(10, 10))
    tk.mainloop()


if __name__ == '__main__':
    main()

   

    