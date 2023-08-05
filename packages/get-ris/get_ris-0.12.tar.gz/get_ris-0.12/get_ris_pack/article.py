class Article():
    def __init__(self,title,authors,year,_type,publisher,abstract) -> None:
        self.title = title
        self.year = year
        if(_type =='Journals'):
            self.type = 'Journal Article'
        elif(_type =='Conferences'):
            self.type = 'Conference Proceedings'
        else:
            self.type = _type
        self.authors = authors
        self.publisher = publisher
        self.abstract = abstract

    def convert_to_Endnote(self):
        """Convert to Endnote Format

        Returns:
            [type]: [description]
        """
        content = ''
        content+=f'%0 {self.type}\n'
        for author in self.authors:
            content+=f'%A {author}\n'
        content+=f'%T {self.title}\n'
        if(self.type == 'Journal Article'):
            content+=f'%J {self.publisher}\n'
        elif(self.type == 'Conference Proceedings'):
            content+=f'%B {self.publisher}\n'
        else:
            content+=f'%J {self.publisher}\n'
        content+=f'%D {self.year}\n'
        content+=f'%X {self.abstract}\n'
        return content

    def __repr__(self) -> str:
        return self.convert_to_Endnote()