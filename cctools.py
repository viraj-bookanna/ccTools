import re
from unidecode import unidecode

def cc_type(card_number):
  if card_number[0] == "4":
    return "visa"
  elif card_number[0:2] in ["34", "37"]:
    return "american_express"
  elif card_number[0:2] in ["51", "52", "53", "54", "55"]:
    return "master"
  elif card_number[0:4] == "6011":
    return "discover"
  else:
    return "default"
def luhn(n):
    r = [int(ch) for ch in str(n)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0
def find_cc(text):
    text = unidecode(text)
    cc_pattern = r'(?:^|[^0-9])(\d{15,19})(?:[^0-9]|$)'
    cc = re.search(cc_pattern, text)
    if not cc:
        cc = re.search(cc_pattern, re.sub(r'\s(\d{4})', r'\1', text))
    exp_pattern = r'(?:^|[^0-9])(?:(?:(\d{2}|20\d{2})([^0-9a-zA-Z])\2*?(\d{2}))|(?:(\d{2})([^0-9a-zA-Z])\5*?(\d{2}|20\d{2})))(?:[^0-9]|$)'
    exp = re.search(exp_pattern, text)
    if not exp:
        exp = re.search(exp_pattern, text.replace(' ', ''))
    if not exp:
        exp_pattern2 = r'(?:^|[^0-9])(?:(0\d|1[012])((?:20)?[23]\d))(?:[^0-9]|$)'
        exp = re.search(exp_pattern2, text)
        if exp:
            exp = re.search(exp_pattern, f"{exp[1]}|{exp[2]}")
    cvv_pattern = r'(?:^|[^0-9])(\d{3})(?:[^0-9]|$)'
    if cc and cc[1] and cc_type(cc[1]) in ["american_express"]:
        cvv_pattern = r'(?:^|[^0-9])(\d{4})(?:[^0-9]|$)'
    cvv = re.search(cvv_pattern, text)
    #print(cc, exp, cvv)
    if not cc or not exp or not cvv or not luhn(cc[1]):
        return None
    exp = [exp[1] if exp[1] else exp[4], exp[3] if exp[3] else exp[6]]
    if len(exp[0])==4 or not (exp[0].startswith('0') or exp[0].startswith('1')):
        y = exp[0]
        m = exp[1]
    else:
        y = exp[1]
        m = exp[0]
    y = y if len(y)==2 else y[2:]
    pipe =  '{}|{}|{}|{}'.format(cc[1], m, y, cvv[1])
    return (pipe, cc[1], m, y, cvv[1])
