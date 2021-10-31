import pprint


pp = pprint.PrettyPrinter(indent=2)


def looger_error(data):
    pp.pprint(" ## INFO ---------------------")
    pp.pprint(data)
    pp.pprint(" ## --------------------------")


def looger_error(data):
    pp.pprint(" ## ERROR ---------------------")
    pp.pprint(data)
    pp.pprint(" ## --------------------------")
