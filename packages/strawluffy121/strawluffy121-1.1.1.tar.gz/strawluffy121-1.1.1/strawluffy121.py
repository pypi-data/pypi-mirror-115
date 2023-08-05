"""
This is the standard way to include a multiple-line
comment in your code
"""
def print_lol(the_list, indent = False, level = 0):
    # 遍历列表
    for lol_list in the_list:
        # 如果元素为列表，递归重新遍历
        if (isinstance(lol_list, list)):
            print_lol(lol_list, indent, level + 1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='')
            print(lol_list)
