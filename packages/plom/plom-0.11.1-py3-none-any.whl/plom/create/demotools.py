# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020 Andrew Rechnitzer
# Copyright (C) 2020-2022 Colin B. Macdonald
# Copyright (C) 2020 Dryden Wiebe
# Copyright (C) 2022 Joey Shi

"""Build pdf files for a demo test and provide demo classlists"""

__copyright__ = "Copyright (C) 2020-2022 Andrew Rechnitzer, Colin B. Macdonald, et al"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"

import csv
import importlib.resources as resources
from pathlib import Path
import sys

import plom
from plom.textools import buildLaTeX


def getDemoClassList():
    """A classlist for demos.

    returns:
        list: each entry is dict of one row of the demo classlist.
    """
    d = []
    with resources.open_text(plom, "demoClassList.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            d.append(row)
    return d


def getDemoClassListLength():
    """How long is the built-in demo classlist."""
    return len(getDemoClassList())


def buildDemoSourceFiles(basedir=Path("."), solutions=False):
    """Builds the LaTeX source files for the demo.

    Keyword args:
        basedir (libpath.Path): where to make the files?  We will build
            in a "sourceVersions" under this directory.
        solutions (bool): build solutions as well.  Default: False.

    Returns:
        bool: True if successful, False if it failed.
    """
    src_dir = basedir / "sourceVersions"
    src_dir.mkdir(exist_ok=True)

    print("LaTeXing example exam file: latexTemplate.tex -> version1.pdf")
    content = resources.read_text(plom, "latexTemplate.tex")
    if not buildLaTeXExam2(content, src_dir / "version1.pdf"):
        return False

    print("LaTeXing example exam file: latexTemplatev2.tex -> version2.pdf")
    content = resources.read_text(plom, "latexTemplatev2.tex")
    if not buildLaTeXExam2(content, src_dir / "version2.pdf"):
        return False

    # if requested then also make the pdfs with solutions
    if solutions:
        print("LaTeXing example solution file: latexTemplate.tex -> solution1.pdf")
        content = resources.read_text(plom, "latexTemplate.tex").replace(
            "% \\printanswers", "\\printanswers"
        )
        # uncomment the line "% \printanswers..."
        if not buildLaTeXExam2(content, Path("sourceVersions") / "solutions1.pdf"):
            return False

        print("LaTeXing example solution file: latexTemplatev2.tex -> solutions2.pdf")
        content = resources.read_text(plom, "latexTemplatev2.tex").replace(
            "% \\printanswers", "\\printanswers"
        )
        # uncomment the line "% \printanswers..."
        if not buildLaTeXExam2(content, Path("sourceVersions") / "solutions2.pdf"):
            return False
    # all done
    return True


def buildLaTeXExam2(src, filename):
    """Compile a string of latex to PDF.

    Arguments:
        src (str): LaTeX source to build.
        filename (str/pathlib.Path): The file to create.

    Returns:
        bool: True if everything worked.  Print to stdout and return
            False if latex failed.
    """

    with open(filename, "wb") as f:
        r, out = buildLaTeX(src, f)
    if r:
        print(">>> Latex problems - see below <<<\n")
        print(out)
        print(">>> Latex problems - see above <<<")
        return False
    return True


def main():
    soln_flag = False
    if len(sys.argv) == 2:
        if sys.argv[1] == "solutions":
            soln_flag = True
    if not buildDemoSourceFiles(solutions=soln_flag):
        sys.exit(1)


if __name__ == "__main__":
    main()
