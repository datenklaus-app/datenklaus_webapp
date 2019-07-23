import pygal


class DKBarChart(pygal.Bar):
    def __init__(self, dataset, labels):
        style = pygal.style.DefaultStyle()
        style.background = "#FFFFFF"
        super().__init__(show_legend=False, show_y_labels=True,
                         classes=(..., "card-img-bottom", "img-fluid"),
                         style=style, height=450)
        self.x_labels = labels
        self.y_labels = range(max(dataset) + 1)

        self.add('', dataset)

    def render(self):
        return super().render(is_unicode=True)
