import os
from flask import Flask
from flaskext.mako import render_template, init_mako
from flask import request

from whoosh import index, qparser, highlight
from whoosh.qparser.dateparse import DateParserPlugin

SOURCEDIR = os.environ.get("DEMOSOURCE", "cpython/Doc")
INDEXDIR = os.environ.get("DEMOINDEX", "index")

app = Flask(__name__)
app.config["MAKO_DIR"] = os.environ.get("DEMOTEMPLATES", "templates")
init_mako(app)


@app.route('/')
def search():
    return render_template("search.html", args=request.args)


@app.route("/results")
def results():
    qs = request.args.get("q", "")
    with get_searcher() as s:
        return render_results(s, qs, "results.html")


@app.route("/analyzer")
def analyzer():
    with get_searcher() as s:
        fieldname = request.args.get("fieldname")
        q = request.args.get("q", "")
        return render_template("analyzer.html", searcher=s, fieldname=fieldname, q=q)


@app.route("/lexicon")
def lexicon():
    with get_searcher() as s:
        fieldname = request.args.get("fieldname")
        return render_template("lexicon.html", reader=s.reader(), fieldname=fieldname)


def get_searcher():
    ix = index.open_dir(INDEXDIR)
    return ix.searcher()


def render_results(s, qs, template):
    qp = qparser.QueryParser("content", s.schema)
    qp = qparser.MultifieldParser(["tgrams", "content"], s.schema)

    # Add the DateParserPlugin to the parser
    qp.add_plugin(DateParserPlugin())

    q = qp.parse(qs)

    results = s.search(q, limit=100)
    results = s.search(q, limit=100, sortedby="title", reverse=True)
    results = s.search(q, limit=100, groupedby="chapter")
    q = results.q

    hf = highlight.HtmlFormatter()
    results.highlighter = highlight.Highlighter(formatter=hf)

    qc = None
    if not results:
        corrected = s.correct_query(q, qs, prefix=1)
        if corrected.query != q:
            qc = corrected.format_string(hf)

    def hilite(hit):
        with open(SOURCEDIR + hit["path"], "rb") as hitfile:
            text = hitfile.read().decode("utf-8")
        return hit.highlights("content", text)

    return render_template(template, qs=qs, q=q,
                           results=results,
                           hilite=hilite,
                           corrected=qc,
                           args=request.args)


if __name__ == '__main__':
    app.run(debug=True)
