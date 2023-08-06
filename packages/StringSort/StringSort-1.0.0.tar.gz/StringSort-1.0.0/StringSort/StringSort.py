class StringSort:

    def __init__(self, string):
        self.string = string

    def delete(self, delete):
        self.delete = delete
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if list1[i] == str(self.delete):
                list1[i] = ''
        return ''.join(list1)

    def delete_2_symbol(self, sign1, sign2):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)):
                list1[i] = ''
        return ''.join(list1)

    def delete_3_symbol(self, sign1, sign2, sign3):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)):
                list1[i] = ''
        return ''.join(list1)

    def delete_4_symbol(self, sign1, sign2, sign3, sign4):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)):
                list1[i] = ''
        return ''.join(list1)

    def delete_5_symbol(self, sign1, sign2, sign3, sign4, sign5):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)):
                list1[i] = ''
        return ''.join(list1)

    def delete_6_symbol(self, sign1, sign2, sign3, sign4, sign5, sign6):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)):
                list1[i] = ''
        return ''.join(list1)

    def delete_7_symbol(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)):
                list1[i] = ''
        return ''.join(list1)

    def delete_8_symbol(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)):
                list1[i] = ''
        return ''.join(list1)

    def delete_9_symbol(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)):
                list1[i] = ''
        return ''.join(list1)

    def delete_10_symbol(self, sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9, sign10):
        list1 = []
        list1.extend(str(self.string))

        for i in range(len(list1)):
            if (list1[i] == str(sign1)) | (list1[i] == str(sign2)) | (list1[i] == str(sign3)) | (list1[i] == str(sign4)) \
                    | (list1[i] == str(sign5)) | (list1[i] == str(sign6)) | (list1[i] == str(sign7)) | \
                    (list1[i] == str(sign8)) | (list1[i] == str(sign9)) | (list1[i] == str(sign10)):
                list1[i] = ''
        return ''.join(list1)


string = StringSort('[(0 ,.)0 ,8 ,1 ,9 ],')
print(string.delete_6_symbol('.', ',', '[', ']', '(', ')'))