def count_lines(path):
    try:
        with open(path,'r',encoding = 'utf-8') as f:
            lines = f.readlines()

    except FileNotFoundError:
        print(f'找不到文件:',path)
        return 0,0,0

    fk_hangshu = [l for l in lines if l.strip()]

    z_zifu = sum(len(l) for l in lines)

    return(len(lines),len(fk_hangshu),z_zifu)

(a,b,c) =count_lines('materials.txt')

print(f'行数为:{a}行,非空行数为:{b}行,总字符数量为:{c}个')