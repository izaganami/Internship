
jsondict={'-1': {'start': 'null', 'end': 'null', 'label': 'null'}, '-2': {'start': 'null0', 'end': 'null0', 'label': 'null0'}, '1': {'start': '00:00:0.09', 'end': '00:00:0.18', 'label': 'AS02'}, '90': {'start': '00:00:8.24', 'end': '00:00:8.34', 'label': 'F02'
}, 116: {'start': '00:00:10.63', 'end': '00:00:10.72', 'label': 'AS02'}, '118': {'start': '00:00:10.81', 'end': '00:00:10.90', 'label': 'AS02'}, '120': {'start': '00:00:10.99', 'end': '00:00:11.08', 'label': 'AS02'}, '122': {'start': '00:00:11.18',
'end': '00:00:11.27', 'label': 'AS02'}, '124': {'start': '00:00:11.36', 'end': '00:00:11.45', 'label': 'AS02'}, 126: {'start': '00:00:11.54', 'end': '00:00:11.63', 'label': 'AS02'}, '128': {'start': '00:00:11.73', 'end': '00:00:11.82', 'label': 'AS02'}}
print(sorted(jsondict.keys(),reverse=True))
[final_elem,before_final_elem]=sorted(jsondict.keys(),reverse=True)[0:2]
final_elem = jsondict[final_elem]['label']
before_final_elem = jsondict[before_final_elem]['label']
print(final_elem + " " + before_final_elem)
print(final_elem+" "+before_final_elem)

