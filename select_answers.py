from restructureSingle import *

def select_ans(Ans_arr):
    ans = []
    score = []
    for entry in Ans_arr:
        score.append(float(entry['GScore']))
    mean = float(np.mean(score))
    std  = float(np.std(score))
    for entry in Ans_arr:
        if float(entry['GScore']) > mean + std:
            ans.append(entry)
    return ans
def engine():
    data = get_data()
    for ques in data:
        selected_ans = select_ans(ques['Ans'])
        ques['selected_ans'] = selected_ans
if __name__ == "__main__":
    engine()