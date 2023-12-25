import os
import regex


def generate_track_values(cache_folder='cache'):
    # 获取 cache 文件夹下所有的 lrc 文件
    lrc_files = [file for file in os.listdir(cache_folder) if file.endswith(('-O.lrc', '-T.lrc'))]

    # 确定待生成字幕数
    num_subtitles = len(lrc_files) // 2

    # 询问用户是否默认 "Disc" 为 1
    default_disc = input(
        f"待生成的字幕数为 {num_subtitles}，默认 Disc 为 1\n按回车确认，若为其他值，请在此输入：")
    disc = int(default_disc) if default_disc else 1

    # 提示用户输入 BPM
    bpm_values_demo = []
    for i, original_file in enumerate(lrc_files[::2]):  # 步长为2，处理原文文件
        # 提取文件名中的数字，即 Track 的值
        track = regex.search(r'\d+', original_file).group()

        # 验证 translated_lrc_file 是否匹配
        translated_file = original_file.replace('-O.lrc', '-T.lrc')
        corresponding_translated_lrc_file = regex.sub(r'\d+', track, translated_file)
        if corresponding_translated_lrc_file not in lrc_files:
            raise ValueError(f"未找到匹配的翻译文件，原文文件：{original_file}，翻译文件：{translated_file}")

        # 计算 Track 的值
        track_value_demo = "{}.{}".format(disc, track)
        bpm_input = input(f"\n请输入 Track {track_value_demo} 的 BPM 值：")
        bpm_values_demo.append(bpm_input)

    # 处理每一组 lrc 文件，生成 Track 的值和完整路径
    track_list = []
    lrc_paths = []
    for i in range(0, len(lrc_files), 2):
        original_file = lrc_files[i]
        track = regex.search(r'\d+', original_file).group()

        # 计算 Track 的值
        track_value_demo = "{}.{}".format(disc, track)
        track_list.append(track_value_demo)

        # 构建完整路径
        original_lrc_path = os.path.join(cache_folder, original_file)
        translated_lrc_path = os.path.join(cache_folder, original_file.replace('-O.lrc', '-T.lrc'))
        lrc_paths.append((original_lrc_path, translated_lrc_path))

    return track_list, lrc_paths, bpm_values_demo


def read_lrc_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lrc_content_read = file.read()
    return lrc_content_read


def parse_lrc_content(lrc_content_input):
    metadata_main = {}
    lyrics_main = []
    lines = lrc_content_input.split('\n')  # 将LRC内容按行拆分
    i = 0
    for line in lines:
        line = line.strip()  # 去除行首尾的空白字符
        if line.startswith('[') and line.endswith(']') and (
                line[3] != ':' or line[6] != '.') and i < 4:  # 我默认你只有4行注释，且首行字幕不是空行
            # 解析元数据
            key, value = line[1:-1].split(':', 1)
            metadata_main[key.strip()] = value.strip()
            i += 1
        elif line:
            # 解析歌词时间轴和文本内容
            timestamp, text = line.split(']', 1)
            timestamp = timestamp[1:]
            lyrics_main.append((timestamp.strip(), text.strip()))
    return metadata_main, lyrics_main


def convert_to_ass_format(lyrics_ass, source):
    ass_content_main = ""

    # 判断是否为原文，如果是，则添加[Events]和Format
    if source == "O":
        ass_content_main += "\n[Events]\n"
        ass_content_main += "Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n"

    # 添加歌词内容
    i = 0
    while i < len(lyrics_ass):
        timestamp, text = lyrics_ass[i]
        start_time = timestamp
        next_timestamp = lyrics_ass[i + 1][0] if i < len(lyrics_ass) - 1 else timestamp
        end_time = next_timestamp
        style = "LOL12JP" if source == "O" else "LOL12CN"
        ass_content_main += "Dialogue: 0,{0},{1},{2},NTP,0,0,0,,{3}\n".format(start_time, end_time, style, text)
        i += 1

    return ass_content_main


def create_ass_header(metadata_assh):
    ass_header_main = ""

    # 创建[Script Info]段
    ass_header_main += "[Script Info]\n"
    ass_header_main += "Title: {}\n".format(metadata_assh.get("ti", ""))
    ass_header_main += "Artist: {}\n".format(metadata_assh.get("ar", ""))
    ass_header_main += "Album: {}\n".format(metadata_assh.get("al", ""))
    ass_header_main += "By: {}\n".format(metadata_assh.get("by", ""))
    ass_header_main += "PlayResX: 3840\n"
    ass_header_main += "PlayResY: 2160\n"

    # 创建[V4+ Styles]段
    ass_header_main += "\n[V4+ Styles]\n"
    ass_header_main += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    ass_header_main += "Style: Title,Agency FB,120,&H00FFFFFF,&HF0FFFFFF,&H00000000,&HF0838383,0,0,0,0,115,100,2,0,1,0,0,2,1900,0,1500,1\n"
    ass_header_main += "Style: LOL12CN,GenWanMin TW TTF Medium,90,&H00FFFFFF,&HF0FFFFFF,&H00000000,&HF0838383,0,0,0,0,100,100,2.5,0,1,0,0,8,1920,0,1640,134\n"
    ass_header_main += "Style: LOL12JP,GenWanMin JP TTF Medium,90,&H00FFFFFF,&HF0FFFFFF,&H00000000,&HF0838383,0,0,0,0,100,100,2.5,0,1,0,0,8,1920,0,1475,128\n"
    ass_header_main += "Style: Script,Microsoft YaHei UI,85,&H00DFDDDD,&HF0FFFFFF,&H00000000,&HF0838383,0,-1,0,0,100,100,0,0,1,0,0,2,1920,0,190,1\n"
    ass_header_main += "Style: Script - s,Microsoft YaHei UI,85,&H00DFDDDD,&HF0FFFFFF,&H00000000,&HF0838383,-1,-1,0,0,100,100,0,0,1,0,0,2,1920,0,305,1\n"

    return ass_header_main


