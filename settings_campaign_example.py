RUN = 1 # Texts are not saved nor sent if RUN is 0. Least_used SIM will not change.
API_KEY = '***'
API_URL = 'https://example.com/api/my_categorised_numbers?key=' + API_KEY
TPL = "Hi, people %s %s using TPL example %s. Hope it helps. Greetings"

TEXTS = {
    'A': TPL % ("want X", "to do V", "and then some"),
    'B': TPL % ("want Y", "to do Z", "and something else")
}
CATEGORIES = {
    'Group A': 'A',
    'Group B': 'B',
}

def custom_replace(txt, cat, greetings):
    txt = txt.replace('Greetings', greetings)
    return txt

BASIC_FOLLOWUP_TXT = "...Hope it works well for you."
WHOLE_FOLLOWUP_TXT = "Hi, you can ...Good luck."

FOLLOWUP_DAYS_BACK = 5 # this can be as low as 2, if followup runs daily without errors

# FINGERPRINT is used to discern 1st text from a followup
FINGERPRINT = "Hi, people"
