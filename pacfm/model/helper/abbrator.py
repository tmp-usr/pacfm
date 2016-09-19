def getKaryotypeAbbr(self):
    """
        returns the saved pickle of karyotype names
    """
    pass






class Abbrator:
    """
        abbreviation generator class
    """

    def __init__(self, text, allowedCharLen, upper=True, pathway=False ):
        self.text= text
        
        self.type1= lambda x: "%s." % x[0] if len(x) > 2 else x 
        self.type2= lambda x: "%s." % x[:3] if len(x) > 4  else x

        self.type3= lambda x: "%s" % x[0] if len(x) > 1 else x 
        self.type4= lambda x: x.replace(' ','') 
            

        self.replaceAnd= lambda x: x.upper().replace('AND','&')
        self.upper = upper
        self.abbr= ""
        
        self.setAbbr(allowedCharLen, pathway)
        if pathway:
            self.abbr= self.abbr.replace(' ','_').replace('.','')

        self.capitalize()


    def __repr__(self):
        if self.upper:
            return self.abbr.upper()
        return self.abbr.lower()


    
    def capitalize(self):
        self.abbr= self.abbr.upper() if self.upper else self.abbr.lower()


    def setAbbr(self, allowedCharLen=0, pathway = False):
        text= self.replaceAnd(self.text)
        if pathway:
            text = text.split('[PATH:')[0].strip()
            text= str(text).translate(None, '/\()&-,')
            text= text.lower().replace(' in ',' ').replace(' of ',' ').replace(' by ',' ')

        charLen= len(text)
        
        functions = [self.type2, self.type1, self.type3]
        #while charLen > allowedCharlen:
        ## starting from the last word, apply the 
        ## abbreviation function until there s empty space
        emptySpace= allowedCharLen - charLen
        #print text
        #print charLen , allowedCharLen
        
        if  emptySpace < 0:
            text= str(text).translate(None, '/\()&')
            text= text.lower().replace(' in ',' ').replace(' of ',' ').replace(' by ',' ')
            
            words= text.split()
            nWords= len(words)

            for f in functions:

                for i in range(len(words))[::-1]:
                # first we try to shorten words
                # then take the initials
                    newWord= f(words[i])
                    words[i] = newWord
                    newText= ' '.join(words)
                    
                    if f == self.type3:
                        newText = ''.join(words).replace('.','')

                    charLen = len(newText)
                    emptySpace = allowedCharLen - charLen
                    
                    if emptySpace < 0:
                        continue 

                    else:
                        self.abbr= newText
                        return newText
            
        else:
            self.abbr= text
            return text

