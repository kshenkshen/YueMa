import sys

def twoSum(num, target):
    dic = dict()
    dic[num[0]] = 0
    for index in range(1, len(num)):
        if dic.has_key(target - num[index]):
            return dic[target - num[index]] + 1, index +1
        else:
            dic.setdefault(num[index], index)

if __name__ == "__main__":
    target = int(raw_input())
    l = []
    for line in sys.stdin:
        l.append(int(line))
    print '{} {}'.format(*twoSum(l, target))
