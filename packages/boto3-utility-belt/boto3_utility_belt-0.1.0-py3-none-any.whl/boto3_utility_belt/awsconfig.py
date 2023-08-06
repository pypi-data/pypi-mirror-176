import json

try:
    import botostubs
except ImportError:
    pass


def _get_config_aggregator_name(session, region_name="us-east-1", aggregator_name=None):
    config = session.client("config", region_name=region_name)
    response = config.describe_configuration_aggregators()
    if aggregator_name:
        aggregator = [
            agg
            for agg in response["ConfigurationAggregators"]
            if agg["ConfigurationAggregatorName"] == aggregator_name
        ]
        if not aggregator:
            raise Exception(
                f"Configuration aggregator {aggregator_name} does not exist"
            )
    else:
        aggregators = response["ConfigurationAggregators"]
        aggregator_count = len(aggregators)
        if aggregator_count == 1:
            aggregator_name = aggregators[0]["ConfigurationAggregatorName"]
        else:
            raise Exception(
                f"{aggregator_count} configuration aggregators found. Unable to determine default aggregator."
            )
    return aggregator_name


def query_config(session, query, region_name="us-east-1"):
    config = session.client("config", region_name=region_name)
    paginator = config.get_paginator("select_resource_config")
    results = []
    response_iterator = paginator.paginate(Expression=query)
    for response in response_iterator:
        for instance in response["Results"]:
            instance_obj = json.loads(instance)
            results.append(instance_obj)
    return results


def query_aggregate_config(
    session, query, region_name="us-east-1", aggregator_name=None
):
    aggregator_name = _get_config_aggregator_name(
        session, region_name=region_name, aggregator_name=aggregator - name
    )
    config = session.client("config", region_name=region_name)
    paginator = config.get_paginator("select_aggregate_resource_config")
    results = []
    response_iterator = paginator.paginate(
        Expression=query, ConfigurationAggregatorName=aggregator_name, MaxResults=100
    )
    for response in response_iterator:
        for item in response["Results"]:
            item_obj = json.loads(item)
            results.append(item_obj)
    return results


def tableize(items):
    results = []
    key_set = set()
    for item in items:
        tags = {tag["key"]: tag["value"] for tag in item.get("tags", [])}
        if tags:
            item["tags"] = tags
        item = _flatten_obj(item)
        results.append(item)
        key_set.update(set(item.keys()))
    keys = sorted(list(key_set))
    return keys, results


def _flatten_obj(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def _all_keys(items):
    key_set = set()
    for item in items:
        key_set.update(set(item.keys()))
    return sorted(list(key_set))
