# Contributing to Bayan Programming Language
# المساهمة في لغة البيان البرمجية

<div dir="rtl">

## 🙏 شكراً لاهتمامك بالمساهمة!

نرحب بجميع المساهمات في لغة البيان! سواء كنت تريد إصلاح خطأ، إضافة ميزة جديدة، تحسين الوثائق، أو حتى مجرد الإبلاغ عن مشكلة.

</div>

---

## 🌟 Ways to Contribute | طرق المساهمة

### 1. Report Bugs | الإبلاغ عن الأخطاء
- Open an issue on GitHub
- Describe the bug clearly
- Include steps to reproduce
- Provide code examples if possible

### 2. Suggest Features | اقتراح ميزات جديدة
- Open an issue with the "feature request" label
- Explain the feature and its benefits
- Provide use cases

### 3. Improve Documentation | تحسين الوثائق
- Fix typos or unclear explanations
- Add examples
- Translate documentation
- Improve tutorials

### 4. Write Code | كتابة الكود
- Fix bugs
- Implement new features
- Optimize performance
- Add tests

---

## 🚀 Getting Started | البدء

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Bayan-Hybrid-Programming-Language.git
cd Bayan-Hybrid-Programming-Language
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add tests for new features
- Update documentation

### 5. Test Your Changes

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_your_feature.py -v
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add: Brief description of your changes"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues if applicable (#123)

### 7. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request

- Go to the original repository on GitHub
- Click "New Pull Request"
- Select your branch
- Describe your changes clearly
- Link related issues

---

## 📝 Code Style Guidelines | إرشادات أسلوب الكود

### Python Code

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

**Example:**

```python
def parse_expression(tokens: List[Token]) -> ASTNode:
    """
    Parse a list of tokens into an expression AST node.
    
    Args:
        tokens: List of tokens to parse
        
    Returns:
        ASTNode representing the expression
        
    Raises:
        ParseError: If tokens cannot be parsed
    """
    # Implementation here
    pass
```

### Bayan Code Examples

- Use clear, simple examples
- Include comments explaining the code
- Show both Arabic and English keywords when relevant
- Test all examples before submitting

**Example:**

```bayan
hybrid {
    # Example: Simple calculator
    # مثال: آلة حاسبة بسيطة
    
    def add(a, b): {
        return a + b
    }
    
    result = add(5, 3)
    print("Result: " + str(result))
}
```

---

## 🧪 Testing Guidelines | إرشادات الاختبار

### Writing Tests

- Write tests for all new features
- Ensure tests are independent
- Use descriptive test names
- Cover edge cases

**Example:**

```python
def test_addition_with_positive_numbers():
    """Test that addition works correctly with positive numbers."""
    code = """
    hybrid {
        x = 5
        y = 3
        result = x + y
    }
    """
    # Test implementation
    assert result == 8

def test_addition_with_negative_numbers():
    """Test that addition works correctly with negative numbers."""
    # Test implementation
    pass
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=bayan --cov-report=html

# Run specific test
python -m pytest tests/test_lexer.py::test_tokenize_number -v
```

---

## 📚 Documentation Guidelines | إرشادات الوثائق

### Writing Documentation

- Use clear, simple language
- Provide examples for every concept
- Include both Arabic and English when relevant
- Keep documentation up-to-date with code changes

### Documentation Structure

```markdown
# Feature Name

## Overview
Brief description of the feature

## Syntax
Show the syntax with examples

## Examples
Provide multiple examples

## Common Mistakes
Show common errors and how to fix them

## See Also
Link to related documentation
```

---

## 🔍 Pull Request Checklist | قائمة التحقق من Pull Request

Before submitting your pull request, make sure:

- [ ] Code follows the style guidelines
- [ ] All tests pass (`python -m pytest tests/ -v`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files are included
- [ ] Code is well-commented
- [ ] Examples are tested and working

---

## 🐛 Bug Report Template | قالب الإبلاغ عن الأخطاء

When reporting a bug, please include:

```markdown
**Description**
A clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Code Example**
```bayan
# Your code here
```

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- Bayan version: [e.g., commit hash]

**Additional Context**
Any other relevant information
```

---

## 💡 Feature Request Template | قالب طلب الميزات

When requesting a feature, please include:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Syntax**
```bayan
# Example of how the feature would be used
```

**Alternatives Considered**
Other ways to achieve the same goal

**Additional Context**
Any other relevant information
```

---

## 🌍 Translation Guidelines | إرشادات الترجمة

We welcome translations of documentation!

### How to Translate

1. Create a new file with `_LANG` suffix (e.g., `README_FR.md` for French)
2. Translate the content
3. Keep code examples in English (or add both languages)
4. Update the main README to link to your translation

### Translation Checklist

- [ ] All headings translated
- [ ] All paragraphs translated
- [ ] Code examples kept or translated appropriately
- [ ] Links updated to point to translated versions
- [ ] Added to main README's language list

---

## 👨‍💻 Development Setup | إعداد بيئة التطوير

### Recommended Tools

- **IDE**: VSCode, PyCharm, or any Python IDE
- **Python**: 3.8 or higher
- **Git**: Latest version
- **pytest**: For running tests

### VSCode Extensions

- Python
- Pylance
- Python Test Explorer
- GitLens

### Development Workflow

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install pytest pytest-cov
```

3. Run tests frequently:
```bash
python -m pytest tests/ -v
```

---

## 🎯 Priority Areas | المجالات ذات الأولوية

We especially welcome contributions in these areas:

1. **Performance Optimization** - Make Bayan faster
2. **Error Messages** - Improve error reporting
3. **Documentation** - More examples and tutorials
4. **Testing** - Increase test coverage
5. **IDE Support** - Syntax highlighting, autocomplete
6. **Standard Library** - Add useful built-in functions
7. **Tooling** - Debugger, profiler, formatter

---

## 📞 Questions? | أسئلة؟

If you have questions about contributing:

- Open a discussion on GitHub
- Check existing issues and pull requests
- Read the documentation in `docs/`

---

## 🙏 Thank You! | شكراً لك!

Thank you for contributing to Bayan! Every contribution, no matter how small, helps make Bayan better for everyone.

---

**Developed by: Basel Yahya Abdullah (باسل يحيى عبدالله)**  
**With assistance from: AI Language Models**

