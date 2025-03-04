import re


def int_to_roman(num):
    num_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    roman = ""

    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i

    return roman


regex_roman_numbers = re.compile("(^M{0,4}(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}) [-–] )")


def process_markdown(lines: list[str]):
    article_counter = 1
    in_paragraph, paragraph_counter = False, 1
    in_item, item_counter = False, 1

    for index, line in enumerate(lines):
        is_paragraph = line.startswith("§")
        is_item = regex_roman_numbers.match(line)
        if is_paragraph:
            lines[index] = re.sub(r"§ \d+º", f"§ {paragraph_counter}º", line)
            paragraph_counter += 1
        elif is_item:
            found_roman_entry = is_item.groups()[0]
            cleaned_line = line.replace(found_roman_entry, "")
            lines[index] = f"{int_to_roman(item_counter)} – {cleaned_line}"
            item_counter += 1
        else:
            is_title = line.startswith("##")
            is_article = line.strip() and not is_title
            if is_article:
                paragraph_counter = 1
                item_counter = 1
                line = re.sub(r"^Art. \d+[.]{0,1} ", "", line)
                lines[index] = f"Art. {article_counter}. {line}"
                article_counter += 1

    return lines


def handle(file: str):
    with open(file, "r", encoding="utf-8") as target_file:
        target_lines = target_file.readlines()
    constitution_start_index = target_lines.index("## TÍTULO I - Máximas\n")
    constitution_end_index = target_lines.index("## Referências\n")
    lines_to_be_processed = target_lines[constitution_start_index:constitution_end_index]
    updated_lines = process_markdown(lines_to_be_processed)
    completed_lines = target_lines[:constitution_start_index] + updated_lines + target_lines[constitution_end_index:]
    with open(file, "w", encoding="utf-8") as target_file:
        target_file.writelines(completed_lines)


if __name__ == "__main__":
    handle("README.md")
