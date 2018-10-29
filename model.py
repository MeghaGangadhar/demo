import  pandas as pd

model=pd.read_pickle("Face.pkl")

def predict(gender,smile,hair,age):
    #df_face_X=df_face.loc[:,['gender','smile','hair','age']]
#    gender ='female'
#    smile=0.1
#    hair='black'
#    age=23
    
    test=pd.DataFrame({"gender":[gender],"smile":[smile],"hair":[hair],"age":[age]})
    test=pd.get_dummies(test,columns=['gender','hair'])
    train_columns=['smile','age','gender_female','gender_male','hair_bald','hair_black','hair_blond','hair_brown','hair_gray','hair_invisible','hair_other','hair_red']
    
    missing_cols = set( train_columns ) - set( test.columns )
    # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        test[c] = 0
    # Ensure the order of column in the test set is in the same order than in train set
    test = test[train_columns]
    print(int(model.predict(test)))
   
    return int(model.predict(test))
    
#predict('male',0,'brown',35)
