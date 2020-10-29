class Arbiter():
    def __init__(self, title, candidate):
        self.title = title
        self.candidate = candidate

    @classmethod
    def determine(cls, title, candidate):
        arbiter = cls(title=title, candidate=candidate)
        title = arbiter.title
        candidate = arbiter.candidate
        accuracy = 0

        if title.title_key in candidate.text:
            accuracy += 1

        for key in title.from_keys:
            if key in candidate.text:
                accuracy += 1
