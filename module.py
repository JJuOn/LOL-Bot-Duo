import os

def check_path_and_mkdir(full_path):
    full_path_list=full_path.split('/')
    for i in range(1,len(full_path_list)):
        if i==len(full_path_list)-1:
            path=full_path
        else:
            path='/'.join(full_path_list[0:i+1])
        if not os.path.exists(path):
            os.mkdir(path)
    return

def read_log(log_file_path):
    file=open(log_file_path,'r')
    idx=int(file.readline())
    file.close()
    return idx
    
def write_log(log_file_path,idx):
    file=open(log_file_path,'w')
    file.write(str(idx))
    file.close()
    return