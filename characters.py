#! /usr/bin/python3

from culture import Culture

class Character():
    def __init__(self, models, culture, residence):
        self.firstname = culture.generate_name(models, "german", "m")
        self.leads = residence
        self.fullname = "{} of {}".format(self.firstname, self.leads.name)
