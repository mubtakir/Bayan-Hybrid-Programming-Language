"""
Tests for Arabic text handling
اختبارات لمعالجة النصوص العربية

This test suite verifies that Bayan handles Arabic text correctly:
1. Character joining (الحروف المتصلة)
2. RTL (Right-to-Left) text direction
3. Bidirectional text (Arabic + English)
4. Arabic numerals vs. Western numerals
5. Diacritics (التشكيل)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bayan'))

import pytest
from bayan import HybridLexer, HybridParser, HybridInterpreter


def test_arabic_string_basic():
    """Test basic Arabic string handling"""
    code = """
name = "محمد"
greeting = "مرحباً"
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['name'] == "محمد"
    assert interpreter.traditional.global_env['greeting'] == "مرحباً"


def test_arabic_character_joining():
    """Test that Arabic characters are properly joined (not separated)"""
    code = """
# Test connected letters
word1 = "سلام"  # س + ل + ا + م (should be connected)
word2 = "كتاب"  # ك + ت + ا + ب (should be connected)
word3 = "مدرسة"  # م + د + ر + س + ة (should be connected)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    # Verify that the strings are stored correctly
    assert interpreter.traditional.global_env['word1'] == "سلام"
    assert interpreter.traditional.global_env['word2'] == "كتاب"
    assert interpreter.traditional.global_env['word3'] == "مدرسة"
    
    # Verify character count (not byte count)
    assert len(interpreter.traditional.global_env['word1']) == 4
    assert len(interpreter.traditional.global_env['word2']) == 4
    assert len(interpreter.traditional.global_env['word3']) == 5


def test_arabic_with_diacritics():
    """Test Arabic text with diacritics (التشكيل)"""
    code = """
# Text with diacritics
text1 = "مَرْحَباً"  # مرحباً with diacritics
text2 = "الْعَرَبِيَّة"  # العربية with diacritics
text3 = "بِسْمِ اللهِ"  # بسم الله with diacritics
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    # Verify that diacritics are preserved
    assert interpreter.traditional.global_env['text1'] == "مَرْحَباً"
    assert interpreter.traditional.global_env['text2'] == "الْعَرَبِيَّة"
    assert interpreter.traditional.global_env['text3'] == "بِسْمِ اللهِ"


def test_bidirectional_text():
    """Test bidirectional text (Arabic + English)"""
    code = """
# Mixed Arabic and English
text1 = "Hello مرحباً"
text2 = "Python لغة برمجة"
text3 = "عمري 25 سنة"
text4 = "Bayan هي لغة برمجة عربية"
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    # Verify that bidirectional text is stored correctly
    assert interpreter.traditional.global_env['text1'] == "Hello مرحباً"
    assert interpreter.traditional.global_env['text2'] == "Python لغة برمجة"
    assert interpreter.traditional.global_env['text3'] == "عمري 25 سنة"
    assert interpreter.traditional.global_env['text4'] == "Bayan هي لغة برمجة عربية"


def test_arabic_numerals():
    """Test Arabic numerals (٠١٢٣٤٥٦٧٨٩) vs Western numerals (0123456789)"""
    code = """
# Western numerals in Arabic text
text1 = "عمري 25 سنة"
text2 = "السعر 100 ريال"

# Arabic-Indic numerals
text3 = "عمري ٢٥ سنة"
text4 = "السعر ١٠٠ ريال"
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    # Verify that both numeral systems are supported
    assert interpreter.traditional.global_env['text1'] == "عمري 25 سنة"
    assert interpreter.traditional.global_env['text2'] == "السعر 100 ريال"
    assert interpreter.traditional.global_env['text3'] == "عمري ٢٥ سنة"
    assert interpreter.traditional.global_env['text4'] == "السعر ١٠٠ ريال"


def test_arabic_string_operations():
    """Test string operations with Arabic text"""
    code = """
# String concatenation
first = "محمد"
last = "أحمد"
full_name = first + " " + last

# String length
name_length = len(full_name)

# String comparison
same = (first == "محمد")
different = (first == "أحمد")
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['full_name'] == "محمد أحمد"
    assert interpreter.traditional.global_env['name_length'] == 9  # 4 + 1 + 4
    assert interpreter.traditional.global_env['same'] == True
    assert interpreter.traditional.global_env['different'] == False


def test_arabic_in_lists():
    """Test Arabic text in lists"""
    code = """
# List of Arabic names
names = ["محمد", "فاطمة", "علي", "زينب"]

# Access elements
first_name = names[0]
last_name = names[3]

# List length
count = len(names)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['names'] == ["محمد", "فاطمة", "علي", "زينب"]
    assert interpreter.traditional.global_env['first_name'] == "محمد"
    assert interpreter.traditional.global_env['last_name'] == "زينب"
    assert interpreter.traditional.global_env['count'] == 4


def test_arabic_in_dicts():
    """Test Arabic text in dictionaries"""
    code = """
# Dictionary with Arabic keys and values
person = {
    "الاسم": "محمد",
    "العمر": 30,
    "المدينة": "القاهرة"
}

# Access values
name = person["الاسم"]
city = person["المدينة"]
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    person = interpreter.traditional.global_env['person']
    assert person["الاسم"] == "محمد"
    assert person["العمر"] == 30
    assert person["المدينة"] == "القاهرة"
    
    assert interpreter.traditional.global_env['name'] == "محمد"
    assert interpreter.traditional.global_env['city'] == "القاهرة"


def test_arabic_identifiers():
    """Test Arabic variable names and function names"""
    code = """
# Arabic variable names
الاسم = "محمد"
العمر = 25
المدينة = "الرياض"

# Arabic function names
def احسب_المجموع(أ, ب):
{
    return أ + ب
}

النتيجة = احسب_المجموع(10, 20)
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['الاسم'] == "محمد"
    assert interpreter.traditional.global_env['العمر'] == 25
    assert interpreter.traditional.global_env['المدينة'] == "الرياض"
    assert interpreter.traditional.global_env['النتيجة'] == 30


def test_arabic_comments():
    """Test Arabic text in comments"""
    code = """
# هذا تعليق عربي
x = 10  # متغير للعدد

# التعليقات العربية يجب أن تعمل بشكل صحيح
# ولا تؤثر على تنفيذ البرنامج
y = 20
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['x'] == 10
    assert interpreter.traditional.global_env['y'] == 20


def test_arabic_multiline_strings():
    """Test multiline strings with Arabic text"""
    code = '''
# Multiline string with Arabic
text = """
هذا نص
متعدد الأسطر
بالعربية
"""
'''
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    text = interpreter.traditional.global_env['text']
    assert "هذا نص" in text
    assert "متعدد الأسطر" in text
    assert "بالعربية" in text


def test_arabic_escape_sequences():
    """Test escape sequences in Arabic strings"""
    code = """
# Newline in Arabic text
text1 = "السطر الأول\\nالسطر الثاني"

# Tab in Arabic text
text2 = "العمود الأول\\tالعمود الثاني"
"""
    lexer = HybridLexer(code)
    tokens = lexer.tokenize()
    parser = HybridParser(tokens)
    ast = parser.parse()
    interpreter = HybridInterpreter()
    interpreter.interpret(ast)
    
    assert interpreter.traditional.global_env['text1'] == "السطر الأول\nالسطر الثاني"
    assert interpreter.traditional.global_env['text2'] == "العمود الأول\tالعمود الثاني"

