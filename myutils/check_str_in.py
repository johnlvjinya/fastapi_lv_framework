


def check_str_list_in(father_str, sons_list):
    state = True
    for s in sons_list:
        if s not in father_str:
            state = False
    return state


if __name__=='__main__':
    father_str = "人类EGFR突变基因检测试剂盒"
    sons_list = "人类-基因-试剂盒".split('-')
    res = check_str_list_in(father_str, sons_list)
    print(res)