import re
from bs4 import BeautifulSoup, Tag, NavigableString


class TextRe:
    @classmethod
    def textcom(cls, fieldtext, comtext, retext):
        try:
            th = fieldtext.find(lambda x: re.compile(comtext).match(x.text) is not None)
            result = ''
            for td in th.next_siblings:
                if isinstance(td, Tag) and td.name == retext:
                    result = td.text
                    break
        except:
            result = ''

        finally:
            return result.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')

    @classmethod
    def replace(cls,str):
        return str.replace('\r','').replace('\n','').replace('\t','').replace('\xa0','')