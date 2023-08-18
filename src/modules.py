import operator
import matplotlib.pyplot as plt


def get_distribution_ratio(data, property_name):
    """
  Get the distribution ratio per property named either `ip`, `source` or `serverIp`.

  Args:
    data: A list of dictionaries.
    property_name: A string representing the property name.

  Returns:
    A list of dictionaries, where each dictionary has the property name as the key and the ratio as the value.
  """

    def sort_by_ratio(x):
        return sorted(x, key=operator.itemgetter(1), reverse=True)

    property_to_count = {}
    for item in data:
        if property_name in item:
            property_to_count[item[property_name]] = property_to_count.get(item[property_name], 0) + 1

    property_to_ratio = {}
    for property_name, count in property_to_count.items():
        property_to_ratio[property_name] = round(count / len(data) * 100, 2)

    return sort_by_ratio(list(property_to_ratio.items()))


def transform_data(data_input):
    """ Transform data to be plotted."""
    other_values = [v for v in data_input if float(v[1]) < 5]
    other = sum(float(str(v[1])) for v in other_values)
    data_output = [v for v in data_input if v not in other_values]
    if other:
        data_output.append(("Others", other))

    return data_output


def plot_pie_chart(data, chart_name):
    """ Plot a pie chart."""
    if data:
        labels, values = zip(*transform_data(data))
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.axis("equal")  # Equal aspect ratio ensures a circular pie chart.
        fig.savefig(f"img/{chart_name}.svg")

        with open(f"img/{chart_name}.svg", "rb") as f:
            svg = f.read().decode("utf-8")
        return svg
    else:
        return None
