import re


class easyMail:
    def __init__(self, text, hero_image, preview_text, url, donate_footer_url, credit, button, action, signature,
                 template='templates/hero/hero_template.txt'):
        self.template = template
        self.text = text
        self.hero_image = hero_image
        self.preview_text = preview_text
        self.url = url
        self.donate_footer_url = donate_footer_url
        self.button = button
        self.signature = signature
        self.f_copy = ''
        self.f_hero = ''
        self.f_body = ''
        self.f_email = ''
        self.body_link_number = 1
        self.hero_link_number = 1
        self.template_links = []
        self.action = action
        self.credit = credit

    @staticmethod
    def load_template(template):
        template = open(template, mode='r')
        template = template.read()
        return template

    @staticmethod
    def format_block(uf_block):
        uf_block = open(uf_block, mode='r')
        f_block = uf_block.read()
        return f_block

    def format_copy(self):
        uf_copy = re.findall(r"^(.+)\n+", self.text, re.MULTILINE)
        f_copy = ''

        for text in uf_copy:
            if len(text) > 1 and re.search("(%%HERO%%)(.*?)(%%HERO%%)", text, re.S):
                self.f_hero = re.search("(%%HERO%%)(.*?)(%%HERO%%)", text, re.S).group(2)
                self.f_hero = (self.format_block('templates/hero/header_p.txt')
                               + self.f_hero + '</strong></p>')

            elif len(text) > 1:
                f_copy = f_copy + (self.format_block('templates/hero/body_p.txt')
                                   + text + '</span></p>')
            self.f_copy = f_copy

    def format_hero_a_tag_url(self):
        a = self.format_block('templates/hero/a.txt')
        f_a = re.sub('%%URL%%', '{' + self.url + '~headertext' + str(self.hero_link_number) + '}', a, re.S)
        return f_a

    def format_hero(self):
        hero_uf = re.findall(str(self.format_block('templates/hero/header_p.txt') + '.*?</p>'),
                             self.f_hero, re.S)
        try:
            hero_uf = hero_uf[-1]
            hero_f = re.sub('margin-bottom:1rem', 'margin-bottom:0', hero_uf, re.S)
            self.f_hero = re.sub(hero_uf, hero_f, self.f_hero, re.S)
            for link in range(len(re.findall("%%LINK%%(.*?)%%LINK%%", self.f_hero, re.S))):
                self.f_hero = re.sub(r"(%%LINK%%)(.*?)(%%LINK%%)", (r"%s\2</a>" % self.format_hero_a_tag_url()),
                                     self.f_hero, 1, re.S)
                self.hero_link_number += 1

        except IndexError:
            self.f_hero = ''

    def format_credit(self):
        credit_uf = self.format_block('templates/hero/credit.txt')
        credit_f = re.sub('%%CREDIT%%', self.credit, credit_uf, re.S)
        return credit_f

    def format_body(self):
        self.f_body = re.sub("(%%HERO%%)(.*?)(%%HERO%%)", '', self.f_copy, re.S)
        graphs_uf = re.findall(
            str(self.format_block('templates/hero/body_p.txt') + '.*?</p>'),
            self.f_body, re.S)
        graphs_uf = graphs_uf[:-1] + [re.sub('margin-bottom:1rem', 'margin-bottom:0', graphs_uf[-1], re.S)]
        self.f_body = ''.join(graphs_uf)
        print(self.f_body)

    def format_button(self, button):
        if self.action == 1:
            return re.sub(">DONATE NOW<", ">TAKE ACTION<", button, re.S)
        else:
            return button

    def format_signature(self, signature):
        return self.format_block(signature)

    def insert_into_template(self):
        template = self.load_template(self.template)
        self.f_email = template
        self.f_email = re.sub("%%HERO_TEXT%%", self.f_hero, self.f_email)
        self.f_email = re.sub("%%BODY_TEXT%%", self.f_body, self.f_email)
        self.f_email = re.sub("%%HERO_BANNER_SOURCE%%", self.hero_image, self.f_email)
        self.f_email = re.sub("%%PREVIEW_TEXT%%", self.preview_text, self.f_email)
        self.f_email = re.sub("%%SIGNATURE%%", self.format_signature(self.signature), self.f_email)
        if self.action == 0 and self.button == 1:
            bh = self.format_block('templates/hero/button_header.txt')
            bh = self.format_button(bh)
            self.f_email = re.sub("%%BUTTON_HEADER%%", bh, self.f_email, re.S)
            self.f_email = re.sub("%%BUTTON_FOOTER%%", '', self.f_email, re.S)
        elif self.button == 1:
            bh = self.format_block('templates/hero/button_header.txt')
            bf = self.format_block('templates/hero/button_footer.txt')
            bh = self.format_button(bh)
            bf = self.format_button(bf)
            self.f_email = re.sub("%%BUTTON_HEADER%%", bh, self.f_email, re.S)
            self.f_email = re.sub("%%BUTTON_FOOTER%%", bf, self.f_email, re.S)
        elif self.button == 0:
            self.f_email = re.sub("%%BUTTON_HEADER%%", '', self.f_email, re.S)
            self.f_email = re.sub("%%BUTTON_FOOTER%%", '', self.f_email, re.S)
        if self.credit != '':
            credit = self.format_credit()
            self.f_email = re.sub("%%CREDIT%%", credit, self.f_email, re.S)
        elif self.credit == '':
            self.f_email = re.sub("%%CREDIT%%", '', self.f_email, re.S)
        if re.search("%%DONATE_URL%%", self.f_email):
            self.f_email = re.sub("%%DONATE_URL%%",
                                  self.donate_footer_url + '&ea.tracking.id=footer-button~footer-button', self.f_email,
                                  re.S)

    def format_body_a_tag_url(self):
        a = self.format_block('templates/hero/a.txt')
        f_a = re.sub('%%URL%%', '{' + self.url + '~body' + str(self.body_link_number) + '}', a, re.S)
        return f_a

    def insert_body_links(self):

        if len(re.findall('%%LINK%%', self.f_email)) % 2 != 0:
            print(len(re.findall('%%LINK%%', self.f_email)))
            print('Oops! Looks like you need to close a link somewhere in the text file.',
                  'Make sure every link starts and ends with %%LINK%%!')
            exit()

        for link in range(len(re.findall("%%LINK%%(.*?)%%LINK%%", self.f_email, re.S))):
            self.f_email = re.sub(r"(%%LINK%%)(.*?)(%%LINK%%)", (r"%s\2</a>" % self.format_body_a_tag_url()),
                                  self.f_email, 1, re.S)
            self.body_link_number += 1

    def find_fname(self):
        self.f_email = re.sub(r"%%FNAME%%", '{salutation~First Name or Friend}', self.f_email, re.S)

    def find_bold(self):
        self.f_email = re.sub(r"(%%BOLD%%)(.*?)(%%BOLD%%)", r"<strong>\2</strong>", self.f_email, re.S)

    def find_italic(self):
        self.f_email = re.sub(r"(%%ITALIC%%)(.*?)(%%ITALIC%%)", r"<em>\2</em>", self.f_email, re.S)

    def find_underline(self):
        self.f_email = re.sub(r"(%%UNDERLINE%%)(.*?)(%%UNDERLINE%%)",
                              r"<span style='text-decoration:underline'>\2</span>", self.f_email, re.S)

    def find_red(self):
        self.f_email = re.sub(r"(%%RED%%)(.*?)(%%RED%%)", r"<span style='color:red'>\2</span>", self.f_email, re.S)

    def find_special_characters(self):
        self.f_email = re.sub(r" -- ", " &mdash; ", self.f_email, re.S)
        self.f_email = re.sub(r">>", "&raquo;", self.f_email, re.S)

    def insert_template_urls(self):
        self.f_email = re.sub(r"%%URL%%", self.url, self.f_email, re.S)

    def create_email(self):
        self.format_copy()
        self.format_hero()
        self.format_body()
        self.insert_into_template()
        self.insert_body_links()
        self.find_fname()
        self.find_bold()
        self.find_italic()
        self.find_underline()
        self.find_red()
        self.find_special_characters()
        self.insert_template_urls()
        return self.f_email
