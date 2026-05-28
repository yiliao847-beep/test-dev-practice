# test_first.py

def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5
    print("✓ 正数相加通过")

def test_add_negative():
    assert add(-1, -2) == -3
    print("✓ 负数相加通过")

def test_add_zero():
    assert add(0, 5) == 5
    print("✓ 零值相加通过")