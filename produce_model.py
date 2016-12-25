import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib

def main():
	inputfv = open('feature_vector.txt', 'r')
	inputfr = open('feature_result.txt', 'r')
	line = inputfv.readline()
	Xa = list()
	while line:
		fs = line.split(" ")
		arr = list()
		for f in fs:
			if f[0] == '\n':
				continue
			arr.append(float(f))
		Xa.append(arr)
		line = inputfv.readline()
	X = np.array(Xa)
	inputfv.close()
	line = inputfr.readline()
	Ya = list()
	while line:
		a = int(line[0])
		Ya.append(a)
		line = inputfr.readline()
	Y = np.array(Ya)
	inputfr.close()
	clf = SVC()
	clf.fit(X, Y)
	joblib.dump(clf, 'model.pkl')

if __name__ == '__main__':
	main()
