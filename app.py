'''|**********************************************************************|
* Project           : MiniML Model Selector, Classification, Prototype 1
*
* Program name      : MiniML Webapp (app.py)
*
* Author            : Rajath_Kotyal
*
* Date created      : 06/07/2020
*
* Purpose           : To choose the Best Fitted Classification Model for any given dataset
*                     in order to the reduce time costraint of developers.
*
* Revision History  :
*
*   Date             Author           Ref                Revision
*
|**********************************************************************|'''

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, precision_recall_curve
from sklearn.metrics import precision_score, recall_score
from PIL import Image
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier


ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "black",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#82E1D7",
                              "theme.textColor": "#0a1464",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()

def local_css():
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        hide_footer_style = """
        <style>
        .reportview-container .main footer {visibility: hidden;}
        """
        st.markdown(hide_footer_style, unsafe_allow_html=True)

def main():
    #st.markdown("<h1 style='text-align: left; color: black;'>Model Selector</h1>", unsafe_allow_html=True)
    st.markdown("# MiniML Model Selector 👨‍💻")
    image = Image.open('mini.png')
    st.sidebar.image(image, width = 150)
    st.sidebar.markdown("# Hey There!! ✌️")
    st.header("Choose the Best Classification Model for your Dataset")
    st.markdown("1. Upload your Classifier Dataset with the below format ")
    # image = Image.open('table.png')
    st.image(image, width = 270)
    st.markdown("- where X are the **features** & Outcome is the Output **Vector Y** Containing values 0 or 1 ")
    st.markdown("2. Make sure all the values are **Integer/Float** & there are **NO** missing values.")
    st.markdown("__Sample dataset__ is provided below 🍻")


    uploaded_file = st.file_uploader("Upload the CSV to continue", type="csv")


#LOADING FILE.
    
    def sample_load_data():
        sample_data = pd.read_csv('sampleDiabetes.csv')
        return sample_data

    sample_df = sample_load_data()

    def test_data():
        tdata = pd.read_csv('sampleDiabetes.csv')
        return tdata

    def load_data():
        try:
            data = pd.read_csv(uploaded_file)
            return data
        except:
            print('Upload a Proper File ')
    if st.checkbox("View Sample dataset", False):
        st.subheader("Sample Diabetes Dataset")
        st.write(sample_df)



    if st.checkbox("Test Program Using Sample Data", True):
        df= test_data()
    else :
        df= load_data()

    st.markdown('[Documentation - Read this for more info](https://github.com/rajathkotyal/Optimum_Model_Selector_Classification "Click this if you need help")')
    st.markdown('[About the Developer](https://www.linkedin.com/in/rajathkotyal)')
    st.markdown('[Click here to download the Sample Dataset (For Testing)](https://drive.google.com/uc?export=download&id=10QQHW-wKlm5rKTV6DeSkuz4SRdpHr70K)')
    #st.text('[ If u see a red error box below. Please upload the CSV file with the proper format ]')
#ASSIGNING FEATURES X AND OUTPUT VECTOR Y
#SPLITTING DATASET
    
    def split(df):
        y=df.Outcome.astype(float)
        x=df.drop(columns=['Outcome']).astype(float)
        x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.25)
        return x_train, x_test,y_train,y_test
        


#PLOTTING MATRICES
    def plot_metrics(metrics_list):
        if 'Confusion Matrix' in metrics_list:
            st.subheader("Confusion Matrix :")
            ConfusionMatrixDisplay.from_estimator(model, x_test, y_test, display_labels=class_names)
            st.pyplot()
            st.markdown('[Click me to know more about Confusion Matrices](https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62)')
    
        if 'ROC Curve' in metrics_list:
            st.subheader("ROC curve :")
            y_pred_prob = model.predict_proba(x_test)[:, 1]  # Get the predicted probabilities for the positive class
            fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
            # Plot the ROC curve
            plt.plot(fpr, tpr)
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            st.pyplot()
            st.text('AUC - Area Under Curve -> Higher the better Accuracy')
            st.markdown('[Click me to know more about ROC & AUC](https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5)')
    
        if 'Precision Recall Curve' in metrics_list:
            st.subheader("Precision Recall Curve:")
            y_pred_prob = model.predict_proba(x_test)[:, 1]  # Get the predicted probabilities for the positive class
            precision, recall, thresholds = precision_recall_curve(y_test, y_pred_prob)
            # Plot the Precision-Recall curve
            plt.plot(recall, precision)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            st.pyplot()
            st.text('AP - Average Precision')
            st.markdown('[Click me to know more about Precision Recall Curve](https://www.geeksforgeeks.org/precision-recall-curve-ml/)')

