from Model import Model
import pandas as pd
from sklearn.linear_model import LinearRegression


class TOWTModel(Model):

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 occupancy_col=None, dependent_df=None, temperature_df=None,
                 additional_vars_df=None, occ_threshold=0.65,
                 knot_temps=[40, 55, 65, 80, 90], model_name="TOWT"):
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
        occ_threshold : float, optional
            Percentage of time assumed to be occupied. The default is 0.65.
        knot_temps : list, optional
            List of knot temperatures for TOWT models. The default is
            [40, 55, 65, 80, 90].
        model_name : str, optional
            Specific model name.
            Options are: TOW, TOWT
            Upper or lower case is accepted. Default is TOWT.
            
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
                         occupancy_col=occupancy_col,
                         model_name=model_name)
        self.temp_train_cols = []
        self.tow_train_cols = []
        self.knot_temps = knot_temps
        self.occ_threshold = occ_threshold
        
        if self.model_name not in ["TOWT", "TOW"]:
            raise ValueError("Unknonwn model type: " + self.model_name + ". "
                             "Please specify model_name as TOW or TOWT.")

    def train(self, interval=None, knot_temps=None):
        """
        Training method for TOWT and TOW model.
        Parameters
        ----------
        model : str, optional
            String that to run either time of week and temperature model or
            just time of week. The default is "TOWT".
        knot_temps : list, optional
            List of knot_temps at least of length 2. Will rewrite class
            knot_temps attribute. The default is None.
        Raises
        ------
        ValueError
            If inferred time interval is monthly, the error will raise.
        Returns
        -------
        Pandas DataFrame
            The main dataframe with all the temp knot and time of week
            variables used for regression attached to it.
        """
        # Checks
        if (knot_temps != self.knot_temps) & (knot_temps is not None):
            self.knot_temps = knot_temps

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
                ' is unavailable. Highest granularity is ' + 
                self.min_interval + '.')

        # Check if time_interval is monthly
        if interval == "Monthly":
            raise ValueError(
                'Inferred time interval is monthly. The TOWT'
                ' algorithm expects hourly or daily data.')
        
        self.model_interval = interval

        # Define knot temp vars and tow vars
        used_knot_temps = pd.DataFrame()
        temp_vars = pd.DataFrame()
        self.x_train_cols = list(set(self.x_train_cols)
                                 - set(self.temp_train_cols
                                       + self.tow_train_cols))
        if self.model_name == "TOWT":
            temp_vars, used_knot_temps = self.define_temp_vars(
                self.df, self.knot_temps)
            self.temp_train_cols = list(temp_vars.columns)
            self.x_train_cols = self.x_train_cols + self.temp_train_cols
        tow_vars = self.define_tow_vars(self.df, self.model_interval)
        self.tow_train_cols = list(tow_vars.columns)
        self.x_train_cols = self.x_train_cols + self.tow_train_cols

        # Assemble regression datasets
        if self.occupancy_col is None:
            self.df = self.find_occ_unocc(time_interval=self.model_interval)
            self.occupancy_col = 'occ'

        main = pd.concat([self.df, temp_vars, tow_vars], axis=1)
        train = main.dropna().copy()

        # Create models and predict
        # Occupied model
        occ_x_train = train.loc[train[self.occupancy_col]
                                == 1, self.x_train_cols]
        occ_y_train = train.loc[train[self.occupancy_col]
                                == 1, self.dependent_col]
        occ_model = LinearRegression().fit(occ_x_train, occ_y_train)
        self.occ_model = occ_model

        # Unoccupied model
        if train[self.occupancy_col].nunique() > 1:
            unocc_x_train = train.loc[train[self.occupancy_col]
                                      == 0, self.x_train_cols]
            unocc_y_train = train.loc[train[self.occupancy_col]
                                      == 0, self.dependent_col]
            unocc_model = LinearRegression().fit(unocc_x_train, unocc_y_train)
            self.unocc_model = unocc_model

        '''
        occ_model, occ_train = model_and_predict(train=train, occupied=True)
        # Unoccupied model
        unocc_model = None
        unocc_train = pd.DataFrame()
        if train['occ'].nunique() > 1:
            unocc_model, unocc_train = model_and_predict(
                train=train, occupied=False)
        # Merge dataset back together
        train_estimate = pd.concat([occ_train, unocc_train])
        train_estimate = pd.concat([main, train_estimate['predict']], axis=1)
        # Get metrics
        metrics = {'R2': R2(train_estimate),
                   'adj R2': adjR2(train_estimate),
                   'CVRMSE': cvrmse(train_estimate),
                   'NMBE': nmbe(train_estimate)}
        # Create dictionary for model/function outputs
        output = {"occupied model": occ_model,
                  "unoccupied model": unocc_model,
                  "data": train_estimate,
                  'knot_temps': (knot_temps, used_knot_temps),
                  'metrics': metrics}
        return(output)
        '''
        return(main)

    def predict(self, df, occ_model=None, unocc_model=None):
        """
        Predict method for TOWT and TOW models.
        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe consisting of at least time['time'] and occupancy['occ'].
            Temp is needed for TOWT.
        occ_model : sklearn LinearRegression object, optional
            Regression object for occipied model. This is required. If None,
            will assume it is an object attribute.
        unocc_model : sklearn LinearRegression object, optional
            Regression object for unoccipied model. The default is None.
            If None, will assume it is an object attribute. If object attribute
            is also None, will assume there is no unoccupied model to predict
            on.

        Returns
        -------
        The main pandas dataframe with the predictions attached to it.
        """

        # Check model objects
        if (occ_model != self.occ_model) & (occ_model is not None):
            self.occ_model = occ_model
        if (unocc_model != self.unocc_model) & (unocc_model is not None):
            self.unocc_model = unocc_model
        time_interval = self.infer_interval(df)

        # Check if time_interval is monthly
        if time_interval == "Monthly":
            raise ValueError(
                'Inferred time interval is monthly. The TOWT'
                ' algorithm expects hourly or daily data.')

        # Define knot temp vars and tow vars
        used_knot_temps = pd.DataFrame()
        temp_vars = pd.DataFrame()
        if self.model_name == "TOWT":
            temp_vars, used_knot_temps = self.define_temp_vars(
                df, self.knot_temps)
        tow_vars = self.define_tow_vars(df, time_interval)

        main = pd.concat([df, temp_vars, tow_vars], axis=1)
        pred = main.dropna().copy()
        if self.model_name == "TOWT":
            pred.drop(columns=['time', 'temp'], inplace=True)
        else:
            pred.drop(columns=['time'], inplace=True)

        # Predict
        occ_x_pred = pred.loc[pred['occ'] == 1, pred.columns != 'load']
        occ_x_pred.drop(columns='occ', inplace=True)
        occ_x_pred['predict'] = occ_model.predict(occ_x_pred)
        if pred['occ'].nunique() > 1:
            unocc_x_pred = pred.loc[pred['occ'] == 0, pred.columns != 'load']
            unocc_x_pred.drop(columns='occ', inplace=True)
            unocc_x_pred['predict'] = unocc_model.predict(unocc_x_pred)

        pred = pd.concat([occ_x_pred, unocc_x_pred], axis=0)
        out = pd.concat([main, pred['predict']], axis=1)
        return(out)

    def temp0(self, temp, knot_temp):
        """
        Defining first knot temp values in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_temp : float
            The lowest knot temp.
        Returns
        -------
        float
            The first knot temperature variable value for TOWT model.
        """

        if temp > knot_temp:
            return(knot_temp)
        else:
            return(temp)

    def tempi(self, temp, knot_tempi, knot_tempj):
        """
        Defining the middle knot temp values in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_tempi : float
            A knot temperature that is not the lowest or greatest.
        knot_tempj : float
            A knot temperature that is one index lower than i
        Returns
        -------
        float
            A middle knot temperature variable value in the TOWT model.
        """

        if temp > knot_tempi:
            return(knot_tempi - knot_tempj)
        else:
            if temp > knot_tempj:
                return(temp - knot_tempj)
            else:
                return(0)

    def tempn(self, temp, knot_tempn):
        """
        Defining the last knot temp value in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_tempn : float
            The highest knot temperature.
        Returns
        -------
        float
            The last knot temperature variable value.
        """
        if temp > knot_tempn:
            return(temp - knot_tempn)
        else:
            return(0)

    def define_temp_vars(self, df, knot_temps):
        """
        Define all knot temperature variable values given a dataframe with
        temperature and specific knot temperatures.
        Parameters
        ----------
        df : pandas dataframe
            The main pandas dataframe that will be used for analysis with a
            numeric temperature column.
        knot_temps : list
            List of specific knot temperatures.
        Returns
        -------
        towt_vars: Pandas DataFrame
            Dataframe consisting of the TOWT variables.
        knot_temps : TYPE
            Used knot temperatues to determine TOWT variables.
        """
        # Define min and max temperatures in dataset
        min_temp = df['temp'].min()
        max_temp = df['temp'].max()

        # Drop outside knot temperature bounds if redundant
        knot_temps = [x for x in knot_temps if x > min_temp]
        knot_temps = [x for x in knot_temps if x < max_temp]

        # Sort knot temperatures from least to greatest
        knot_temps.sort()

        # Create the temperature variables according to LBNL algo (Mathieu)
        temp_var_dict = {}
        for i in range(len(knot_temps)):
            idx = 'temp'+str(i)
            if i == 0:
                temp_var_dict[idx] = df['temp'].apply(
                    self.temp0, args=(knot_temps[i],)).values
            elif i == len(knot_temps)-1:
                temp_var_dict[idx] = df['temp'].apply(
                    self.tempi, args=(knot_temps[i], knot_temps[i-1])).values
                temp_var_dict['temp'+str(i+1)] = df['temp'].apply(self.tempn,
                                                                  args=(knot_temps[i],)).values
            else:
                temp_var_dict[idx] = df['temp'].apply(
                    self.tempi, args=(knot_temps[i], knot_temps[i-1])).values

        return pd.DataFrame(temp_var_dict), knot_temps

    @staticmethod
    def define_tow_vars(df, time_interval):
        """
        The function creates time of week indicator variables. 168 hours of
        week or 7 days of week.
        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe consisting of at a minimum a timestamp column labelled
            "time".
        time_interval : str
            DESCRIPTION.
        Returns
        -------
        Pandas DataFrame
            Dataframe containing indicator variables for time of week.
        """
        if time_interval.upper() == 'DAILY':
            dow = df['time'].dt.dayofweek
            tow_vars = pd.get_dummies(dow, prefix="tow")
            return(tow_vars)

        elif time_interval.upper() == 'HOURLY':
            dow = df['time'].dt.dayofweek
            hour = df['time'].dt.hour
            tow = dow*24 + hour
            tow_vars = pd.get_dummies(tow, prefix="tow")
            return(tow_vars)

        else:
            raise ValueError(
                "Time interval supplied expected 'daily' or 'hourly'. "
                "Neither of those were given.")
