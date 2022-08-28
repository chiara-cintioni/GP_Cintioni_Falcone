# The above code is sorting the data in the file and writing the sorted data to a new file.
k = []
with open('taxmap.txt','r') as dat, open('output.txt','w') as f:
    # Sorting the data in the file and writing the sorted data to a new file.
    for i in dat:
        res = i.split('	')
        # Taking the 5th element of the list and assigning it to the variable word.
        word = res[4]
        if res not in k:
          k.append(res)
          f.write(' '.join([str(m) for m in res]) +'\n')


