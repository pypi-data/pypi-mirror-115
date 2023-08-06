# import
import pandas as pd
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict, KFold , cross_validate
from sklearn.metrics import r2_score , make_scorer


from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.stats import f

def pPCA(data, Y=None, scale=False, n_components=10):
    """
         retrun the projection of the data on the specified PCA components with the score plot and projection plot on the first 2 principal componenets
         if y is not None each class will be colored diffrently

         :param: data: dataframe containg the independent variables
         :param Y: the dependent variable
         :param scale if set to true independent variables will be automaticly standazized
         :return: scree plot (left fig) and xscore plot (right fig)

    """
    # Data initialisation and checks ----------------------------------------------

    assert isinstance(Y, list) or Y is None or type(Y).__module__ == np.__name__, "target data msut be a factor "
    assert isinstance(scale, bool), 'scale must be boolean instance'
    if Y is None:
        if scale == True:
            # Standardize the data to have a mean of ~0 and a variance of 1
            X_std = StandardScaler().fit_transform(data)
        else:
            X_std = data
        # Create a PCA instance: pca
        pca1 = PCA(n_components=n_components)
        principalComponents = pca1.fit_transform(X_std)
        print('explanation variance by the selected components ', pca1.explained_variance_ratio_[:n_components].sum())
        PCA_components = pd.DataFrame(principalComponents)

        features = range(pca1.n_components_)

        PCA_components_i = pd.DataFrame(columns=PCA_components.columns)
        PCA_components_o = pd.DataFrame(columns=PCA_components.columns)
        from pyod.models import pca
        clf = pca.PCA(n_components=n_components)
        clf.fit(data)
        outliers = clf.predict(data)
        for k, i in enumerate(outliers):
            if i == 0:
                PCA_components_i.loc[k] = PCA_components.iloc[k]
            elif i == 1:
                PCA_components_o.loc[k] = PCA_components.iloc[k]

        fig, ax = plt.subplots(ncols=2, figsize=(15, 5))

        ax[0].bar(features, pca1.explained_variance_ratio_, color='black')
        ax[0].set(xlabel='variance %', ylabel='PCA features', xticks=features)

        ax[1].scatter(PCA_components_i[0], PCA_components_i[1], color='b')
        ax[1].scatter(PCA_components_o[0], PCA_components_o[1], color='r')
        for i in range(PCA_components.shape[0]):
            ax[1].text(x=PCA_components.iloc[i, 0] + 0.3, y=PCA_components.iloc[i, 1] + 0.3, s=i + 1)
        ax[1].set(xlabel='PCA 1', ylabel='PCA 2' )


        plt.show()
        return (PCA_components)
    else:
        if scale == True:
            # Standardize the data to have a mean of ~0 and a variance of 1
            X_std = StandardScaler().fit_transform(data)
        else:
            X_std = data
        # Create a PCA instance: pca
        pca = PCA(n_components=n_components)
        principalComponents = pca.fit_transform(X_std)
        print('explanation variance by the selected components ', pca.explained_variance_ratio_[:n_components].sum())
        principalDf = pd.DataFrame(data=principalComponents[:, :2]
                                   , columns=['principal component 1', 'principal component 2'])

        features = range(pca.n_components_)

        fig, ax = plt.subplots(ncols=2, figsize=(15, 5))

        ax[0].bar(features, pca.explained_variance_ratio_, color='black')
        ax[0].set(xlabel='variance %', ylabel='PCA features', xticks=features)

        targets = np.unique(Y)
        colors = ['r', 'g']
        tar = pd.DataFrame(Y)
        finalDf = pd.concat([principalDf, tar], axis=1)

        for target, color in zip(targets, colors):
            indicesToKeep = finalDf[0] == target

            ax[1].scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                          , finalDf.loc[indicesToKeep, 'principal component 2']
                          , c=color
                          )
        for i in range(principalDf.shape[0]):
            ax[1].text(x=principalDf.loc[i, 'principal component 1'] + 0.3,
                       y=principalDf.loc[i, 'principal component 2'] + 0.3, s=i + 1)
        ax[1].set(xlabel='PCA 1', ylabel='PCA 2')

        plt.show()
        return (principalComponents)


