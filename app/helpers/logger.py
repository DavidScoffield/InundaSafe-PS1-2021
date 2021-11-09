import pprint


pp = pprint.PrettyPrinter(indent=2)


def logger_info(data):
    pp.pprint(" ## INFO ---------------------")
    pp.pprint(data)
    pp.pprint(" ## --------------------------")


def logger_error(data):
    pp.pprint(" ## ERROR ---------------------")
    pp.pprint(data)
    pp.pprint(" ## --------------------------")
