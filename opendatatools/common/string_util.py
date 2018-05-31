# encoding: UTF-8

def remove_chinese(str):
    s = ""
    for w in str:
        if w >= u'\u4e00' and w <= u'\u9fa5':
            continue
        s += w
    return s