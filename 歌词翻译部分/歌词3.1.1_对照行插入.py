import regex


patternTime = r"\[(?:[^][]+|(?R))*\]"
lines1 = []
while True:
    line = input().strip()
    if line == '结束':
        break
    lines1.append(line)

lines2 = []
while True:
    line = input().strip()
    if line == '结束':
        break
    elif line == '':
        continue
    elif not regex.sub(patternTime, "", line):
        continue
    lines2.append(line)

j = 0
for i in lines1:
    bracket_contents = regex.findall(patternTime, i)
    patternContent = regex.sub(patternTime, "", i)
    patternContent = patternContent.strip()

    if not i:
        print()
    else:
        print(bracket_contents[0], patternContent, sep='')

    for bc in bracket_contents:
        if not regex.sub(patternTime, "", i):
            continue
        print(bc + lines2[j])
        j += 1

#  可以去除不必要空格
