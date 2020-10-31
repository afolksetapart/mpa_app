class Arbiter():
    def __init__(self, title, candidate):
        self.title = title
        self.candidate = candidate
        self.accuracy = 0

    @classmethod
    def compare(cls, title, candidate):
        """Compares a Title/Candidate object and scores the result"""
        arbiter = cls(title=title, candidate=candidate)
        t = arbiter.title
        c = arbiter.candidate

        if "Sheet music" in c.labels or "Music" in c.labels:
            if t.title_key in c.text:
                arbiter.accuracy += 1

            for key in t.from_keys:
                if key in c.text:
                    arbiter.accuracy += .5

            if "alfred" in c.text:
                arbiter.accuracy += .5

            if "disney" in c.text:
                arbiter.accuracy += .5

            if "medley" in c.text:
                arbiter.accuracy = 0

        return arbiter

    def determine(self):
        """Determines if score is high enough to return a True value (match found)"""
        if self.accuracy >= 1.5:
            return True
        else:
            return False
