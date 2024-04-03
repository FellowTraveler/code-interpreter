import copy
from typing import List, Optional, Iterable, Dict
from pydantic import BaseModel


class Error(BaseModel):
    """
    Represents an error that occurred during the execution of a cell.
    The error contains the name of the error, the value of the error, and the traceback.
    """

    name: str
    "Name of the exception."
    value: str
    "Value of the exception."
    traceback_raw: List[str]
    "List of strings representing the traceback."

    @property
    def traceback(self) -> str:
        """
        Returns the traceback as a single string.

        :return: The traceback as a single string.
        """
        return "\n".join(self.traceback_raw)


class MIMEType(str):
    """
    Represents a MIME type.
    """


class Result:
    """
    Represents the data to be displayed as a result of executing a cell in a Jupyter notebook.
    This is result returned by ipython kernel: https://ipython.readthedocs.io/en/stable/development/execution.html#execution-semantics

    The result can contain multiple types of data, such as text, images, plots, etc. Each type of data is represented
    as a string, and the result can contain multiple types of data. The text representation is always present, and
    the other representations are optional.

    The class also provides methods to display the data in a Jupyter notebook.
    """

    text: str
    "Text representation of the result. Always present."
    html: Optional[str] = None
    markdown: Optional[str] = None
    svg: Optional[str] = None
    png: Optional[str] = None
    jpeg: Optional[str] = None
    pdf: Optional[str] = None
    latex: Optional[str] = None
    json: Optional[dict] = None
    javascript: Optional[str] = None
    extra: Optional[dict] = None
    "Extra data that can be included. Not part of the standard types."

    is_main_result: bool
    "Whether this data is the result of the cell. Data can be produced by display calls of which can be multiple in a cell."

    raw: Dict[MIMEType, str]
    "Dictionary that maps MIME types to their corresponding string representations of the data."

    def __init__(self, is_main_result: bool, data: [MIMEType, str]):
        self.is_main_result = is_main_result
        self.raw = copy.deepcopy(data)

        self.text = data.pop("text/plain")
        self.html = data.pop("text/html", None)
        self.markdown = data.pop("text/markdown", None)
        self.svg = data.pop("image/svg+xml", None)
        self.png = data.pop("image/png", None)
        self.jpeg = data.pop("image/jpeg", None)
        self.pdf = data.pop("application/pdf", None)
        self.latex = data.pop("text/latex", None)
        self.json = data.pop("application/json", None)
        self.javascript = data.pop("application/javascript", None)
        self.extra = data

    def keys(self) -> Iterable[str]:
        """
        Returns the MIME types of the data.

        :return: The MIME types of the data.
        """
        return self.raw.keys()

    def __str__(self) -> str:
        """
        Returns the text representation of the data.

        :return: The text representation of the data.
        """
        return self.text

    def _repr_html_(self) -> str:
        """
        Returns the HTML representation of the data.

        :return: The HTML representation of the data.
        """
        return self.html

    def _repr_markdown_(self) -> str:
        """
        Returns the Markdown representation of the data.

        :return: The Markdown representation of the data.
        """
        return self.markdown

    def _repr_svg_(self) -> str:
        """
        Returns the SVG representation of the data.

        :return: The SVG representation of the data.
        """
        return self.svg

    def _repr_png_(self) -> str:
        """
        Returns the base64 representation of the PNG data.

        :return: The base64 representation of the PNG data.
        """
        return self.png

    def _repr_jpeg_(self) -> str:
        """
        Returns the base64 representation of the JPEG data.

        :return: The base64 representation of the JPEG data.
        """
        return self.jpeg

    def _repr_pdf_(self) -> str:
        """
        Returns the PDF representation of the data.

        :return: The PDF representation of the data.
        """
        return self.pdf

    def _repr_latex_(self) -> str:
        """
        Returns the LaTeX representation of the data.

        :return: The LaTeX representation of the data.
        """
        return self.latex

    def _repr_json_(self) -> dict:
        """
        Returns the JSON representation of the data.

        :return: The JSON representation of the data.
        """
        return self.json

    def _repr_javascript_(self) -> str:
        """
        Returns the JavaScript representation of the data.

        :return: The JavaScript representation of the data.
        """
        return self.javascript


class Logs(BaseModel):
    """
    Data printed to stdout and stderr during execution, usually by print statements, logs, warnings, subprocesses, etc.
    """

    stdout: List[str] = []
    "List of strings printed to stdout by prints, subprocesses, etc."
    stderr: List[str] = []
    "List of strings printed to stderr by prints, subprocesses, etc."


class Execution(BaseModel):
    """
    Represents the result of a cell execution.
    """

    class Config:
        arbitrary_types_allowed = True

    results: List[Result] = []
    "List of the result of the cell (interactively interpreted last line), display calls (e.g. matplotlib plots)."
    logs: Logs = Logs()
    "Logs printed to stdout and stderr during execution."
    error: Optional[Error] = None
    "Error object if an error occurred, None otherwise."

    @property
    def text(self) -> Optional[str]:
        """
        Returns the text representation of the result.

        :return: The text representation of the result.
        """
        for d in self.results:
            if d.is_main_result:
                return d.text


class KernelException(Exception):
    """
    Exception raised when a kernel operation fails.
    """

    pass
