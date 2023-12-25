import regex

lines = []
patterns = {
    "0": (r"[\[\]]", r"\[(?:[^][]+|(?R))*\]"),
    "1": (r"[<>]", r"<(?:[^<>]+|(?R))*>"),
    "2": (r"[()]", r"\((?:[^()]+|(?R))*\)"),
    "3": (r"[「」]", r"「(?:[^「」]+|(?R))*」"),
    "4": (r"[【】]", r"【(?:[^【】]+|(?R))*】")
}

while True:
    line = input().strip()
    if line == '结束':
        break
    lines.append(line)

judge1 = input("是否删除括号内的内容（0表示只删去括号本身，1表示将嵌套括号内的所有内容删除）：")
judge2 = input("括号类型是？0表示[]，1<>，2表示()，3表示「」，4表示【】：")

for line in lines:
    result = regex.sub(patterns[judge2][int(judge1)], "", line)
    print(result)
