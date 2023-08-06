# Various feature engineering functions
from .utils import str_to_func
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


class cpfinder:
    def __init__(self, data: np.ndarray, annotations=[], method: str = "bocpd"):
        """
        Finds the changepoints with various methods.

        Args:
            data (np.ndarray): Time series that changepoint detector will work on
            method (str): A method to find changepoint including; bocpd (as Bayesian Online Chanpoint Detection), rulsif (as online RuLSif)..
        """
        self.methodString = method
        self.data = data
        self.annotations = annotations

    def saveAnimationVideo(self, fname):
        writergif = animation.PillowWriter(fps=1)
        self.animationVideo.save(fname, writer=writergif)

    def fit(
        self,
        animationFlag: bool,
        interval: int = None,
        plotFlag: bool = False,
        model_parameters: dict = {"auto": True},
    ):
        """Fit the given data on model

        Args:
            animationFlag (bool): Whether return results animation or not
            interval (int): Animation variable to use to determine how much sample in each step
            plotFlag (bool): Whether plot animation or not
            model_parameters (dict): Model paramters for given method

            Example for bocpd:

            model_parameters = {
                "hazard" : 1 / 100,
                "mean0" = 0,
                "var0" = 1,
                "varx" = 2,
                "ii" = 3 ,
            }

            * These are default parameters if you want to use this simply no need to define anything for `model_parameters` argument.

            Example for rulsif:


        """

        # Given method to function
        method = str_to_func(self.methodString)

        detector = method(**model_parameters)

        results = detector.fit(
            self.data, interval, animationFlag, plotFlag, annots=self.annotations
        )
        if plotFlag:
            plt.show()
        self.animationVideo = results if animationFlag else None
        self.changepoints = results if not animationFlag else None
