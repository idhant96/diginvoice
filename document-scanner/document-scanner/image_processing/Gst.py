import re

class Gst:
    """
    Gst number formatting and validation
    """

    def __init__(self, gst_no):
        """ Constructor for this class. """
        # Create some member animals
        self.gst_no = gst_no

    def corrections(self):
        """
        Correct gst number if not right
        :return:
        """

        # convert string to list
        gst_list = list(self.gst_no)

        # first two characters should be digit
        gst_list[0] = Gst.digit(gst_list[0])
        gst_list[1] = Gst.digit(gst_list[1])

        # 3,4,5,6,7 should be alphabets
        gst_list[2] = Gst.alpha(gst_list[2])
        gst_list[3] = Gst.alpha(gst_list[3])
        gst_list[4] = Gst.alpha(gst_list[4])
        gst_list[5] = Gst.alpha(gst_list[5])
        gst_list[6] = Gst.alpha(gst_list[6])

        # 8,9,10,11 should be digit
        gst_list[7] = Gst.digit(gst_list[7])
        gst_list[8] = Gst.digit(gst_list[8])
        gst_list[9] = Gst.digit(gst_list[9])
        gst_list[10] = Gst.digit(gst_list[10])

        # 12 should be alphabet
        gst_list[11] = Gst.alpha(gst_list[11])

        # 13 should be digit
        gst_list[12] = Gst.digit(gst_list[12])

        # 14 should be digit
        gst_list[13] = 'Z'

        # 15 should be alpha
        gst_list[14] = Gst.alpha(gst_list[14])

        self.gst_no = ''.join(gst_list)

    @staticmethod
    def digit(char):
        """
        convert given character to digit if it is not
        :param char:
        :return:
        """
        if char.isalpha():
            return Gst.replace_similar(char)
        return char

    @staticmethod
    def alpha(char):
        """
        convert given character to digit if it is not
        :param char:
        :return:
        """
        if not char.isalpha():
            return Gst.replace_similar(char)
        return char

    @staticmethod
    def replace_similar(dig):
        """
        Replace characters with similar ones
        :param dig:
        :return:
        """
        if dig == 'S':
            return '5'
        elif dig == '5':
            return 'S'
        elif dig == 'Z':
            return '2'
        elif dig == '5':
            return 'Z'

    @staticmethod
    def find(para):
        """
        find text from substring from the paragraph
        :param para: paragraph to search from
        :return: return found string
        """
        m = re.search('[0-9A-Z]{15}', para)
        if m:
            return m.group(0)
        return None