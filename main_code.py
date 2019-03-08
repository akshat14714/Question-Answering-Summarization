from summarize_2 import *
from select_answers import *
from pprint import pprint as pp
data = get_selected_answers()
c = 0
for ques in data:
	if c> 5:
		break
	answers=[]
	for i in ques['selected_ans']:
		answers.append(i['GBody'])
	if(len(answers) > 1):
		summary = summarize(answers)
		pp(ques)
		pp(summary)
		c+=1
print(c)