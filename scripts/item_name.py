#!/usr/bin/python

def item_name(prefix, pdict, secondary_keys=[], excluded_keys=[]):
    """A function for consistently naming data directories according to parameters."""
    def dict_to_name(d):
        return '_'.join(map(lambda item: "%s%s" % item, sorted(d.items(), key=lambda item: item[0])))
    main_items = pdict.copy()
    secondary_items = dict()
    for key in excluded_keys:
        del main_items[key]
    for key in secondary_keys:
        del main_items[key]
        secondary_items[key] = pdict[key]
    if len(secondary_keys) > 0:
        return prefix + '_' + dict_to_name(main_items) + '/' + dict_to_name(secondary_items)
    else:
        return prefix + '_' + dict_to_name(main_items)
