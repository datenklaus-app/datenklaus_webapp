import pygal


class DKBarChart(pygal.Pie):
    """
    Pygal Bar chart with global styling for internal use
    """

    def __init__(self, dataset, labels, title=None):
        style = pygal.style.DefaultStyle()
        style.label_font_size = 16
        
        super().__init__(show_legend=True, show_y_labels=False,
                         classes=(..., "chart-card-chart", "img-fluid", "w-100", "rounded"), height=400,
                         style=style, half_pie=True, legend_at_bottom=True)

        self.title=title

        for i in range(len(labels)):
            self.add(labels[i], dataset[i])

    def render(self, is_unicode=True, disable_xml_declaration=False):
        return super().render(is_unicode=is_unicode, disable_xml_declaration=disable_xml_declaration)
