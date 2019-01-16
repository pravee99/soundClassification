import pandas as pd
import numpy as np
from pyAudioAnalysis import audioBasicIO 
from pyAudioAnalysis import audioFeatureExtraction
from sklearn import svm
from sklearn.metrics import accuracy_score,confusion_matrix, classification_report


def create_featureMatrix(path, type):
    arr = []
    list = []
    for i in range(1, 21):
        full_path = path + type + str(i) + ".wav"
        #Extract Sample Frequency & Samples
        [Fs, x] = audioBasicIO.readAudioFile(full_path)
        #Extract Time-domain & Frequency-domain features by using window size of 50ms & step size of 25ms
        F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs)
        #Tranposing feature Matrix of type n_samples * features
        Feature_Matrix = F.T
        # Assign label to samples from a file
        Feature_Matrix = np.insert(Feature_Matrix, Feature_Matrix.shape[1], i, 1)
        if i == 1:
            arr = Feature_Matrix
            list = f_names
        else:
            arr = np.append(arr, Feature_Matrix, axis=0)
    return (arr, list)
        
def music_speech():
    path = "../audio_data/music/"
    type = "mu"
    music_arr, list = create_featureMatrix(path, type)
   
    path = "../audio_data/speech/"
    type = "sp"
    speech_arr, list = create_featureMatrix(path, type)
    list.append("fileNumber")
    print("List of features extracted: "+ str(list))
    
    train_data, test_data = concatenate(music_arr, speech_arr, list)
    return train_data, test_data
    
# Assigns label to Speech & Music dataset and concatenates 2/3rds of both 
# to form the training dataset. The remaining data is testing data 
def concatenate(music_arr, speech_arr, list):
    ma = pd.DataFrame(music_arr, columns=[list])
    ma['Label'] = "Yes"  #MUSIC
    count = int((2/3) * len(music_arr))
    train_data = ma.iloc[ 0:count+1, :] 
    test_data  = ma.iloc[count+1:, :] 
    
    
    sa = pd.DataFrame(speech_arr, columns=[list])
    sa['Label'] = "No" #SPEECH
    count = int((2/3) * len(speech_arr))
    train_data = train_data.append(sa.iloc[0:count+1, :])
    test_data = test_data.append(sa.iloc[count+1:, :])
    
    return train_data, test_data   

#Train model - SVM classifier
def train_model(X, Y, test):
    clf = svm.SVC(kernel='linear').fit(X, Y)
    y_pred = clf.predict(test.iloc[:, :-2])
    y_true = test.iloc[:, -1:]
    
    accuracy = accuracy_score(y_true, y_pred)
    print("Accuracy score: " + str(accuracy))
    print("Predicted values/Model output "+ str(y_pred))
    print("Ground Truth label: "+ str(y_true))
    
    confusionMatrix = confusion_matrix(y_true, y_pred)
    print("Confusion matrix:\n "+ str(confusionMatrix))
    print("classification report: \n" +str(classification_report(y_true, y_pred)))
    

def main():
    train, test  = music_speech()
    
    print("# of Music samples in training data: " + str((train['Label'] == 'Yes').sum()))
    print("# of Speech samples in training data: " + str((train['Label'] == 'No').sum()))  
    
    print("# of music samples in testing data: "+str((test['Label'] == 'Yes').sum()))
    print("# of speech samples in testing data: "+str((test['Label'] == 'No').sum()))
 
    X = train.iloc[:, :-2]  # training 
    Y = train.iloc[:, -1:]    # file label 
    #consider 34 features from both time and frequency domain
    print("Consider 34 features: ")
    train_model(X,Y, test)
    

    print("Consider 3 features: ")
    X = X.loc[:, ['zcr', 'spectral_entropy', 'spectral_flux']]
    test = test.loc[:, ['zcr', 'spectral_entropy', 'spectral_flux', 'fileNumber', 'Label']]
    #consider 3 features both from time and frequency domain
    train_model(X, Y, test)

    
    
    
    
main()
    
    
