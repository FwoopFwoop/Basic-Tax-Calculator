class Bracket:
    # rate as a percentage
    rate = 0
    # bracket cap (or false for all)
    cap = False

    def __init__(self, rate, cap):
        self.cap = cap
        self.rate = rate


class TaxSystem:
    # list of brackets in ascending order
    brackets = []
    standard_deduction = 0
    personal_exemption = 0

    def __init__(self, brackets, standard_deduction, personal_exemption):
        self.brackets = brackets
        self.standard_deduction = standard_deduction
        self.personal_exemption = personal_exemption


# shorthand for making brackets
def br(rate, cap):
    return Bracket(rate, cap)


current_rates = (.1, .15, .25, .28, .33, .396)
house_rates = (.12, .25, .35, .396)
senate_rates = (.1, .12, .22, .24, .32, .35, .385)
final_rates = (.1, .12, .22, .24, .32, .35, .37)

current_single = TaxSystem(list(map(br, current_rates, [9325, 27950, 91900, 191650, 416700, 418400, False])),
                           6350, 4050)
current_joint = TaxSystem(list(map(br, current_rates, [18650, 75900, 153100, 233350, 416700, 47000, False])),
                          12700, 8100)

house_single = TaxSystem(list(map(br, house_rates, [45000, 200000, 500000, False])),
                         12200, 0)
house_joint = TaxSystem(list(map(br, house_rates, [90000, 260000, 1000000, False])),
                        24400, 0)

senate_single = TaxSystem(list(map(br, senate_rates, [9525, 38700, 70000, 160000, 200000, 500000, False])),
                          12000, 0)
senate_joint = TaxSystem(list(map(br, senate_rates, [19050, 77400, 140000, 320000, 400000, 1000000, False])),
                         24000, 0)

final_single = TaxSystem(list(map(br, final_rates, [9525, 38700, 70000, 160000, 200000, 500000, False])),
                         12000, 0)
final_joint = TaxSystem(list(map(br, final_rates, [19050, 77400, 165000, 315000, 400000, 600000, False])),
                        24000, 0)


def tax_paid(income, people, tax_system):
    def calculate(money, brackets, base, tax):
        # Base case for taking whatever income is left
        if not brackets[0].cap:
            return tax + brackets[0].cap * money
        else:
            taxable_amount = brackets[0].cap - base
            new_base = brackets[0].cap
            rate = brackets[0].rate
            if taxable_amount > money:
                return tax + rate * money
            else:
                return calculate(money - taxable_amount, brackets[1:], new_base, rate * taxable_amount)

    exemption = people * tax_system.personal_exemption + tax_system.standard_deduction
    if exemption > income:
        return 0
    else:
        return calculate(income - exemption, tax_system.brackets, 0, 0)
