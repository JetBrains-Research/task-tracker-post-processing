ans = input()
if (len(ans) > 2):
    if ((len(ans) % 2) == 0):
        ans = ('('.join(ans[:int((len(ans) / 2))]) + ')'.join(ans[int((len(ans) / 2)):]))
    else:
        ans = (('('.join(ans[:(int((len(ans) / 2)) + 1)]) + ')') + ')'.join(ans[int(((len(ans) / 2) + 1)):]))
print(ans)