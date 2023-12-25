import pykakasi
import regex


def ignore_convert(text):
    pattern = r"\[(?:[^][]+|(?R))*\]"
    bracket_contents = regex.findall(pattern, text)
    for bc in bracket_contents:
        print(bc, end='')
    text = regex.sub(pattern, "", text)
    return text


def lyric_convert(text):
    kks = pykakasi.kakasi()
    for i in text:
        i = ignore_convert(i)
        result = kks.convert(i)
        output = ''
        for j in result:
            if j['orig'] == '':
                output += ''
            else:
                bracket = r"\(|\)"
                hepburn_str = regex.sub(bracket, "", j['hepburn'])
                if not hepburn_str or hepburn_str == ' ':
                    output += j['orig']
                else:
                    output += j['orig'] + '(' + hepburn_str + ')'
        print(output)


lines = []
while True:
    line = input().strip()
    if line == '结束':
        break
    lines.append(line)
lyric_convert(lines)
