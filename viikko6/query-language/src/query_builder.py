from matchers import All, And, HasAtLeast, HasFewerThan, PlaysIn


class QueryBuilder:
    def __init__(self, matcher=All()):
        self.matcher = matcher

    def build(self):
        return self.matcher

    def chain_matcher(self, matcher):
        and_matcher = And(self.matcher, matcher)
        return QueryBuilder(and_matcher)

    def plays_in(self, team):
        matcher = PlaysIn(team)
        return self.chain_matcher(matcher)

    def has_at_least(self, value, attr):
        matcher = HasAtLeast(value, attr)
        return self.chain_matcher(matcher)

    def has_fewer_than(self, value, attr):
        matcher = HasFewerThan(value, attr)
        return self.chain_matcher(matcher)
