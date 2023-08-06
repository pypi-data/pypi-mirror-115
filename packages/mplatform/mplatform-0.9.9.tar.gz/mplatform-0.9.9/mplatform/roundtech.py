"""
    Full name       : Minh Phuong BUI
    Email address   : phuong.buiminh00@gmail.com
    ENGINEERING MECHANICS major
    project         : Rounding in technique 
"
"""

__all__ = ['Round']

class RTNQ:

    @staticmethod
    def inttech(value):return float(value)

    @staticmethod
    def floattech(value,digits):
        if [(str(value)).count('.')  ==1]:
            temp = str(value)[:(str(value).rindex('.'))+digits+2]
            if (str(value)).count('e')  == 1:
                if len(str(value)[str(value).rfind('.')+1:str(value).rindex('e')])\
                    > digits:
                    if int(temp[-1]) >= 5:
                        temp = str(value)[:(str(value).rindex('.'))+digits]+\
                                (str(int(temp[-2])+1))
                        value = temp + str(value)[(str(value).rindex('e')):]
                    else:
                        temp = str(value)[:(str(value).rindex('.'))+digits+1]
                        value = temp + str(value)[(str(value).rindex('e')):]
                    return float(value)
                if len(str(value)[str(value).rfind('.')+1:str(value).rindex('e')])\
                    <= digits:return value
            else:
                if len(str(value)[str(value).rfind('.')+1:]) > digits:
                    if int(temp[-1]) >= 5:
                        temp = str(value)[:(str(value).rindex('.'))+digits]+\
                            (str(int(temp[-2])+1))
                        value = temp
                    else:
                        temp = str(value)[:(str(value).rindex('.'))+digits+1]
                        value = temp
                    return float(value)
                if len(str(value)[str(value).rfind('.')+1:]) <= digits:return value
        else: print('\n\tMath Error!\nI will fix it in the next update\n')

    @staticmethod
    def listtech(value,digits):
        for (index,ivalue) in enumerate(value):
            if str(type(ivalue)) == "<class 'float'>":value[index] =\
                RTNQ.floattech(value[index], digits)
            if str(type(ivalue)) == "<class 'int'>":value[index] =\
                RTNQ.inttech(value[index])
        return value

    @staticmethod
    def matrixtech(value,digits):
        if len(value.shape) == 2:
            temp_1 = []
            for i in range(0,(value.shape)[0]):
                temp_2 = []
                for j in range(0,(value.shape)[-1]):
                    if str(type(value[i][j])) == "<class 'numpy.float64'>":
                        temp_2.append(RTNQ.floattech(value[i][j], digits))
                    if str(type(value[i][j])) == "<class 'numpy.int32'>":
                        temp_2.append(RTNQ.inttech(value[i][j]))
                temp_1.append(temp_2)
            return temp_1


def Round(value,digits=4):
    """input: value and digits"""
    type_value =(str(type(value))).split("'",3)
    if 1<= digits <= 7:
        if type_value[1] == 'numpy.ndarray':return (RTNQ.matrixtech(value,digits))
        elif type_value[1] == 'str':return value
        elif type_value[1] == 'int':return RTNQ.inttech(value)
        elif type_value[1] == 'float':return (RTNQ.floattech(value, digits))
        elif type_value[1] == 'complex':return value
        elif type_value[1] == 'list':return (RTNQ.listtech(value, digits))
        elif type_value[1] == 'tuple':return value
        else: print('\n\tMath Error!\nI will fix it in the next update\n')
    else: return value

def main(): pass
if __name__ == '__main__' : main()