#CALLING FUNCTIONS & CHOOSING CLASSIFIER

    #df = load_data()
    x_train,x_test,y_train,y_test = split(df)
    class_names = ['Positive','Negative']
    st.sidebar.subheader("Choose Classifier")
    classifier = st.sidebar.selectbox("Classifier",("Support Vector Machine","LogisticRegression","RandomForestClassifier","GaussianNB","KNeighborsClassifier","SGD_Classifier"))


#SUPPORT VECTOR MACHINE
    if classifier == 'Support Vector Machine':
        st.sidebar.subheader("Select Hyperparameters")
        C = st.sidebar.number_input("C = Regularisation Parmeter (Lower the better)", 0.01, 10.0, step=0.01, key='C')
        kernel = st.sidebar.radio("Kernel",("rbf","linear"), key = 'kernel')
        gamma = st.sidebar.radio("Gamma(Kernel Co-eff)",("scale","auto"),key='gamma')

        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("SVM Results : ")
            model = SVC(C=C, kernel=kernel, gamma=gamma)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)

#LogisticRegression
    if classifier == 'LogisticRegression':
        st.sidebar.subheader("Select Hyperparameters")
        C = st.sidebar.number_input("C = regularisation Parameter (Lower the better)", 0.01, 10.0, step=0.01, key='C_LR')
        max_iter = st.sidebar.slider("Maximum number of iterations", 100,500,key='max_iter')
        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("LogisticRegression Results : ")
            model = LogisticRegression(C=C, max_iter=max_iter)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)


#RANDOM FOREST CLASSIFIER
    if classifier == 'RandomForestClassifier':
        st.sidebar.subheader("Select Hyperparameters")
        n_estimators = st.sidebar.number_input("The number of trees in forest",100,5000,step=10, key='n_estimators')
        max_depth = st.sidebar.number_input("The maximum depth of the tree",1,20,step=1,key='max_depth')
        bootstrap = st.sidebar.radio("Bootstrap Samples whe building Trees : ",('True','False'),key='bootstrap')
        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("RandomForestClassifier Results : ")
            model = RandomForestClassifier(n_estimators = n_estimators, max_depth=max_depth, bootstrap=bootstrap)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)

#GaussianNB
    if classifier == 'GaussianNB':
        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))
        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("GaussianNB Results : ")
            model = GaussianNB()
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)

#KNeighborsClassifier
    if classifier == 'KNeighborsClassifier':
        st.sidebar.subheader("Select Hyperparameters")
        n_neighbors = st.sidebar.slider("The number of neighbors to consider : ",1,10,step=1,key='n_neighbors')
        algorithm = st.sidebar.selectbox("Algorithm",("auto","ball_tree","kd_tree","brute"),key='algorithm')
        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))

        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("K Nearest Results : ")
            model = KNeighborsClassifier(n_neighbors=n_neighbors,algorithm=algorithm)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)

#Stochastic Gradient Descent
    if classifier == 'SGD_Classifier':
        st.sidebar.subheader("Default Hyperparameters Set")
        #alpha = st.sidebar.selectbox("Regularization Parameter: ",("0.001","0.01","0.1","0.5"),key='alpha')
        #max_iter = st.sidebar.number_input("Maximum number of iterations", 1000,5000,key='max_iter')
        # *issue with datatype
        metrics = st.sidebar.multiselect("Choose the metrics : ",('Confusion Matrix','ROC Curve','Precision Recall Curve'))
        if st.sidebar.button("Classify", key = 'classify'):
            st.subheader("SGDClassifier Results : ")
            model = SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol=0.001, shuffle=True, verbose=0,
            epsilon=0.1, n_jobs=None, random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
            class_weight=None, warm_start=False, average=False)
            model.fit(x_train, y_train)
            accuracy = model.score(x_test,y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy : ", accuracy.round(2))
            st.write("Precision : ", precision_score(y_test, y_pred, labels= class_names).round(2))
            st.write("Recall : ", recall_score(y_test, y_pred, labels= class_names).round(2))
            plot_metrics(metrics)

#External docs
# local_css("styles.css")

if __name__ == "__main__" :
    main()

print("Whoops!")
