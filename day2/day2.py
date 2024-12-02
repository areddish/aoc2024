import pyperclip
answer_part = 1
def answer(v):
    global answer_part
    pyperclip.copy(v)
    print("Part 1 =" if answer_part == 1 else "Part 2 =", v)
    answer_part = 2

def check_safe(vals):
    inc_count = 0
    dec_count = 0
    diff_count = 0
    prev = vals[0]
    for v in vals[1:]:
        diff = v - prev
        if diff > 0:
            inc_count += 1
        elif diff < 0:
            dec_count += 1
        diff = abs(diff)
        if (1 <= diff <= 3):
            diff_count += 1
        prev = v
    #print(vals, inc_count, dec_count, min_diff, max_diff, inc_count or dec_count or (min_diff >= 1 and max_diff <= 3))
    return (diff_count == len(vals)-1) and (inc_count == len(vals)-1 or dec_count == len(vals)-1)

#with open("test.txt") as file:
with open("day2.txt") as file:
    lines = file.read().strip().splitlines()

    ans = 0
    ans2 = 0
    for l in lines:
        vals = [int(x) for x in l.split()]
        if check_safe(vals):
            ans += 1

        for i in range(len(vals)):
            if check_safe(vals[:i]+vals[i+1:]):
                ans2 += 1
                break
    answer(ans)
    answer(ans2)