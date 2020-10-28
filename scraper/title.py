class Title():
    title_key = None
    from_keys = None
    title = None
    from_comp = None
    claim = None

    @classmethod
    def parse_record(cls, row):
        """Creates a clean Title obj from CSV record(row)"""
        title_key = ''.join(chr.lower()
                            for word in row['TITLE'] if chr.isalnum())
        from_keys = row['FROM/COMPOSER'].lower().split('/')
        title = row['TITLE']
        from_comp = row['FROM/COMPOSER']
        claim = row['CLAIM']

        cls.create(
            title_key=title_key,
            from_keys=from_keys,
            title=title,
            from_comp=from_comp,
            claim=claim
        )
