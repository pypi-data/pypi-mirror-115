def floor(string):
    stri = len(string)
    lin = ""
    li = ""
    for i in range (stri):
        lin = lin + "_"
    for i in range (stri):
        li = li + " "
    print("""
     ____"""+lin+"""______
    |     """+li+"""     |
    |     """+li+"""     |
    |     """+li+"""     |
    |     """+li+"""     |
    |     """+li+"""     |
    |     """+li+"""     |
    |_____%s_____|
    """%string)