def sign(num):
    return 0 if num==0 else int(num/abs(num))
# why does python not have sign already I have no idea


def getPercentage(num, full):
    return (num/full)*100
def getIntPercentage(num, full):
    return int((num/full)*100)