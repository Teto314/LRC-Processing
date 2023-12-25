import regex
import os


def process_lines(lines):
    origin_lines = []
    chinese_lines = []
    empty_lines_count = 0
    parity_line = False

    patternTime = r"\[(?:[^][]+|(?R))*\]"

    for i in range(len(lines)):
        line = lines[i]
        matches = regex.findall(patternTime, line)

        if matches:
            line = line.strip()
            line = regex.sub("\u200b", "", line)
            line = regex.sub("\ufeff", "", line)

            if not regex.sub(patternTime, "", line):
                origin_lines.append(line)
                chinese_lines.append(line)
                continue

            if not parity_line:
                origin_lines.append(line)
                parity_line = not parity_line
            else:
                chinese_lines.append(line)
                parity_line = not parity_line
        else:
            empty_lines_count += 1

    return origin_lines, chinese_lines, empty_lines_count


def process_lrc_file(input_file, output_folder):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    origin_lines, chinese_lines, empty_lines_count = process_lines(lines)

    origin_output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}-O.lrc")
    chinese_output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}-T.lrc")

    with open(origin_output_file, "w", encoding="utf-8") as file:
        for line in origin_lines:
            file.write(line + "\n")

    with open(chinese_output_file, "w", encoding="utf-8") as file:
        for line in chinese_lines:
            file.write(line + "\n")

    print(f"处理完成: {input_file}")
    if empty_lines_count != 0:
        print(f"提示！跳过 {empty_lines_count} 行空行")

    if len(chinese_lines) != len(origin_lines):
        err = len(chinese_lines) - len(origin_lines)
        print("\n警告！\n有", err // 2, "行原文被误识为译文，请检查输出", sep='')


def main():
    output_folder = "cache"
    os.makedirs(output_folder, exist_ok=True)

    lrc_files = [f for f in os.listdir() if f.endswith(".lrc")]

    for lrc_file in lrc_files:
        process_lrc_file(lrc_file, output_folder)


if __name__ == "__main__":
    main()
