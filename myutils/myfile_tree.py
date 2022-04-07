
import os

def file_tree_dict(dir_path):

    file_dict = {}
    for dir_path, dir_names, file_names in os.walk(dir_path):

        # f_path = dir_path.replace(dir_path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        # f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        dir_path = dir_path.replace('\\', '/')
        if dir_path not in file_dict:
            file_dict[dir_path] = []
        for filename in file_names:
            if '.pickle' not in filename:  # 不要Pickle
                final_path = os.path.join(dir_path,filename).replace('\\', '/')
                file_dict[dir_path].append({"final_path":final_path, "final_name":filename})

    new_dict = {}
    for k,v in file_dict.items():
        if v:
            new_dict[k] = v
    return new_dict

def file_dir_dict(dir_path):
    res = {}
    
    for dir_path, dir_names, file_names in os.walk(dir_path):
        dir_path = dir_path.replace('\\', '/')
        if len(dir_names)>0:
            res[dir_path] = [{'dir_names':i, 'dir_t_path':os.path.join(dir_path, i).replace('\\', '/')} for i in dir_names]
            # print(dir_path, '++++++' ,dir_names, len(file_names))
            break
    return res

def read_txt_py_text(txt_f_path):
    f_lines = []
    f_lines2 = []
                
    try:
        fxxx = open(txt_f_path, 'r', encoding='utf-8')
        f_lines = fxxx.readlines()
        fxxx.close

    except:
        fxxx = open(txt_f_path,'rb')
        f_lines = fxxx.readlines()
        fxxx.close
        for l in f_lines:
            try:
                str1 = l.decode("utf8","ignore").rstrip('\r\n')
                f_lines2.append(str1)
            except:
                str1 = l.decode('gb2312').rstrip('\r\n')
                f_lines2.append(str1)
            finally:
                f_lines2.append(str(l).rstrip('\r\n'))
        f_lines = f_lines2

    return f_lines



if __name__=='__main__':
    # res_dict = file_tree_dict('test')
    # for k,v in res_dict.items():
    #     print(k, '===========>',v)

    res_dict = file_dir_dict('E:/SS_KUDU')  # E:/SS_KUDU
    # for k,v in res_dict.items():
    #     print(k, '===========>', v)




