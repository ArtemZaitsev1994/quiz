def set_bold_font(q):
    def bold_gen():
        while True:
            yield '<b>'
            yield '</b>'

    bold_tag = bold_gen()
    return q.replace('*', '{}').format(*[next(bold_tag) for x in range(q.count('*'))])
