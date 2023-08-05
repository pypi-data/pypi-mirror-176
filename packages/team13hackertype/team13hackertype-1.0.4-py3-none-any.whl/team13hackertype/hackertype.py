import keyboard
import os


def looping_string(string: str, chunk_size: int):
    '''
    Creates an iterator that loops over a string forever.
    Each iteration returns the next chunk of the string
    of length 'chunk_size'.

    Parameters
    ----------
    string : str
        The string that is being looped.
    chunk_size : int
        The size of the substring that is returned

    Returns
    -------
    Iterator[str]
        The next substring that is size chunk_size
    '''
    current_index = 0
    string_length = len(string)
    while True:
        chunk = ''
        for i in range(chunk_size):
            chunk += string[(current_index + i) % string_length]
        current_index = (current_index + chunk_size) % string_length
        yield chunk


def get_code_snippet(language: str) -> str:
    '''
    Given a coding language, returns a large code snippet
    written in that language as a raw string.

    Parameters
    ----------
    language : str
        The language of the code snippet.

    Returns
    -------
    str
        The code snippet.

    Raises
    ------
    NotImplementedError
        Raised if we do not have a snippet for the language
        provided. Right now, we support python and java.
    IOError
        Raised if there was another IO problem with opening the file.
    Exception
        Raised for any other miscellaneous exceptions occuring
        when opening the file.
    '''
    language_to_path = {
        'python': './code_snippets/python.txt',
        'java': './code_snippets/java.txt'
    }

    __dirname = os.path.dirname(os.path.abspath(__file__))

    try:
        snippet_filename = os.path.normpath(
            os.path.join(__dirname, language_to_path[language]))
        with open(snippet_filename) as file:
            return file.read()
    except KeyError:
        raise NotImplementedError(
            f"Language {language} is not currently supported"
        )
    except IOError as ioe:
        raise IOError("Unexpected I/O error", ioe)
    except Exception as e:
        raise Exception("Unexpected exception", e)


def hackertype(language: str, speed: int = 20) -> None:
    '''
    Starts listening for keyboard presses. On key press,
    print out 'speed' amount of characters from a sample document
    written in the 'language' coding language.

    Parameters
    ----------
    language : str
        The coding language of the hacker type to be printed.
        Supported values include python and java
    speed : int, optional
        The number of characters to print out on a single key
        press. (Default is 20.)

    Returns
    -------
    None
    '''
    code_snippet = get_code_snippet(language)
    code_snippet_iter = looping_string(code_snippet, speed)
    keyboard.on_press(lambda e:
                      print(next(code_snippet_iter), end='', flush=True))

    keyboard.wait('esc')


if __name__ == '__main__':
    hackertype('python')
