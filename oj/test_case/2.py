n = int(raw_input())

ans = 0.0
for item in range(n):
    l = raw_input().split()
    ans = ans + float(l[0])  * float(l[1]) / 10.0

print "%.2f\n" %ans

