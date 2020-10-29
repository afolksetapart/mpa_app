class Arbiter():
    def __init__(self, title, candidate):
        self.title = title
        self.candidate = candidate
        self.accuracy = 0

    @classmethod
    def compare(cls, title, candidate):
        arbiter = cls(title=title, candidate=candidate)
        t = arbiter.title
        c = arbiter.candidate

        # print(f"Image being evaluated: {c.preview_url}")
        # print(f"Labels being evaluated: {c.labels}")
        # print(f"Title key: {t.title_key}")
        # print(f"From Keys: {t.from_keys}")

        if "Sheet music" in c.labels or "Music" in c.labels:
            if t.title_key in c.text:
                arbiter.accuracy += 1

            for key in t.from_keys:
                if key in c.text:
                    arbiter.accuracy += .5

            if "disney" in c.text:
                arbiter.accuracy += .5

            if "medley" in c.text:
                arbiter.accuracy = 0
            # print(f"Score: {arbiter.accuracy}\n\n")
        return arbiter

        # print "no match"

    def determine(self):
        if self.accuracy >= 1.0:
            return True
        else:
            return False
