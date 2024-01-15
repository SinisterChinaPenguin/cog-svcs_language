def remove_trailing_opens(string1):
    end_str=string1[-5:] # last 5 chars of string
    if end_str.lower() == 'opens':
        char_before=string1[-6:-5] # check what character before opens is (is it a space?)
        if char_before != ' ':
            string1 = string1[:-5] # remove last 5 characters (i.e. opens from opens in new window)
    return string1

#string1 = "consumer rights actopens" # Delivery rights Rights 
string1 = "Delivery rights Rights opens"
string1 = remove_trailing_opens(string1)
words = string1.lower().split()
print (" ".join(sorted(set(words), key=words.index)))


#Consumer Contracts RegulationOpens
#Consumer Rights ActOpens

# new window
