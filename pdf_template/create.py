from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

def generate_rendered_html(template_path, data_dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    rendered_html = template.render(data_dict)
    return rendered_html


def save_rendered_html(rendered_html, output_file):
    with open(output_file, 'w') as file:
        file.write(rendered_html)


def render_template(template_path, data_dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)

    # Create a dictionary to store the consolidated items and their quantities
    consolidated_items = {}

    # Calculate the quantities and prices for the consolidated items
    for item in data_dict['receiptItems']:
        item_name = item['name']
        item_price = item['price']
        item_count = item['count']
        item_total_price = item_price * item_count

        if item_name in consolidated_items:
            consolidated_items[item_name]['count'] += item_count
            consolidated_items[item_name]['price'] += item_total_price
        else:
            consolidated_items[item_name] = {'count': item_count, 'price': item_total_price}

    # Update the data_dict with consolidated items
    data_dict['consolidatedItems'] = consolidated_items

    # Format the prices with commas and two decimal places for each item
    for item_data in consolidated_items.values():
        item_data['formatted_price'] = '{:,.2f}'.format(item_data['price'] / item_data['count'])
        item_data['formatted_last_price'] = '{:,.2f}'.format(item_data['price'])

    # Calculate the sum of prices for all items
    total_price = sum(item_data['price'] for item_data in consolidated_items.values())

    # Format the total price with commas and two decimal places
    formatted_total_price = '{:,.2f}'.format(total_price)

    # Add the total price to the data_dict
    data_dict['formattedTotalPrice'] = formatted_total_price

    rendered_html = template.render(data_dict)
    return rendered_html

