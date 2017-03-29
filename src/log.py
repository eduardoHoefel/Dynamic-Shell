def log(text):
    with open('.log_debug.txt','w') as f:
        f.write('\n' + str(text))

