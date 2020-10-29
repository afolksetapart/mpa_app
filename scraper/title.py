class Title():
    def __init__(self):
        self.title_key = None
        self.from_keys = None
        self.title = None
        self.from_comp = None
        self.claim = None

    @classmethod
    def parse_record(cls, row):
        """Creates a clean Title obj from CSV record(row)"""
        title_key = ''.join(chr.lower()
                            for chr in row['TITLE'] if chr.isalnum())
        from_key_list = row['FROM/COMPOSER'].lower().split('/')
        from_keys = [item.replace(" ", "") for item in from_key_list]
        title = row['TITLE']
        from_comp = row['FROM/COMPOSER']
        claim = row['CLAIM']

        title = cls(
            title_key=title_key,
            from_keys=from_keys,
            title=title,
            from_comp=from_comp,
            claim=claim
        )

        return title
