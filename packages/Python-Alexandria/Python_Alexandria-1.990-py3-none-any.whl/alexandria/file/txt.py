def save_txt(filename, string):
    with open(filename, 'a') as f:
        f.write('	'.join(map(str, string))+'\n')
