import numpy as np
import pandas as pd
from scipy import optimize, stats
from Model import Model


class ChangePointModel(Model):

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 dependent_df=None, temperature_df=None,
                 additional_vars_df=None, model_name="3PH"):
        """
        Initialize object by ensuring data provided is fit for modeling and
        noting model specs.
        Parameters
        ----------
        df : Pandas DataFrame, optional
            A preprocessed dataframe that includes a timestamp column,
            dependent variable column, and other regressor variables. No other
            variables should be included. The default is None.
        dependent_col : str, optional
            Needed to mark what the dependent variable will be in the pre-
            processed dataframe. Not used if a preprocessed dataframe is not
            supplied. The default is "load".
        temperature_col : str, optional
            Needed to mark what the temperature variable is in the preprocessed
            dataframe, if a temperature column exists. If one is not needed for
            modeling, input None. Not used if a preprocessed dataframe is not
            supplied. The default is "temp".
        occupancy_col : str, optional
            Needed to mark what the binary occupied variable is in the
            preprocessed dataframe or additional variables dataframe, if a
            occupancy column exists. If one is not supplied, an occupancy
            schedule can be estimated based off the load. If separate
            occupied/unoccupied models are not wanted, change the occ_threshold
            to 1. The default is None.
        dependent_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and a dependent variable
            column. If wanting to train a model and a preprocessed dataframe
            is not supplied, this is needed. The default is None.
        temperature_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and a temperature column.
            If the desired model is assuming the dependent variable is
            dependent on temperature, this dataframe is needed. The default is
            None.
        additional_vars_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and other regressor
            variables. This is merged with the dependent_df dataframe.
            The default is None.
        model_name : str, optional
            Specific model name.
            Options are: SLR, 3PC, 3PH, 4P, 5P.
            Upper or lower case is accepted. Default is 3PH.

        Raises
        ------
        ValueError
            If specifed changepoint type is not recognized or not provided
        Returns
        -------
        None.
        """
        super().__init__(df=df,
                         dependent_col=dependent_col,
                         temperature_col=temperature_col,
                         dependent_df=dependent_df,
                         temperature_df=temperature_df,
                         additional_vars_df=additional_vars_df,
                         model_name=model_name)

        if self.model_name not in ["SLR", "3PH", "3PC", "4PH", "4PC", "5P"]:
            raise ValueError("Unknonwn model type: " + self.model_name + ". "
                             "Please specify model_name as"
                             " 'SLR', '3PH', or '3PC', '4PH, '4PC' or '5P'.")
            
        if self.model_name == "SLR":
            self.model = self.SLR
            self.feature_names_in_ = ["slp", "y_int"]     
            
        if self.model_name == "3PH":
            self.model = self.piecewise_3PH
            self.feature_names_in_ = ["hcp", "base", "hsl"]
            
        if self.model_name == "3PC":
            self.model = self.piecewise_3PC
            self.feature_names_in_ = ["ccp", "base", "csl"]
        
        if self.model_name == "4PH":
            self.model = self.piecewise_4PH
            self.feature_names_in_ = ["hcp", "base", "hsl1", "hsl2"]
            
        if self.model_name == "4PC":
            self.model = self.piecewise_4PC
            self.feature_names_in_ = ["ccp", "base", "csl1", "csl2"]
            
        # self.occ_model = self.model
        # self.unocc_model = None
            
    @staticmethod
    def SLR(x, slp, y_int):
        """ 3-parameter heating functional form
        
        Parameters
        ----------
        x: array, temperatures
        slp: float, slope
        y_int: float, y-intercept
        
        Returns
        -------
        numpy piecewise function
        
        """
        conds = [x]
        
        funcs = [lambda x: slp * x + y_int]
        
        return np.piecewise(x, conds, funcs)

        
    @staticmethod
    def piecewise_3PH(x, hcp, base, hsl):
        """ 3-parameter heating functional form
        
        Parameters
        ----------
        x: array, temperatures
        hcp: float, heating change point
        base: float, non-heating constant
        hsl: float, heating slope
        
        Returns
        -------
        numpy piecewise function
        
        """
        conds = [x < hcp, x >= hcp]
        
        funcs = [lambda x: hsl * (x-hcp) + base,
                 lambda x: base]
        
        return np.piecewise(x, conds, funcs)

    @staticmethod
    def piecewise_3PC(x, ccp, base, csl):
        """ 3-parameter cooling functional form
        
        Parameters
        ----------
        x: array, temperatures
        ccp: float, cooling change point
        csl: float, cooling slope
        base: float, non-heating constant

        Returns
        -------
        numpy piecewise function

        """
        conds = [x <= ccp, x > ccp]
        
        funcs = [lambda x: base,
                 lambda x: csl * (x-ccp) + base]
        
        return np.piecewise(x, conds, funcs)
    
    @staticmethod
    def piecewise_4PH(x, hcp, base, hsl1, hsl2):
        """ 4-parameter heating functional form
        
        Parameters
        ----------
        x: array, temperatures
        hcp: float, change point
        base: float, constant
        hsl1: float, heating slope 1
        hsl2: float, heating slope 2
        
        Returns
        -------
        numpy piecewise function
        
        """
        conds = [x < hcp, x >= hcp]
        
        funcs = [lambda x: hsl1 * (x-hcp) + base,
                 lambda x: hsl2 * (hcp-x) + base]
        
        return np.piecewise(x, conds, funcs)
    
    @staticmethod
    def piecewise_4PC(x, ccp, base, csl1, csl2):
        """ 4-parameter cooling functional form
        
        Parameters
        ----------
        x: array, temperatures
        ccp: float, change point
        base: float, constant
        csl1: float, cooling slope 1
        csl2: float, cooling slope 2
        
        Returns
        -------
        numpy piecewise function
        
        """
        conds = [x < ccp, x >= ccp]
        
        funcs = [lambda x: csl1 * (x-ccp) + base,
                 lambda x: csl2 * (ccp-x) + base]
        
        return np.piecewise(x, conds, funcs)
    
    

    def get_bounds(self, temperature):
        """
        Get temperature bounds for piecewise linear parameters

        Parameters
        ----------
        temperature : array, temperatures

        Returns
        -------
        bounds: dictinary of values

        """
        hcp_bound_percentile = 45
        ccp_bound_percentile = 55

        percentiles = hcp_bound_percentile, ccp_bound_percentile
        # heating change point, cooling change point
        hcp, ccp = np.percentile(temperature, percentiles)

        hcp_min = hcp  # Heating change-point minimum
        hcp_max = ccp  # Heating change-point maximum
        ccp_min = hcp  # Cooling change-point minimum
        ccp_max = ccp  # Cooling change-point minimum
        base_min = 0  # Baseload minimum
        base_max = np.inf  # Baseload maximum
        hsl_min = -np.inf  # Heating slope minimum
        hsl_max = 0  # Heating slope maximum
        csl_min = 0  # Cooling slope minimum
        csl_max = np.inf  # Cooling slope maximum
        
        if self.model_name == "SLR":
            training_bounds = ([hsl_min, base_min],
                               [csl_max, base_max])
            
        elif self.model_name == "3PH":
            training_bounds = ([hcp_min, base_min, hsl_min], 
                               [hcp_max, base_max, hsl_max])
            
        elif self.model_name == "3PC":
            training_bounds = ([ccp_min, base_min, csl_min], 
                               [ccp_max, base_max, csl_max])
            
        elif self.model_name == "4PH":
            training_bounds = ([hcp_min, base_min, hsl_min, hsl_min], 
                               [hcp_max, base_max, hsl_max, hsl_max])
            
        elif self.model_name == "4PC": 
            training_bounds = ([ccp_min, base_min, csl_min, csl_min], 
                               [ccp_max, base_max, csl_max, csl_max])
            
        else:
            raise ValueError(
                'Incorrect changepoint type specified: ' + self.model_name + '.')
        return training_bounds
    
    
    def fit_model(self, x, y):
        """
        Fit a change point model to the data.

        Parameters
        ----------
        x : numpy array
            Temperature
        y : numpy array
            Load

        Returns
        -------
        y_fit : numpy array
            Fitted load values

        """
        x = np.array(x)
        y = np.array(y)
        model_bounds = self.get_bounds(temperature = x)
        
        p, e = optimize.curve_fit(f = self.model, 
                                  xdata = x, 
                                  ydata = y, 
                                  bounds = model_bounds)
        y_fit = self.model(x, *p)
        return p, y_fit
    

    def train(self, interval=None):
        """
        Training method for change point models (SLR, 3PC, 3PH, 4P, 5P)

        Parameters
        ----------
        interval: str, optional
            Desired interval to aggregate data to for training. 
            If None is provided then the finest granulairty possible is used.

        Returns
        -------
        Pandas Dataframe 
            Origianl training data with fitted values added
        """
        if interval is None:
            interval = self.min_interval
        
        min_available_interval_num = self.interval_tiers[self.min_interval]
        desired_interval_num = self.interval_tiers[interval]

        if min_available_interval_num > desired_interval_num:
            self.df = self.group_interval(time_interval=interval,
                                          time_col=self.timestamp_col)
         
        if min_available_interval_num < desired_interval_num:
            raise ValueError(
                'Desired interval: ' + interval + 
                ' is unavailable. Finest granularity interval is ' + 
                self.min_interval + '.')
        self.model_interval = interval
        
        train = self.df.dropna().copy()
        
        x_train = train[self.temperature_col]
        y_train = train[self.dependent_col]
        
        self.coef_ , y_fit = self.fit_model(x_train, y_train)
        
        train_estimate = pd.DataFrame({'time': train[self.timestamp_col],
                                   'temp': train[self.temperature_col],
                                   'load': train[self.dependent_col],
                                   'y_fit': y_fit}) 
        return train_estimate


    def predict(self, df=None, model=None):
        
        if df is None:
            raise ValueError(
                'No prediction df specified. Please pass a df to predict on.')
        if self.model is None:
            raise ValueError(
                'No trained model. Please train a model.')
        
        # predict_ts_col = self.__check_timestamp_col(df)

        predict_interval = self.infer_interval(df)
        
        min_predict_interval_num = self.interval_tiers[predict_interval]
        model_interval_num = self.interval_tiers[self.model_interval]

        if min_predict_interval_num > model_interval_num:
            df = self.group_interval(time_interval=self.model_interval,
                                          time_col=self.timestamp_col)
        
        if min_predict_interval_num < model_interval_num:
            raise ValueError(
                'Modeled interval: ' + self.model_interval + 
                ' does not match data interval: ' + predict_interval + '.')
        
        main = df.dropna().copy()
        x_pred = np.array(main[self.temperature_col])
        y_pred = self.model(x_pred, *self.coef_)
        
        predictions = pd.DataFrame({'time': main[self.timestamp_col],
                                   'temp': main[self.temperature_col],
                                   'y_pred': y_pred}) 
        
        return predictions
        
