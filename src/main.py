"""
This program returns the top x customers with the highest Simple Lifetime Value from data D
"""

from dateutil.parser import parse as date_parser
from dateutil import rrule


date_key = 'event_time'
total_amount_key = 'total_amount'

def total_weeks(start, end):
    weeks = rrule.rrule(rrule.WEEKLY, dtstart=start, until=end)
    return weeks.count()

def load_data(file_path, events):
    first_loop = True
    with open(file_path) as f:
        for line in f.readlines():
            if first_loop:
                first_loop = False
                line_eval = line.strip()[1:-1]
            else:
                line_eval = line.strip()[:-1]
            ingest(line_eval, events)

def write_output(fname, data):
    with open(fname, 'w') as f:
        for x in data:
            f.write(x[0] + ', ' + str(x[1]) + '\n')

def ingest(e, D):
    dic = eval(e)
    if date in dic:
        dic[date] = date_parser(dic[date])

    customer_id = dic['customer_id'] if dic['type'] != 'CUSTOMER' \
                  else dic['key']
        
    if customer_id not in D:
        # Create new customer_id
        D[customer_id] = [dic]
    else:
        # Add customer data
        D[customer_id].append(dic)
        
def topXSimpleLTVCustomers(x, D):

    life_time_value = []
    for customer_id in D:

        # SITE VISITS PER WEEK
        visits_date_list = [r[date_key] for r in D[customer_id] if r['type'] == 'SITE_VISIT']
        if visits_date_list and 'ORDER' in [r['type'] for r in D[customer_id]]:
            active_weeks = total_weeks(min(visits_date_list), max(visits_date_list))
            num_visits = float(len(visits_date_list))
            # Visits per week = Total # of visits / weeks customer activity
            visits_per_week = num_visits / active_weeks

            # CUSTOMER EXPENDITURE PER VISIT
            order_data = [ (r['key'], r['verb'], r['event_time'], float(r[total_amount_key].split()[0]))
                           for r in D[customer_id] if r['type'] == 'ORDER' ]
            order_amounts_by_id = {}
            # Check for order updates
            for key, verb, dt, amount in order_data:
                order_amounts_by_id[key] = (dt, amount)

            total_order_amounts = sum([order_amounts_by_id[key][1] for key in order_amounts_by_id])
            expenditure_per_visit = float(total_order_amounts) / visits_per_week

            # LTV
            avg_cust_val_p_week = expenditure_per_visit * visits_per_week
            cust_lifespan = 10
            life_time_value.append( (customer_id, 52 * avg_cust_val_p_week * cust_lifespan) )
        else:
            # No ORDER events
            life_time_value.append( (customer_id, 0) )

    life_time_value.sort(reverse=True, key=lambda y: y[1])
    print "\nFull LTV list:"
    for ltv in life_time_value:
        print "{}".format(ltv)

    return life_time_value[:x]



if __name__ == '__main__':
    customer_info = {}
    print_info = True
    load_data("input.txt", customer_info)
    top_LTVs = topXSimpleLTVCustomers(10, customer_info)
    output_file = "output.txt"
    write_output(output_file, top_LTVs)
    print "\nData saved in: {}".format(output_file)