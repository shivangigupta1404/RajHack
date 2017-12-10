import csv,numpy,pandas
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
from sklearn import svm

clf=svm.SVC()
def prediction_model():
    print("fitting model")
    filename='sfg/trainLabels.csv'
    names=['image','level']
    data = pandas.read_csv(filename, names=names)
    im=data.image
    image=im.values.reshape(-1, 1)
    X, y = image, data.level
    clf.fit(X, y)
    print("model is now fit")

def predict(val):
    pred=clf.predict(numpy.asarray(val))
    return(pred)