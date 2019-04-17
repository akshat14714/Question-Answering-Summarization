import json
from pprint import pprint
def remove_tags(inp):
    ans = []
    all_tags = ['<p>', '<a>', '<b>', '<blockquote>', '<code>', '<del>', '<dd>', '<dl>', '<dt>', '<em>', '<h1>', '<h2>', '<h3>', '<i>', '<img>', '<kbd>', '<li>', '<ol>', '<p>', '<pre>', '<s>', '<sup>', '<sub>', '<strong>', '<strike>', '<ul>', '<br>', '<hr>']
    all_tags2 = ['</p>', '</a>', '</b>', '</blockquote>', '</code>', '</del>', '</dd>', '</dl>', '</dt>', '</em>', '</h1>', '</h2>', '</h3>', '</i>', '</img>', '</kbd>', '</li>', '</ol>', '</p>', '</pre>', '</s>', '</sup>', '</sub>', '</strong>', '</strike>', '</ul>', '</br>', '</hr>']
    for arr in inp:
        for tag in all_tags:
            arr['GBody'] = arr['GBody'].replace(tag, '')
        for tag in all_tags2:
            arr['GBody'] = arr['GBody'].replace(tag, '')
        ans.append(arr)
    return ans
def load_data(filename):
    try:
        with open(filename,'r') as f:
            data = json.load(f)
        return data
    except :
            print("Error in opening " +filename +" file")
            sys.exit(0)
def engine():
    filename = 'query_full.json'
    data = load_data(filename)
    # pprint(data)
    # print("\n\n\n")
    for ques in data:
        # print(ques)
        data[ques]['Ans'] = remove_tags(data[ques]['Ans'])
    # pprint(data)
    with open('query_full_.json','w') as f:
        json.dump(data,f)

if __name__ == '__main__':
    engine()