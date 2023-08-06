# Energy Models Package

                             THIS IS A PACKAGE OF MODELS OF PREDICT IN TIMESERIES FORECASTING                
             this package helps any developer in univariate and multivariate-multi-step time series forcasting in house-power-consumption dataset lets take a look about each type 
             Real-world time series forecasting is challenging for a whole host of reasons not limited to problem features such as having multiple input variables,the requirement 
             to predict multiple time steps,nd the need to a perform the same type of prediction for multiple physical sites.

# Installation

````
pip install EnergyModels
````

# Models list
  
  * LSTM 
  * BILSTM
  * GRU
  * BIGRU
  * TimeDistributer
  * CNN
  * TCN
  All models take 3 parameters except TCN :
    
    * must take value 
      -1 : n_steps
      -2 : n_features 
    * default value = 1 
      -3 : n_outputs  
      
  TCN Model you can build it by just give it data to build function
      
  
# Package Folders 
 
 * Data
 * models
 
# how to use the package

 first you must read the data set you want to use the models on it 
 and then import preprocess_data from Data folder :
 
 ````
 from Data import preprocess_data as pr
 
 df = pd.read_csv('Data.txt',sep=';', 
                  parse_dates={'date_time' : ['Date', 'Time']}, infer_datetime_format=True, 
                  low_memory=False, na_values=['nan','?'], index_col='date_time')

 pr.fill_missing(df.values)
 df.to_csv('new_data.csv')
 
 df = pd.read_csv('new_data.csv',parse_dates=['date_time'], index_col= 'date_time')
 ````
 
 next step you can use functions on preprocess_data to split and scale the data . 
 
   ````
   X_train, X_test = pr.train_test_split(df)
   X_train, X_test, scaler = pr.scale_data(X_train, X_test)
   ```` 
   
 After that converting the data to supervised.
 now you can build model by import it from models folder :
 
  ````
  from Energy_Models import Models as m
  model=m.lstm(21, 7 , 7 ).getModel()
  21 ==> n_steps
  7 ==> n_features
  7==>n_outputs
  ````
  
 After that you will able to predict and evaluate your models used. 
 
  ````
  y=model.predict(X)
  X==>input
  ````
 
 Models have evaluation function you can give it  the model and (actual , predicted) values 
 
  ````
  m.evaluate(model,actual,pred)
  ````
   
 Else you can calculate loss using metrics function for train and test both :
 
  ````
  m.print_metrics(model,Y_train,Y_pred_train,Y_test,Y_pred_test)
  ```` 