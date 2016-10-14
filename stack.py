def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring

def getNum(string):
	num = ""
	for letter in string:
		if not (letter in "0123456789"): break
		num += letter
	if num == '':
		print "NO NUMBER IN", string, string[0], "is not a unit"
		return 0
	return int(num)
