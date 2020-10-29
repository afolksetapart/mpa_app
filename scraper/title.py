class Title():
    def __init__(self, title_key, from_keys, title, from_comp, claim):
        self.title_key = title_key
        self.from_keys = from_keys
        self.title = title
        self.from_comp = from_comp
        self.claim = claim

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
