def main():
    txt_path = "F:\\Desktop\\EnglishText\\EnglishText.txt"  # 指定TXT文件路径

    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：未找到文件 {txt_path}，请检查路径是否正确。")
        return
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return

    units = {}
    current_unit = None
    current_question = None
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 识别单元标题（如U1, U2）
        if line.startswith('U') and line[1:].isdigit():
            current_unit = line
            units[current_unit] = []
            continue

        # 识别题目（支持1. 2. ... 9. 10.等任意数字编号）
        if current_unit and any(line.startswith(f'{i}.') for i in range(1, 100)):
            if current_question:
                units[current_unit].append(current_question)
            current_question = {'question': line[2:].strip(), 'options': [], 'answer': ''}
            continue

        # 识别选项（A. B. C. D.）
        if current_question and (line.startswith('A.') or line.startswith('B.') or
                                 line.startswith('C.') or line.startswith('D.')):
            current_question['options'].append(line)
            continue

        # 识别答案（支持中文和英文冒号）
        if current_question and ('答案：' in line or '答案:' in line):
            answer = line.split('答案：')[-1].split('答案:')[-1].strip()
            if answer in ['A', 'B', 'C', 'D']:
                current_question['answer'] = answer

    # 处理最后一个题目
    if current_unit and current_question:
        units[current_unit].append(current_question)

    print("===== 大学英语词汇练习题 ===== made by 晕吖")

    while True:
        print("\n请选择练习单元 (U1-U12)，输入q退出程序:")
        available_units = sorted(units.keys())
        if available_units:
            print(", ".join(available_units))
        else:
            print("未找到任何题目数据，请检查文件格式是否正确。")
            break

        choice = input("\n你的选择: ").upper()

        if choice == 'Q':
            print("感谢使用，再见！")
            break

        if choice in units and units[choice]:
            print(f"\n开始单元 {choice} 的练习...")
            correct_count = 0
            total_questions = len(units[choice])
            question_index = 0  # 用于记录当前题目索引

            while question_index < total_questions:
                q = units[choice][question_index]
                print(f"\n===== 单元 {choice} - 题目 {question_index+1}/{total_questions} =====")
                print(q['question'])
                for option in q['options']:
                    print(option)

                user_answer = input("\n请输入你的答案 (A/B/C/D)，输入q退出当前单元: ").upper()

                if user_answer == 'Q':
                    print(f"你选择退出单元 {choice} 的练习")
                    break  # 退出当前单元练习

                if user_answer == q['answer']:
                    print("恭喜！答案正确！")
                    correct_count += 1
                else:
                    print(f"答案错误。正确答案是: {q['answer']}")
                    if q['options']:
                        correct_option = [opt for opt in q['options'] if opt.startswith(q['answer'] + '.')]
                        if correct_option:
                            print(f"解析: {correct_option[0]}")

                question_index += 1  # 移动到下一题

            if question_index == total_questions:  # 完成所有题目
                print(f"\n单元 {choice} 练习完成！")
                print(f"正确题数: {correct_count}/{total_questions}，正确率: {(correct_count / total_questions) * 100:.2f}%")
        else:
            print("无效的选择或该单元没有题目，请重新输入。")


if __name__ == "__main__":
    main()