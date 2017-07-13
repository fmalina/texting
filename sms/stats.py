from collections import Counter
from sms.models import Sim, Sms
from datetime import datetime, timedelta


def get_stats(days_back=0):
    all_sims = Sim.objects.all()

    txts = Sms.objects.filter(typ='s')
    if days_back:
        txts = txts.filter(at__gt=datetime.now()-timedelta(days=days_back))
    txts = txts.extra({'date': "date(at)"}).values_list('date','sim')

    sims = {s.pk: s for s in all_sims} # map of SIM pks and their SIM objects
    txts = [(date, sims[sim]) for date, sim in txts] # graft in the SIM objects

    # Group all texts by date, each text represented by its SIM.
    d = {}
    for date, sim in txts:
        try:
            d[date] = d[date] + [sim]
        except KeyError:
            d[date] = []

    # Make a data grid of all SIMs, not just those used on the day.
    # Count how many texts a SIM sent and fill in zero if it wasn't used.
    counts = {}
    for date, sim_counts in d.items():
        used_sims = dict(Counter(sim_counts))
        sim_row = [(sim, used_sims.get(sim, 0)) for sim in all_sims]
        counts[date] = sim_row
    
    # Order by date.
    dates = list(sorted(counts.items(), reverse=1))
    return dates


def least_used(get_list=False):
    dates = get_stats(days_back=12)

    # Order SIMs by usage in the last few days.
    sim_totals = {}
    for day, sim_counts in dates:
        for sim, counts in sim_counts:
            try: sim_totals[sim] = sim_totals[sim] + counts
            except KeyError: sim_totals[sim] = counts
    sort = lambda sims: sorted(sims, key=lambda x: x[1])

    # Choose one least used over the last few days
    weeks_usage = sort(sim_totals.items())
    # today_usage = sort(dates[0][1])
    if get_list:
        return weeks_usage
    return weeks_usage[0][0] if weeks_usage else None
