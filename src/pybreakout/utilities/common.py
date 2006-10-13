class Describer:
    def __repr__(self):
        currentClassName = self.__class__.__name__
        outString = "\n\n<instance of '%s' class>"%currentClassName
        attributeNameList = self.__dict__.keys()
        attributeNameList.sort()
        for attributeName in attributeNameList:
            outString += "\n\t<attr name='%s' value='%s' />"%(attributeName,self.__dict__[attributeName])
        outString += "\n</instance>\n\n"
        return outString