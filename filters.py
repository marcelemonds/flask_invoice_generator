import locale


def currencyFormat(value):
    value = float(value)
    if value == 0:
        return "- €"
    else:
        return "{:,.2f} €".format(float(value)).replace('.', '_').replace(',', '.').replace('_', ',')