def convert_lyrics_time(ass_content_lt):
    lines = ass_content_lt.split('\n')
    converted_lines = []

    for i, line in enumerate(lines):
        if line.startswith("Dialogue:"):
            parts = line.split(",")
            start_time = convert_time(parts[1])  # 去除中括号并将小数点替换为冒号
            end_time = convert_time(parts[2])  # 去除中括号并将小数点替换为冒号
            hours, minutes, seconds = end_time.split(":")
            seconds, milliseconds = seconds.split(".")
            hours = int(hours)
            milliseconds = int(milliseconds)
            seconds = int(seconds)
            minutes = int(minutes)

            # 这里是想要将字幕结束时间（百分秒）稍减，让每句之间留出空隙
            interval = 7
            if milliseconds < interval:
                # 秒数减一
                if seconds == 0:
                    # 若秒数为00，则进行退位操作
                    if minutes == 0 and hours == 1:
                        hours -= 1
                        minutes = 59
                        seconds = 59
                    # 进行分钟数减一和秒数设为59的操作
                    else:
                        minutes -= 1
                        seconds = 59
                else:
                    # 秒数减一
                    seconds -= 1
                # 执行减法操作
                milliseconds -= interval
                # 处理借位情况
                if milliseconds < 0:
                    milliseconds += 100
            else:
                milliseconds -= interval

            # 重新格式化为字符串时间表示
            end_time = "{:01d}:{:02d}:{:02d}.{:02d}".format(hours, minutes, seconds, milliseconds)
            if i == len(lines) - 2:  # 如果是最后一行
                end_time = "9:59:59.99"
            converted_line = ",".join(parts[:1] + [start_time, end_time] + parts[3:])
            converted_lines.append(converted_line)
        else:
            converted_lines.append(line)

    return "\n".join(converted_lines)


def convert_time(timestamp):
    minutes, seconds = timestamp.split(":")
    seconds, milliseconds = seconds.split(".")
    hours = "0"
    if int(minutes) >= 60:
        hours = 1  # 计算小时数
        minutes = str(int(minutes) % 60).zfill(2)  # 计算剩余的分钟数

    converted_time = "{}:{}:{}.{}".format(hours, minutes, seconds, milliseconds)
    return converted_time


def save_ass_file(ass_content_save, track_value_demo, cache_folder='cache'):
    # 获取 cache 文件夹的上层目录作为输出路径
    output_folder = os.path.dirname(os.path.abspath(cache_folder))

    # 构建保存文件的完整路径，使用 track_value 作为文件名
    file_name = f"{track_value_demo}.ass"
    file_path = os.path.join(output_folder, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ass_content_save)


# 主代码
# 调用函数获取 Track 的值列表和 lrc 文件的完整路径
track_values, lrc_file_paths, bpm_values = generate_track_values()
# 读取 lrc 文件
for (original_lrc_file, translated_lrc_file), track_value, bpm_value in zip(lrc_file_paths, track_values, bpm_values):
    lrc_content_original = read_lrc_file(original_lrc_file)
    lrc_content_translated = read_lrc_file(translated_lrc_file)

    # 读取原文歌词
    metadata, lyrics_original = parse_lrc_content(lrc_content_original)
    # 读取译文歌词
    _, lyrics_translated = parse_lrc_content(lrc_content_translated)  # metadata 是相同的，选择其中一个即可

    # 创建 ASS 文件的头部信息
    ass_header = create_ass_header(metadata)

    # 去除音轨号前面的零
    cleaned_track_value = '.'.join(str(int(part)) for part in track_value.split('.'))
    # 生成标题字幕
    title_subtitle = 'Dialogue: 0,0:00:00.00,9:59:59.99,Title,,0,0,0,,{}\\NBy: {}  Track: {}\\NBPM: {}\n'.format(
        metadata.get('ti', ''), metadata.get('ar', ''), cleaned_track_value, bpm_value)

    # 生成原文歌词的 ASS 内容
    ass_content_original = convert_lyrics_time(convert_to_ass_format(lyrics_original, source="O"))
    # 生成译文歌词的 ASS 内容
    ass_content_translated = convert_lyrics_time(convert_to_ass_format(lyrics_translated, source="T"))
    
    # 将头部信息和两份歌词内容拼接在一起
    ass_content = ass_header + ass_content_original + ass_content_translated + title_subtitle

    save_ass_file(ass_content, track_value, cache_folder='cache')