def PLS_DA(data, Y, scale=False, n_components=10):
    """
      -Function to perform standard Partial Least Squares regression to classify samples.


      :param: data: dataframe containg the independent variables
      :param Y: the dependent variable
      :param scale: if set to true independent variables will be automaticly standazized
      :return: scree plot (left fig) and xscore plot (right fig)

    """
    # Data initialisation and checks ----------------------------------------------

    assert isinstance(Y, list) or Y is None or type(Y).__module__ == np.__name__, "target data msut be a factor "
    assert isinstance(scale, bool), 'scale must be boolean instance'
    #scale the data if scaler is profied
    if scale == True:
        # Standardize the data to have a mean of ~0 and a variance of 1
        X_std = StandardScaler().fit_transform(data)
    else:
        X_std = data
    #get R2 score
    scoring = make_scorer(r2_score)
    #splt the data into 7 folds to perform cross validation
    kfold = KFold(n_splits=7)
    # save Q2 score of cv results
    Q2_scores = []
    R2_scores = []
    for i in range(1, n_components + 1):
        pls_binary = PLSRegression(n_components=i)
        scores = cross_validate(pls_binary, X=data, y=Y, scoring=scoring, cv=7, n_jobs=-1, return_train_score=True, )
        R2_scores.append(np.mean(scores['train_score']))
        Q2_scores.append(np.mean(scores['test_score']))

    #get pls componant array
    features = np.arange(len(Q2_scores))
    # call the sklearn pls regressor
    pls_binary = PLSRegression(n_components=2)
    #set the target variable
    y_binary = Y
    #get the laten variable of the pls model
    X_pls = pls_binary.fit_transform(data, y_binary)[0]

    labplot = [0, 1]
    # get list of classes
    unique = list(set(y_binary))
    #get list of distinct colors // for now this only works for 2 classes
    colors = ['r', 'g']

    # print the R2 score (goodness of the fit
    print('R2 score :', pls_binary.score(data, Y))

    fig, ax = plt.subplots(ncols=2, figsize=(15, 5))

    #
    for i, u in enumerate(unique):
        col = np.expand_dims(np.array(colors[i]), axis=0)
        xi = [X_pls[j, 0] for j in range(len(X_pls[:, 0])) if y_binary[j] == u]
        yi = [X_pls[j, 1] for j in range(len(X_pls[:, 1])) if y_binary[j] == u]
        # plot the scatter plot of the model result where each
        ax[0].scatter(xi, yi, c=col, s=100, edgecolors='k', label=str(u))
    for i in range(X_pls.shape[0]):
        ax[0].text(X_pls[i, 0] + 0.3, X_pls[i, 1] + 0.3, s=i + 1)

    ax[0].set(xlabel='Latent Variable 1', ylabel='Latent Variable 2', title='PLS cross-decomposition')
    ax[0].legend()
    #plot the paired bar bolt where the first bar containe R2 value and the second one Q2
    ax[1].bar(features - 0.2, R2_scores, 0.4, label='R2')
    ax[1].bar(features + 0.2, Q2_scores, 0.4, label='Q2')
    ax[1].legend()

    plt.show()
    return X_pls

#####################################################################################





