import os.path
import mailbox
import email.parser
import email.utils
import datetime
from hashlib import md5

from whoosh import analysis, fields, index
from whoosh.lang.stopwords import stoplists
from whoosh.util import now


sourcedir = "/Users/matt/Presentation/archives"
indexdir = "/Users/matt/Presentation/index"

ana = analysis.StemmingAnalyzer(stoplist=stoplists["en"], maxsize=40)


class EmailSchema(fields.SchemaClass):
    subject = fields.TEXT(stored=True, sortable=True, analyzer=ana)
    sgrams = fields.NGRAMWORDS
    body = fields.TEXT(stored=True, spelling=True, analyzer=ana)
    sender = fields.TEXT(phrase=False, stored=True)
    sent = fields.DATETIME(sortable=True)
    filename = fields.STORED
    key = fields.STORED

ix = index.create_in(indexdir, EmailSchema)
with ix.writer(limitmb=1024) as w:
    t = now()
    parser = email.parser.Parser()
    for filename in os.listdir(sourcedir):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(sourcedir, filename)
        print filepath
        mbox = mailbox.mbox(filepath)
        for key, msg in mbox.iteritems():
            sent = None
            if msg["date"]:
                sent_tuple = email.utils.parsedate_tz(msg["date"])
                if sent_tuple and sent_tuple[0] >= 2000:
                    tm = email.utils.mktime_tz(sent_tuple)
                    sent = datetime.datetime.fromtimestamp(tm)

            if not msg["subject"]:
                continue
            if not msg["from"]:
                continue

            if msg.get_charset():
                print msg.get_charset()

            subject = msg["subject"].decode("latin1")

            w.add_document(subject=subject, sgrams=subject,
                           body=msg.get_payload().decode("latin1"),
                           sender=msg["from"].decode("latin1"),
                           sent=sent,
                           filename=filename, key=key)

    print "-", now() - t

print now() - t

