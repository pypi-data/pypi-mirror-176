import re
import chinese_converter


def split_eng_cn(input):
    cn = re.findall(r'[\u4e00-\u9fff]+', input)
    cn_text = ''
    if cn != None:
        for n in cn:
            cn_text += ' '
            cn_text += n
            input = input.replace(n, '')
    eng = input
    # string = '' if eng/cn not found in text
    return eng, chinese_converter.to_simplified(cn_text)