class pyPCA(BaseEstimator):
    """
         PyPAC object - Wrapper for sklearn.decomposition PCA algorithms for Omics data analysis
        :param n_comps: Number of components for PCA
        :param scaler: data scaling object

    """

    def __init__(self, n_comps=2, scaler=StandardScaler()):

        # Perform the check with is instance but avoid abstract base class runs. PCA needs number of comps anyway!
        pca = PCA(n_components=n_comps)
        assert isinstance(scaler,
                          TransformerMixin) or scaler is None, "sclaler must be an sklearn transformer-like or None"

        # initialize variabels
        self.pca_algorithm = pca
        self.n_comps = n_comps
        self.scaler = scaler
        self.loadings = None
        self.isfitted = False
        self.scores = None
        self.m_params = None

    def transform(self, x):
        """
        get the projection of the data metrix x on the pricipal componants of PCA
        :param x: data metrix to be fit (rows : samples , columns : variables )

        :return: PCA projections (x scores) (rows : samples , columns : principal componants)

        :raise ValueError: If there are problems with the input or during model fitting.
        """
        try:
            if self.scaler is not None:
                xscaled = self.scaler.transform(x)
                return self.pca_algorithm.transform(xscaled)
            else:
                return self.pca_algorithm.transform(x)
        except ValueError as ver:
            raise ver

    def _residual_ssx(self, x):
        """
        :param x: data metrix to be fit (rows : samples , columns : variables )
        :return: RSS resudual sum of squares
        """
        pred_scores = self.transform(x)

        x_reconstructed = self.scaler.transform(self.inverse_transform(pred_scores))
        xscaled = self.scaler.transform(x)
        residuals = np.sum((xscaled - x_reconstructed) ** 2, axis=1)
        return residuals

    def inverse_transform(self, scores):
        """
        inverse transformation of x score data to the original data before projection
        :param scores: The projections ( x scores)  (rows : samples , columns : principal componants)

        :return: Data matrix in the original format (rows : samples , columns : variables )

        """
        # Scaling check for consistency
        if self.scaler is not None:
            xinv_prescaled = self.pca_algorithm.inverse_transform(scores)
            xinv = self.scaler.inverse_transform(xinv_prescaled)
            return xinv
        else:
            return self.pca_algorithm.inverse_transform(scores)

    def fit_transform(self, x, **fit_params):
        """
        Fit a model and return the x scores (rows : samples , columns : principal componants)
        :param x:  data metrix to be fit (rows : samples , columns : variables )
        :return: PCA projections ( x scores) after transforming x
        :raise ValueError: If there are problems with the input or during model fitting.
        """

        try:
            self.fit(x, )
            return self.transform(x)
        except ValueError as ver:
            raise ver

    def fit(self, x):
        """
              Perform model fitting on the provided x data matrix and calculate basic goodness-of-fit metrics.
              :param x: data metrix to be fit (rows : samples , columns : variables )
              :raise ValueError: If any problem occurs during fitting.
        """
        try:
            # check if we will use scaling or not for PCA
            if self.scaler is not None:
                xscaled = self.scaler.fit_transform(x)
                self.pca_algorithm.fit(xscaled)
                self.scores = self.pca_algorithm.transform(xscaled)
                ss = np.sum((xscaled - np.mean(xscaled, 0)) ** 2)
                predicted = self.pca_algorithm.inverse_transform(self.scores)
                rss = np.sum((xscaled - predicted) ** 2)

            else:
                self.pca_algorithm.fit(x, )
                self.scores = self.pca_algorithm.transform(x)
                ss = np.sum((x - np.mean(x, 0)) ** 2)
                predicted = self.pca_algorithm.inverse_transform(self.scores)
                rss = np.sum((x - predicted) ** 2)
            # set model parmetres
            self.m_params = {'R2X': 1 - (rss / ss), 'VarExp': self.pca_algorithm.explained_variance_,
                             'VarExpRatio': self.pca_algorithm.explained_variance_ratio_}

            # For "Normalised" DmodX calculation
            resid_ssx = self._residual_ssx(x)
            s0 = np.sqrt(resid_ssx.sum() / ((self.scores.shape[0] - self.n_comps - 1) * (x.shape[1] - self.n_comps)))
            self.m_params['S0'] = s0

            # set loadings
            self.loadings = self.pca_algorithm.components_
            # set fitted to true
            self.isfitted = True


        except ValueError as ver:
            raise ver

    def hotelling_T2(self, comps=None, alpha=0.05):
        """
        Obtain the parameters for the Hotelling T2 ellipse at the desired significance level.
        :param list comps:
        :param float alpha: Significance level
        :return: The Hotelling T2 ellipsoid radii at vertex
        :raise AtributeError: If the model is not fitted
        :raise ValueError: If the components requested are higher than the number of components in the model
        :raise TypeError: If comps is not None or list/numpy 1d array and alpha a float
        """

        try:
            if self.isfitted is False:
                raise AttributeError("Model is not fitted yet ")
            n_samples = self.scores.shape[0]
            if comps is None:
                n_comps = self.n_comps
                ellips = self.scores[:, range(self.n_comps)] ** 2
                ellips = 1 / n_samples * (ellips.sum(0))
            else:
                n_comps = len(comps)
                ellips = self.scores[:, comps] ** 2
                ellips = 1 / n_samples * (ellips.sum(0))

            # F stat
            fs = (n_samples - 1) / n_samples * n_comps * (n_samples ** 2 - 1) / (n_samples * (n_samples - n_comps))
            fs = fs * f.ppf(1 - alpha, n_comps, n_samples - n_comps)

            hoteling_t2 = list()
            for comp in range(n_comps):
                hoteling_t2.append(np.sqrt((fs * ellips[comp])))

            return np.array(hoteling_t2)

        except AttributeError as atrer:
            raise atrer
        except ValueError as valer:
            raise valer
        except TypeError as typer:
            raise typer

    def dmodx(self, x):
        """
        Normalised DmodX measure
        :param x: data metrix to be fit (rows : samples , columns : variables )
        :return: The Normalised DmodX measure for each sample
        """
        resids_ssx = self._residual_ssx(x)
        s = np.sqrt(resids_ssx / (self.loadings.shape[1] - self.n_comps))
        dmodx = np.sqrt((s / self.m_params['S0']) ** 2)
        return dmodx

    def _dmodx_fcrit(self, x, alpha=0.05):
        """
        :param alpha: significance level
        :return dmodx fcrit
        """

        # Degrees of freedom for the PCA model (denominator in F-stat)

        dmodx_fcrit = f.ppf(1 - alpha, x.shape[1] - self.n_comps - 1,
                            (x.shape[0] - self.n_comps - 1) * (x.shape[1] - self.n_comps))

        return dmodx_fcrit

    def outlier(self, x, comps=None, measure='T2', alpha=0.05):
        """
         using F statistic and T2 /Dmodx mesure to determine outliers
        :param x: data metrix to be fit (rows : samples , columns : variables )
        :param comps: Which components to use (for Hotelling T2 only)
        :param measure: T2 or DmodX
        :param alpha: Significance level
        :return: List of ouliers indices
        """
        try:
            if measure == 'T2':
                scores = self.transform(x)
                t2 = self.hotelling_T2(comps=comps)
                outlier_idx = np.where(((scores ** 2) / t2 ** 2).sum(axis=1) > 1)[0]
            elif measure == 'DmodX':
                dmodx = self.dmodx(x)
                dcrit = self._dmodx_fcrit(x, alpha)
                outlier_idx = np.where(dmodx > dcrit)[0]
            else:
                print("Select T2 (Hotelling T2) or DmodX as outlier exclusion criteria")
            return outlier_idx
        except Exception as exp:
            raise exp

    def PCA_score_plot(self, x):
        """ plot the projection of the x scores on the firest 2 components
        :param x : data metrix to be fit (rows : samples , columns : variables )
        :return 2 dimentional scatter plot """

        try:
            if self.isfitted == False:
                raise AttributeError("Model is not fitted yet ")

            plt.scatter(self.scores[:, 0], self.scores[:, 1])

            for i in range(self.scores.shape[0]):
                plt.text(x=self.scores[i, 0] + 0.3, y=self.scores[i, 1] + 0.3, s=i + 1)
            plt.xlabel('PC 1')
            plt.ylabel('PC 2')
            plt.title('PCA score plot')
            plt.show()
        except AttributeError as atter:
            raise atter
        except TypeError as typer:
            raise typer

    def scree_plot(self, x):
        """ plot the explained varianace of each componant in the PCA model
        :param x : data metrix to be fit (rows : samples , columns : variables )
        :return scree plot  """

        try:
            if self.isfitted == False:
                raise AttributeError("Model is not fitted yet ")
            features = ['PC ' + str(x) for x in range(1, self.n_comps + 1)]
            plt.bar(features, self.m_params['VarExpRatio'], color='black')

            plt.ylabel('variance %')
            plt.xlabel('PCA features')
            plt.xticks = features
            plt.title('Scree plot')
            plt.show()
        except AttributeError as atter:
            raise atter
        except TypeError as typer:
            raise typer

    def outlier_plot(self, x, comps=None, measure='T2', alpha=0.05):
        """ detect outlier in x metric based on their variance and plot them with different color
        :param x : data metrix to be fit (rows : samples , columns : variables )
        :param comps: Which components to use (for Hotelling T2 only)
        :param measure: T2 or DmodX
        :param alpha: Significance level

        :return scree plot  """

        try:
            if self.isfitted == False:
                raise AttributeError("Model is not fitted yet ")
            # get ouliers index
            outliers = self.outlier(x=x, comps=comps, measure=measure, alpha=alpha)
            # not outlier index
            not_outliers = [x for x in np.arange(self.scores.shape[0]) if x not in outliers]

            plt.scatter(self.scores[not_outliers, 0], self.scores[not_outliers, 1], color='black', label='not outlier')
            plt.scatter(self.scores[outliers, 0], self.scores[outliers, 1], color='r', label='outlier')
            for i in range(self.scores.shape[0]):
                plt.text(x=self.scores[i, 0] + 0.3, y=self.scores[i, 1] + 0.3, s=i + 1)

            plt.ylabel('PCA 2')
            plt.xlabel('PCA 1')
            plt.legend()
            plt.title('outliers plot')
            plt.show()
        except AttributeError as atter:
            raise atter
        except TypeError as typer:
            raise typer

    def target_plot(self, x, y):
        """ the same as score plot but instead but we add color to each sample based on their classe
        :param x : data metrix to be fit (rows : samples , columns : variables )
        :params y : target variable (list) (each class has unique integer value)

        :return scree plot  """
        assert isinstance(y, (list, np.ndarray)) and len(y) == self.scores.shape[0]
        try:
            if self.isfitted == False:
                raise AttributeError("Model is not fitted yet ")

            targets = np.unique(y)
            colors = ['r', 'g']
            for target, color in zip(targets, colors):
                indicesToKeep = [x for x in np.arange(self.scores.shape[0]) if y[x] == target]

                plt.scatter(self.scores[indicesToKeep, 0]
                            , self.scores[indicesToKeep, 1]
                            , c=color, label='class ' + str(target)
                            )
            for i in range(self.scores.shape[0]):
                plt.text(x=self.scores[i, 0] + 0.3, y=self.scores[i, 1] + 0.3, s=i + 1)

            plt.ylabel('PCA 2')
            plt.xlabel('PCA 1')
            plt.legend()
            plt.title('target plot')
            plt.show()
        except AttributeError as atter:
            raise atter
        except TypeError as typer:
            raise typer







