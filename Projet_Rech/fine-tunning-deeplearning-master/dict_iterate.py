dict={1: {'start': '00:00:0.06', 'end': '00:00:0.12', 'label': 'F18', 'prob': '60.00%'},
      43: {'start': '00:00:2.61', 'end': '00:00:2.67', 'label': 'F04', 'prob': '18.00%'},
      175: {'start': '00:00:10.60', 'end': '00:00:10.67', 'label': 'AS00', 'prob': '99%'},
      250: {'start': '00:00:15.15', 'end': '00:00:15.21', 'label': 'F12', 'prob': '13.00%'},
      314: {'start': '00:00:19.03', 'end': '00:00:19.21', 'label': 'F03', 'prob': '20.00%'}}
elem=[]
for elt,value in dict.items():
    if float(value['prob'][0:-1]) < 60:
        elem.append(elt)
for e in elem:
    del dict[e]
print(dict)