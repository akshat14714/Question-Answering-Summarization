from restructureSingle import *

def select_ans(Ans_arr):
    ans = []
    score = []
    for entry in Ans_arr:
        score.append(float(entry['GScore']))
    mean = float(np.mean(score))
    std  = float(np.std(score))
    for entry in Ans_arr:
        if float(entry['GScore']) >= mean + std:
            ans.append(entry)
    return ans

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

def engine():
    data = get_data()
    for ques in data:
        selected_ans = select_ans(ques['Ans'])
        ques['selected_ans'] = remove_tags(selected_ans)
        print(ques['selected_ans'])
        print()

if __name__ == "__main__":
    engine()