class TokenClassifier:
    """
    Token Classifier
    """

    # product list
    products = ['Red Shirt']

    def __init__(self):
        """ Constructor for this class. """

    @staticmethod
    def classify(token):
        classifications = []
        if not token:
            return classifications
        if TokenClassifier.is_quantity(token):
            classifications.append("Quantity")
        if TokenClassifier.is_product(token):
            classifications.append("Product")
        if TokenClassifier.is_price(token):
            classifications.append("Price")

    @staticmethod
    def is_quantity(token):
        """
        Check if given token is quantity
        :param token:
        :return: boolean
        """
        return token.isdigit()

    @staticmethod
    def is_product(token):
        """
        Check if the given string is product
        :return: boolean
        """
        return token in TokenClassifier.products

    @staticmethod
    def is_price(token):
        return token.isdecimal()
