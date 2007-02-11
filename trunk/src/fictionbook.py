'''
FictionBook2 module
'''

import sys, string, re
import cbparser

class TexFBook(cbparser.XMLCbParser):

    NONE = 0
    SECTION_STARTED = 1

    def __init__(self, outfile):
        cbparser.XMLCbParser.__init__(self)
        self.outfile = outfile
        self.author = None
        self.epigraphs = []
        self.current_epigraph_text = None
        self.current_epigraph_author = None
        self.author_name = None
        self.title = None
        self.mode = self.NONE

    def _uwrite(self, ustr):
        self.f.write(ustr.encode('utf-8')) 

    def _pQuote(self, str):
        ''' Basic paragraph TeX quoting '''
        if len(str)==0:
            return str

        # 'EN DASH' at the beginning of paragrapg - russian direct speach
        if ord(str[0])==8211:
            str="\\cdash--*" + str[1:]

        return str
    
    # --- callbacks ---

    # -- Dealing with book title --

    def start_FictionBook_description_title__info_author(self, attrs):
        self.author={}

    def chars_FictionBook_description_title__info_author_first__name(self, text):
        self.author['first']=text
        
    def chars_FictionBook_description_title__info_author_middle__name(self, text):
        self.author['middle']=text
        
    def chars_FictionBook_description_title__info_author_last__name(self, text):
        self.author['last']=text

    def end_FictionBook_description_title__info_author(self):
        self.author_name = u''
        for k in ['first','middle','last']:
            if self.author.has_key(k):
                v = self.author[k]
            else:
                v = None
            if v:
                if len(self.author_name)==0:
                    self.author_name = v
                else:
                    self.author_name = self.author_name + u' ' + v
        self.author=None

    def chars_FictionBook_description_title__info_book__title(self, text):
        self.title = text

    def end_FictionBook_description_title__info(self):
        if self.author_name:
            self.f.write("\\author{")
            self._uwrite(self.author_name)
            self.f.write("}\n");

        if self.title:
            self.f.write("\\title{")
            self._uwrite(self.title)
            self.f.write("}\n")

        if self.author_name or self.title:
            self.f.write("\\maketitle\n");


        # TODO: PDF info generation temporaty disabled. It seems that
        # non ASCII characters are not allowed there!
        if False and (self.author_name or self.title):
            self.f.write("\n\\pdfinfo {\n")

            if self.author_name:
                self.f.write("\t/Title (")
                self._uwrite(self.author_name) #TODO quoting, at least brackets
                self.f.write(")\n")

            if self.title:
                self.f.write("\t/Author (")
                self._uwrite(self.title) #TODO quoting, at least brackets
                self.f.write(")\n")

            self.f.write("}\n")

    # -- section stuff --        

    def _emit_section_start(self):
        self._emit_section_title()
        self._emit_section_epigraphs()
    
    # -- dealing with epigraphs ---

    def end__section_epigraph(self):
        if self.current_epigraph_text:
            self.epigraphs = self.epigraphs + [(self.current_epigraph_text, self.current_epigraph_author)]
            self.current_epigraph_text = None
            self.current_epigraph_author = None
            
    def chars__section_epigraph_p(self, text):
        if self.current_epigraph_text:
            self.current_epigraph_text = "\\\\" + self.current_epigraph_text+text
        else:
            self.current_epigraph_text = text

    def chars__section_epigraph_text__author(self, text):
        self.current_epigraph_author

    def _emit_section_epigraphs(self):
        if len(self.epigraphs):
             # TODO:emit
             self.epigraphs=[]
        self.current_epigraph_text = None
        self.current_epigraph_author = None
    
    # -- dealing with section titles ---

    def _emit_section_title(self):
        if len(self.section_title):
            self.f.write("\\section{")
            self._uwrite(self.section_title) # TODO quote
            self.f.write("}\n");
            self.section_title=""
    
    def start__section(self, attrs):
        if self.mode == self.SECTION_STARTED:
            self._emit_section_start() # nested section
        else:
            self.mode = self.SECTION_STARTED

    def start__section_p(self, attrs):
        if self.mode == self.SECTION_STARTED:
            # First non-title, non-epigraph element in the sesssion
            self._emit_section_start()
            self.mode == self.NONE
    start__section_annotation = start__section_p

    def start__section_title(self, attrs):
        if self.mode == self.SECTION_STARTED:
            self.section_title=""

    def chars__section_title_p(self, text):
        if len(self.section_title):
            self.section_title = "\\\\" + self.section_title+text
        else:
            self.section_title = text

    def start__section_title_empty__line(self, text):
        self.section_title = self.section_title+text + "\\\\"

    def end_section(self):
        self.mode = self.NONE

    # -- Dealing with section content

    def start__section_empty__line(self, text):
        self.f.write("\n")

    def chars__section_p(self, text):
        self._uwrite(self._pQuote(text))
        self.f.write("\n\n")

    # -- Dealing with book start and end

    def start_FictionBook(self, attrs):
        self.f = open(self.outfile,"w")
        self.f.write("\\documentclass[11pt]{book}\n")
        self.f.write("\\usepackage{graphicx}\n")
        self.f.write("\\usepackage{url}\n")
        self.f.write("\\usepackage{epigraph}\n")
        self.f.write("\\usepackage{verbatim}\n")
        self.f.write("\\usepackage[utf-8]{inputenc}\n")
        self.f.write("\\usepackage[russian]{babel}\n")
        self.f.write("\\usepackage[papersize={9cm,12cm}, margin=4mm, ignoreall, pdftex]{geometry}\n")
        self.f.write("\\setcounter{secnumdepth}{-2}\n"); # supress section numbering
        self.f.write("\n\\begin{document}\n\n")

    def end_FictionBook(self):
        self.f.write("\\tableofcontents\n"); #TODO: move to beginning, make hyperlined index.
        self.f.write("\n\\end{document}\n")
        self.f.close()

