from django.shortcuts import render

from models import Flow


def top_prefixes(request):
    return top_prefixes_hours(request, 0)

def top_prefixes_hours(request, hours):
    hours = int(hours)
    flows = Flow.objects.aggregate_bytes_per_prefix(hours)

    dates = [d for d in Flow.objects.get_dates()[-hours:]]

    top_flows = list()

    for f in flows[:10]:
        flow_data = Flow.objects.get_latest_flows_per_prefix(f['ip_dst'], f['mask_dst'], hours)
        flow = {
            'label': '{}/{}'.format(f['ip_dst'], f['mask_dst']),
            'data': [d.bytes_exp for d in flow_data],
        }
        top_flows.append(flow)


    context = {
        'hours': hours,
        'dates': [d.strftime('%m%d-%H%M') for d in dates],
        'top_flows': top_flows,
        'flows': flows,
    }

    return render(request, 'top_prefixes.html', context)


def top_asns(request):
    return top_asns_hours(request, 0)

def top_asns_hours(request, hours):
    hours = int(hours)

    flows = Flow.objects.aggregate_bytes_per_as(hours)
    dates = [d for d in Flow.objects.get_dates()[-hours:]]

    list_asns = [a['as_dst'] for a in flows[:10]]
    top_flows = list()

    for asn in list_asns:
        flow_data = Flow.objects.aggregate_bytes_per_prefix_in_as(asn, hours)
        flow = {
            'label': asn,
            'data': [d['sum_bytes'] for d in flow_data],
        }
        top_flows.append(flow)

    context = {
        'hours': hours,
        'dates': [d.strftime('%m%d-%H%M') for d in dates],
        'top_flows': top_flows,
        'flows': flows,
    }

    return render(request, 'top_asns.html', context)
