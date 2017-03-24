def log(text):
    with open('log.txt','w') as f:
        f.write('\n' + str(text))

