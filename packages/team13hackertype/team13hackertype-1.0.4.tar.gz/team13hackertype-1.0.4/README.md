# Team 13 - Hackertype

![Buildtest](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-13/actions/workflows/build.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9088681&assignment_repo_type=AssignmentRepo)

A little exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

## Team Members

Kedan Zha

Bruce Wu

Evan Huang

Amaan Khwaja

## Project Description

Hackertype lets you pretend you are the elite hacker you always you knew you were in your heart of hearts, right from the CLI.

## CLI Tools

### Hackertype

```sh
python -m team13hackertype hackertype <language:[python|java]>
```

Run the classic hackertype app from the old internet days. Press keys to generate programming snippets from the given language and press `esc` to finish. Currently supported languages are `python` and `java`.

### Penetrate

```sh
python -m team13hackertype penetrate <language> <text:optional>
```

Simulate a penetration hack. The program will display your text in a scary looking font before launching into hackertype of your given language. The supported language and usage is the same as hackertype. When done, the program will tell you that you are logging out.

### Help

```sh
python -m team13hackertype -h
```

View a description of the functions and the parameters provided by the package.

Happy hacking!

## Usage in a Python project

While hackertype is meant to be, for the most part, a fun, whimsical command line app, there are a few functionalities that may be imported into your project.

### `hackertype.looping_string`

```python
looping_string(string: str, chunk_size: int) -> Iterator[str]
```

Creates an iterator that loops over a string forever. Each iteration returns the next chunk of the string of length 'chunk_size'.

- Parameters
  - `string: str`
    - The string that is being looped.
  - `chunk_size: int`
    - The size of the substring that is returned.
- Returns
  - `Iterator[str]`
    - An iterator of substrings of `string` where each substring has size `chunk_size`. This iterator has no stop.

### `hackertype.get_code_snippet`

```python
get_code_snippet(language: str) -> str
```

Given a coding language, returns a large code snippet written in that language as a string. Currently, supported values for lanuage are `'python'` and `'java'`. The code snippet for Python was borrowed from [TensorFlow](https://github.com/tensorflow/tensorflow/blob/bf75d55d5a902a01585dd2948ea7f443511fc923/tensorflow/python/kernel_tests/math_ops/cwise_ops_binary_test.py) and the snippet for Java was borrowed from [Spring](https://github.com/spring-projects/spring-boot/blob/67af4c0a653d7db77cc3093809c1b7ccdcb99f2a/spring-boot-project/spring-boot-tools/spring-boot-gradle-plugin/src/test/java/org/springframework/boot/gradle/docs/PackagingDocumentationTests.java).

- Parameters
  - `language: 'python' | 'java'`
    - The language of the code snippet.
- Returns
  - `str`
    - The code snippet written in the `language` programming language.
- Raises
  - `NotImplementedError`
    - Raised if we do not have a snippet for the language provided. Right now, we support python and java.
  - `IOError`
    - Raised if there was another IO problem with opening the file.
  - `Exception`
    - Raised for any other miscellaneous exceptions occuring when opening the file.

### `hackertype.hackertype`

```python
hackertype(language: str, speed: int = 20) -> None
```

Starts listening for keyboard presses. On key press, prints out `speed` amount of characters from a code snippet written in the `language` coding language, until the `Esc` key is pressed. Note that this function is **not** asynchronous. This means that after running, it will wait for the `Esc` key before continuing program execution.

- Parameters
  - `language: 'python' | 'java'`
    - The coding language of the hacker snippet to be printed.Supported values include `'python'` and `'java'`.
  - `speed: int, optional, default: 20`
    - The number of characters to print out on a single key press.
- Returns
  - `None`
- Raises
  - Same as `hackertype.get_code_snippet`.

### `penetrate.penetrate`

```python
penetrate(language: str, text: str = "DARKWEB", loading_bar_speed: float = 1.0, emphasis_style: str = "bold red", notification_style: str = "bold green") -> None
```

Simulates a penetration hacking attempt in the standard output. Logs out `text` in ASCII text before launching into hackertype. Upon escaping, displays a logging out message. Note that this function utilizes `hackertype.hackertype` and is also **not** asynchronous.

- Parameters
  - `language: str`
    - The coding language of the hacker type to be printed.Supported values include `'python'` and `'java'`. See `hackertype.hackertype`.
  - `text: str, optional, default: "DARKWEB"`
    - The text shown in the banner. Length of string must be less than 8.
  - `loading_bar_speed: float, optional`
    - The speed of loading bar progress.
  - `emphasis_style: str, optional, default: "bold red"`
    - The style for Console print of emphasized text. For options, see [Rich docs](https://rich.readthedocs.io/en/stable/style.html).
  - `notification_style: str, optional, default: "bold green"`
    - The style for Console print of emphasized text, used in `show_header`. For options, see [Rich docs](https://rich.readthedocs.io/en/stable/style.html).
- Returns
  - `None`
- Raises
  - `NotImplementedError`
    - Raised if we do not have a snippet for the language provided. Right now, we support python and java. See `hackertype.hackertype`.
  - `ValueError`
    - Raised if the given style is not provided.
  - `Exception`
    - Unexpected exception that may arise from IO or console issues.

## Example Usage

View an example usage of the functions [here](./example.py).

## Contributing Runbook

1. Clone the project. (`git clone https://github.com/software-students-fall2022/python-package-exercise-project-3-team-13.git`)
2. Change directories into the project. (`cd python-package-exercise-project-3-team-13`)
3. Set up and activate your virtual environment. (`python -m venv venv && source venv/bin/activate`)
4. Install the requirements. (`python -m pip install -r requirements.txt`)
5. The package is now available to you in `src/team13hackertype`.
6. Run the tests. (`python -m pytest ./tests`)
7. To build, run `python -m build`.
