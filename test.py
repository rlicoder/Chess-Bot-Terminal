import json

puz = {}

puz.update({"name": "123121"})
l = ['e2e4', 'g2g3']
puz.update({"sol": l})

x = [puz, puz]

json_object = json.dumps(x, indent = 4)

solset = {}
solset.update({"puzzles": x})
test = json.dumps(solset, indent = 4)

outfile = open('solset.txt', 'a')
outfile.write(test)
outfile.close()

f = open('solset.txt')
data = json.load(f)
f.close()
print(data)

