data = open("list.txt","r").read()
listp = data.split("\n")
for i in listp:
    if i == "" or i == " ":
        listp.remove(i)
origspace = list("abcdefghijklmnopqrstuvwxyz ")
keyspace  = list("4bcd3fgh1jklmn0pqr57uvwxyz ")



def check(text,include=[],exclude=[]):
    result = []



    
    #for i in listp:
    #    listp.append(english_to_leetspeak(i.upper()))
    e = text.lower()
    x = text.lower()
    for normalletter in origspace:
        e = e.replace(keyspace[origspace.index(normalletter)],normalletter)

    for i in listp+include:
        if not i.lower() in exclude:
            
            if (i.lower() in e) or (i.lower() in e.replace(" ","")):
                
                result.append(i)
            if (i.lower() in x) or (i.lower() in x.replace(" ","")):
                
                result.append(i)


    #print("Time: ", total_time)
    if len(result) == 0:
        return False
    else:
        return result


