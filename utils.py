
littleTextDict = {
    '1':'󰬺',
    '2':'󰬻',
    '3':'󰬼',
    '4':'󰬽',
    '5':'󰬾',
    '6':'󰬿',
    '7':'󰭀',
    '8':'󰭁',
    '9':'󰭂',
    '0':'.'
}

def littleDigits(txt):
    return ''.join([
        littleTextDict.get(i, i) for i in txt
    ])

def farsi_to_fingilish(farsi_text):
    # Dictionary mapping Farsi letters to Fingilish equivalents
    farsi_to_fingilish_map = {
        "ا": "a", "ب": "b", "پ": "p", "ت": "t",
        "ث": "s", "ج": "j", "چ": "ch", "ح": "h",
        "خ": "kh", "د": "d", "ذ": "z", "ر": "r",
        "ز": "z", "ژ": "zh", "س": "s", "ش": "sh",
        "ص": "s", "ض": "z", "ط": "t", "ظ": "z",
        "ع": "a", "غ": "gh", "ف": "f", "ق": "gh",
        "ک": "k", "گ": "g", "ل": "l", "م": "m",
        "ن": "n", "و": "v", "ه": "h", "ی": "y",
        "۰": "0", "۱": "1", "۲": "2", "۳": "3",
        "۴": "4", "۵": "5", "۶": "6", "۷": "7",
        "۸": "8", "۹": "9"
    }
    
    # Convert the Farsi text to Fingilish
    fingilish_text = "".join(farsi_to_fingilish_map.get(char, char) for char in farsi_text)

    return fingilish_text
