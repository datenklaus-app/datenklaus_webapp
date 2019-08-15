import pygal


class DKBarChart(pygal.Bar):
    def __init__(self, dataset, labels):
        style = pygal.style.DefaultStyle()
        style.label_font_size = 16

        super().__init__(show_legend=False, show_y_labels=True,
                         classes=(...,"chart-card-chart", "img-fluid", "rounded"), height=400,
                         style=style)
        self.x_labels = labels
        self.y_labels = range(max(dataset) + 1)

        self.add('', dataset)

    def render(self, disable_xml_declaration=False):
        return super().render(is_unicode=True, disable_xml_declaration=disable_xml_declaration)
