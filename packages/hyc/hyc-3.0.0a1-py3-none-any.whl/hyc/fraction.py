from hyc.num import coprime, hcf, lcm

# 分数类
class fraction:
    def __init__(self, a, b):
        self.fraction = [a, b]

    # 分数化整数（保留到个位）
    def __int__(self):
        if self.fraction[1] > self.fraction[0]:
            num = self.fraction[1]//self.fraction[0]
        else:
            num = 0
        return num

    # 读作
    def __str__(self):
        string = '{}分之{}'.format(self.fraction[0], self.fraction[1])
        return string

    # 分数化小数（可选择保留位数，不选则不四舍五入）
    def __float__(self, rounding: int=False):
        decimal = self.fraction[0]/self.fraction[1]
        if rounding:
            decimal = round(decimal, rounding)
        return decimal

    # 约分
    def red_fr(self):
        if self.simp_fr():
            return self
        else:
            _, common_div = hcf(self.fraction)
            for i in range(2):
                self.fraction[i] = self.fraction[i]//common_div
            return fraction(self.fraction[0], self.fraction[1])

    # 最简分数
    def simp_fr(self):
        if coprime(self.fraction):
            return True
        else:
            return False

    # 倒数
    def opposide(self):
        fraction_opposide = fraction(self.fraction[1], self.fraction[0])
        return fraction_opposide

    # 分数加法
    def __add__(self, other: list):
        result = 0
        fraction_list = den_di([self]+other)
        for i in fraction_list:
            result += i.fraction[1]
        fraction_sum = fraction(fraction_list[0].fraction[0], result)
        return fraction_sum.red_fr()


    # 分数减法
    def __sub__(self, other: list):
        if len(other) > 1:
            for i in other:
                subtracted += i
        else:
            subtracted = other[0]
        new_minuend, new_subtracted = den_di([self, subtracted])
        new_minuend.fraction[1]-=new_subtracted.fraction[1]
        return new_minuend.red_fr()

    # 分数乘法
    def __mul__(self, other: list):
        deno = 1
        mole = 1
        other_fraction = []
        for i in other:
            other_fraction.append(i.fraction)

        for i in [self.fraction]+other_fraction:
            deno*=i[0]
            mole*=i[1]
        result = fraction(deno,mole)
        return result.red_fr()

    # 分数除法
    def __truediv__(self, other: list):
        divisor = fraction(1, 1)
        for i in other:
            divisor *= [i]

        divisor = fraction(divisor.fraction[0], divisor.fraction[1])
        result = self*[divisor.opposide()]
        return result.red_fr()

# 通分
def den_di(fraction_list: list[fraction]):
    all_deno = []
    for i in fraction_list:
        all_deno.append(i.fraction[0])
        common_deno = lcm(all_deno)
    new_fraction_list = []
    for i in fraction_list:
        common_mul = int(common_deno/i.fraction[0])
        i = fraction(i.fraction[0]*common_mul, i.fraction[1]*common_mul)
        new_fraction_list.append(i)
    return new_fraction_list
