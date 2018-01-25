import json
import re
import cv2


class Utils(object):

    @classmethod
    def formatter(cls, word):
        word = cls.cleaner(word)
        word = word.replace(' ', '')
        word = word.replace('.', '')
        word = word.replace('!', '')
        return word

    @classmethod
    def get_true_gst(cls, company):
        data = cls.get_data('pharma', 'pharma_list')
        for key in data.keys():
            if key == company:
                return data[key]['GSTIN'], data[key]['DLNO']
        return None

    @classmethod
    def check_gst_format(cls, word):
        if re.findall(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}', word):
            return ''.join(re.findall(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}', word))
        else:
            return None

    @classmethod
    def change_gst_letters(cls, subtext):
        final = ''
        try:
            subpart = subtext[0:2]
            if not subpart.isdigit():
                final = final + cls.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[2:7]
            if not subpart.isalpha():
                final = final + cls.to_alphabets(subpart)
            else:
                final = final + subpart
            subpart = subtext[7:11]
            if not subpart.isdigit():
                final = final + cls.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[11]
            if not subpart.isalpha():
                final = final + cls.to_alphabets(subpart)
            else:
                final = final + subpart
            subpart = subtext[12]
            if not subpart.isdigit():
                final = final + cls.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[13]
            if subpart is not 'Z':
                final = final + 'Z'
            else:
                final = final + subpart
            final = final + subtext[14].upper()
            # print(final)
            return final
        except IndexError:
            # print('Exception Handled')
            return final

    @classmethod
    def to_alphabets(cls, numbers):
        final = ''
        for number in numbers:
            if number.isalpha():
                final = final + number
            elif number == '1':
                final = final + 'I'
            elif number == '2':
                final = final + 'Z'
            elif number == '5':
                final = final + 'S'
            elif number == '8':
                final = final + 'B'
            elif number == '0':
                final = final + 'O'
            else:
                final = final + number
        return final

    @classmethod
    def to_digits(cls, characters):
        final = ''
        for character in characters:
            if character.islower():
                character = character.upper()
            if character.isdigit():
                final = final + character
            elif character == 'B':
                final = final + '8'
            elif character == 'S':
                final = final + '5'
            elif character == 'O':
                final = final + '0'
            elif character == 'I':
                final = final + '1'
            elif character == 'Z':
                final = final + '2'
            else:
                final = final + character
        return final

    @classmethod
    def get_data(cls, file_name, obj):
        with open('{}.json'.format(file_name)) as fh:
            data = json.load(fh)
        return data['{}'.format(obj)]

    @classmethod
    def cleaner(cls, st):
        st = st.encode('ascii', 'ignore').decode('utf-8')
        return re.sub(r'[(?|$|,+''"”*#:|!)]', r'', st)

