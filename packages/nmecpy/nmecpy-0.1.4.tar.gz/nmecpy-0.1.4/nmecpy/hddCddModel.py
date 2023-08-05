from Model import Model
import pandas as pd
from sklearn.linear_model import LinearRegression


class HDDCDDModel(Model):

    def __init__(self, df=None):
        """
        The class assumes a dataframe with HD and CD values that are already
        calculated.

        Parameters
        ----------
        df : Pandas DataFrame, optional
            If training a model, a dataframe must be provided. If using only
            for predictions, a dataframe is not needed when initialized.

        Returns
        -------
        None.

        """
        super().__init__(df=df)

    def train(self, model="HD-CD"):
        """
        Model training method for heating degree and cooling degree models.

        Parameters
        ----------
        model : str, optional
            String value equaling HD-CD for a heating and cooling degree model.
            HD for just a heating degree model. CD for just a cooling degree
            model. The default is "HD-CD".

        Returns
        -------
        None.

        """

        time_interval = self.infer_interval(self.df)

        # Assemble regression datasets
        if ('occ' not in self.df.columns):
            self.df = self.find_occ_unocc(time_interval=time_interval)

        main = self.df
        train = self.df.dropna().copy()
        train.drop(columns=['time', 'temp'], inplace=True)

        # Create models and predict
        # Occupied model
        occ_x_train = train.loc[train['occ'] == 1, train.columns != 'load']
        occ_x_train.drop(columns='occ', inplace=True)
        occ_y_train = train.loc[train['occ'] == 1, 'load']
        occ_model = LinearRegression().fit(occ_x_train, occ_y_train)
        self.occ_model = occ_model

        # Unoccupied model
        if train['occ'].nunique() > 1:
            unocc_x_train = train.loc[train['occ']
                                      == 0, train.columns != 'load']
            unocc_x_train.drop(columns='occ', inplace=True)
            unocc_y_train = train.loc[train['occ'] == 0, 'load']
            unocc_model = LinearRegression().fit(unocc_x_train, unocc_y_train)
            self.unocc_model = unocc_model

        return(main)

    def predict(self, df, occ_model=None, unocc_model=None):
        """
        Predict method for heating degree and cooling degree methods.

        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe with heating and/or cooling degree variables.
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
        Predictions attached to main dataframe.

        """

        # Check model objects
        if (occ_model != self.occ_model) & (occ_model is not None):
            self.occ_model = occ_model
        if (unocc_model != self.unocc_model) & (unocc_model is not None):
            self.unocc_model = unocc_model

        main = df
        pred = main.dropna().copy()
        pred.drop(columns=['time', 'temp'], inplace=True)

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
