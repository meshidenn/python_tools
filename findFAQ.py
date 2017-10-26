import csv,sys,requests,json

def search_answer_finder(url, query):
    payload = {'type': 'recommend', 'text': query}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r


def extract_match_list(res, ans):
    obj        = json.loads(res.text)
    match_list = []
    for doc in obj['docs']:
        if ans == doc['fields']['ID']:
            match_list.append({ "id": doc['fields']['ID'], "score": doc['score'], "eq": True })
        else:
            match_list.append({ "id": doc['fields']['ID'], "score": doc['score'], "eq": False })

    return match_list


def print_as_json(row, match):
    print json.dumps({
      'no'         : row['no'],
      'annotation' : row['annotation'],
      'result'     : match
    })


def print_as_tsv(row, match):
    line = [
        row['no'],
        row['annotation'],
        match[0]['id'],
        str(match[0]['score']),
        str(match[0]['eq']),
        match[1]['id'],
        str(match[1]['score']),
        str(match[1]['eq']),
        match[2]['id'],
        str(match[2]['score']),
        str(match[2]['eq']),
        match[3]['id'],
        str(match[3]['score']),
        str(match[3]['eq']),
        match[4]['id'],
        str(match[4]['score']),
        str(match[4]['eq'])
    ]
    print( "\t".join(line) )


def search_faq():
    args = sys.argv
    with open(args[1], 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:

            row_dict = {
                'no'        : row[0],
                'question'  : row[1],
                'answer'    : row[2],
                'qa'        : row[3],
                'annotation': row[4],
            }

            # search AnserFinder API
            af_url     = 'http://localhost:8080/answer_finder/api/v1/documents/search'
            http_res   = search_answer_finder(af_url, row_dict['question'])
            match_list = extract_match_list(http_res, row_dict['annotation'])

            # print stdout
            if args[2] == 'json':
                print_as_json(row_dict, match_list)
            else:
                print_as_tsv(row_dict, match_list)
            

# main
search_faq()

