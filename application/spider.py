from lxml import html
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#seed_url = u"http://www.kekenet.com/read/essay/ats/"
seed_url = u"http://www.cnn.com/"
x = html.parse(seed_url)
spans = x.xpath("*//ul[@id='menu-list']//li/h2/a")
for span in spans[:10]:
    details_url = span.xpath("attribute::href")[0]
    xx = html.parse(details_url)
    name = 'documents_cn//'+span.text.replace(u' ', u'_')
    f = open(name, 'a')
    try:
        contents = xx.xpath("//div[@id='article']//p/text()")
        for content in contents:
            if len(str(content)) > 1:
                f.write(content.encode('raw_unicode_escape')+'\n')
    except Exception, e:
        print "wrong!!!!", e
        f.close()
        os.remove(name)
    else:
        f.close()