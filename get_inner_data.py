async def get_inner_data(session, response_json, template):
    outload_data = dict()
    add_request_key = template.get('add_request_key')
    outload_data_key = template.get('outload_data_key')
    key_to_name = template.get('key_to_name')

    for key in add_request_key + outload_data_key:
        inner_request_data = response_json.get(key)
        if key in outload_data_key:
            key_value = inner_request_data if inner_request_data is not [] else ''
            outload_data.setdefault(key, key_value)
            continue

        if isinstance(inner_request_data, str) and inner_request_data != '':
            url_list = [inner_request_data]

        else:
            url_list = inner_request_data

        needed_key = key_to_name.get(key)
        needed_value = ''
        if url_list is not []:
            for url in url_list:
                ad_response = await session.get(url)
                add_response_json = await ad_response.json()
                needed_value += f'{add_response_json.get(needed_key)}, '
        outload_data.setdefault(key, needed_value)

    await session.close()
    return outload_data
