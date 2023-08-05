# 找一个数所有的因数
def factor(num):
    factors = []
    for i in range(num-1):
        i += 1
        if num % i == 0:
            factors.append(i)
    factors.append(num)
    return factors

# 判断一个数是否为完全数
def per_num(num):
    sum = 0
    factors = factor(num)
    for i in range(len(factors)-1):
        sum += factors[i]
    if sum == num:
        return True

# 判断一个数是否为质数
def pri_num(num):
    if len(factor(num)) == 2:
        return True
    else:
        return False

# 判断一个数是否为偶数
def even_num(num):
    if num %2 == 0:
        return True
    else:
        return False

# （最大）公因数
def hcf(num_list):
    common_f = []
    for i in factor(num_list[0]):
        common = True
        for j in num_list:
            if not i in factor(j):
                common = False
        if common:
                common_f.append(i)
    return common_f, max(common_f)

# 注意：本函数会返回两个值：两个数的公因数和最大公因数；请在该函数的参数内传入一个包含两个或以上数字的列表！

# （最小）公倍数
def lcm(num_list):
    i = 1
    common = False
    while not common:
        common = True
        now_num = num_list[0]*i
        for j in num_list:
            if not now_num % j == 0:
                common = False
        i += 1
    return now_num

# 注意：请在该函数的参数内传入一个包含两个或以上数字的列表！

# 分解质因数
def pri_fac(num):
    pri_factors = []
    now_num = num
    while not pri_num(now_num):
        pri_factor = factor(now_num)[1]
        now_num = int(now_num/pri_factor)
        pri_factors.append(pri_factor)
    pri_factors.append(now_num)
    if pri_factors:
        text = '{} = '.format(num)
        for i in pri_factors:
            text += '{}*'.format(i)
        text += '1'
    else:
        text = '{} = {}'.format(num, num)
    return text

# 互质数
def coprime(num_list):
    if len(hcf(num_list)) == 1:
        return True
    else:
        return False

# 注意：请在该函数的参数内传入一个长度大于1的列表
