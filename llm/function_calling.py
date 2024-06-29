import regex,json

def find_json(content):
    json_pattern = r"\{.*\}"
    json_result = regex.findall(json_pattern, content)
    return json_result

def parse_to_json(content):
    if content is None:
        return None
    json_result = find_json(content)
    if len(json_result) == 0:
        return None
    try:
        content = json.loads(json_result[0])
        return content
    except Exception as e:
        return None