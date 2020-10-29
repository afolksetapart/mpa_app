class Arbiter():
    def __init__(self, title, candidate):
        self.title = title
        self.candidate = candidate
        self.accuracy = 0

    @classmethod
    def compare(cls, title, candidate):
        arbiter = cls(title=title, candidate=candidate)
        title = arbiter.title
        candidate = arbiter.candidate

        if "Sheet music" in candidate.labels:
            if title.title_key in candidate.text:
                arbiter.accuracy += 1

            for key in title.from_keys:
                if key in candidate.text:
                    arbiter.accuracy += .5

            if "disney" in candidate.text:
                arbiter.accuracy += .5

            if "medley" in candidate.text:
                pass

        else:
            pass
        # print "no match"

    def determine(self):
        if self.accuracy >= 1:
            return True
        else:
            return False
