# Python Coding Style Specification

## Core Principles

### 1. Favor Simplicity Over Complexity
- **Always choose the simple, straightforward solution** over complex or "sophisticated" alternatives
- **Avoid over-engineering** - resist the urge to build elaborate abstractions unless clearly needed
- **No premature optimization** - especially avoid blind optimization without measurement
- **Use simple building blocks** that can be composed elegantly rather than complex features
- **Principle**: If there are two ways to solve a problem, choose the one that is easier to understand

### 2. Clarity is Key
- **Readable code beats clever code** - optimize for the reader, not the writer
- **Use clear, descriptive names** for variables, functions, and classes
- **Format code for maximal scanning ease** - use whitespace and structure intentionally
- **Document intent and organization** with comments and docstrings where helpful
- **Reduce cognitive load** - code should express intent clearly at a glance
- **Principle**: The easier your code is to understand immediately, the better it is

### 3. Write Pythonic Code
- **Follow Python community standards and idioms** for naming, formatting, and programming paradigms
- **Cooperate with the language** rather than fighting it
- **Leverage Python features** like generators, itertools, collections, and functional programming
- **Write code that looks like Python wrote it** - use established patterns and conventions
- **Examples of Pythonic patterns**:
  - List comprehensions over explicit loops when appropriate
  - Context managers (`with` statements) for resource management
  - Generator expressions for memory efficiency
  - `enumerate()` instead of manual indexing
  - `zip()` for parallel iteration

### 4. Don't Repeat Yourself (DRY)
- **Avoid code duplication** to make code more maintainable and extendable
- **Use functions and modules** to encapsulate common logic in single authoritative locations
- **Consider inheritance** to avoid duplicate code between related classes
- **Leverage language features** like default arguments, variable argument lists (`*args`, `**kwargs`), and parameter unpacking
- **Eliminate duplication through abstraction** - but don't abstract too early

### 5. Focus on Readability First
- **PEP8 is a guide, not a law** - readability trumps mechanical adherence to style rules
- **Make code as easy to understand as possible** - this is the ultimate goal
- **Deliberately violate guidelines** if it makes specific code more readable
- **Consider the human reader** first when making formatting and style decisions
- **Principle**: Rules serve readability, not the other way around

### 6. Embrace Conventions
- **Follow established conventions** to eliminate trivial decision-making
- **Use PEP8 as a baseline** but prioritize readability when there's conflict
- **Establish consistent patterns** in your codebase for common tasks:
  - Variable naming patterns
  - Exception handling approaches
  - Logging configuration
  - Import organization
- **Consistency enables focus** - familiar patterns let readers focus on logic rather than parsing

## Specific Implementation Guidelines

### Naming Conventions
- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private attributes**: `_single_leading_underscore`
- **Choose descriptive names** that clearly indicate purpose and content

### Code Structure
- **Organize imports** in this order: standard library, third-party, local imports
- **Use blank lines** to separate logical sections
- **Keep functions focused** on a single responsibility
- **Prefer composition over inheritance** when appropriate
- **Write functions that do one thing well**

### Documentation
- **Write docstrings** for modules, classes, and functions that aren't immediately obvious
- **Use comments** to explain why, not what
- **Keep comments up to date** with code changes
- **Focus on intent** rather than implementation details

### Error Handling
- **Use specific exception types** rather than generic `Exception`
- **Follow the "easier to ask for forgiveness than permission" (EAFP) principle**
- **Handle errors at the appropriate level** - don't catch exceptions you can't handle meaningfully

### Performance and Optimization
- **Write clear code first** - optimize only when necessary and after measurement
- **Use appropriate data structures** for the task
- **Leverage built-in functions** and library functions when they're clearer
- **Profile before optimizing** - don't guess where bottlenecks are

## Code Review Checklist

When generating or reviewing Python code, ensure:
- [ ] The simplest solution that works is chosen
- [ ] Names clearly communicate purpose
- [ ] Code is easily scannable and readable
- [ ] Pythonic patterns are used appropriately
- [ ] No unnecessary duplication exists
- [ ] Conventions are followed consistently
- [ ] Comments explain intent where needed
- [ ] Error handling is appropriate
- [ ] The code would be easy for another developer to understand and maintain

## Decision Framework

When faced with coding choices, ask:
1. **Is this the simplest solution that works?**
2. **Will this be clear to someone reading it in 6 months?**
3. **Am I using Python idioms appropriately?**
4. **Am I duplicating logic that could be abstracted?**
5. **Does this follow our established conventions?**
6. **Is this optimized for readability?**

The answer to all these questions should be "yes" for beautiful Python code.