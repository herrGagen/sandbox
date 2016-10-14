import math
from sklearn.linear_model import LinearRegression


class DA:

    def __init__(self, first_month, counts):
        self.first_month = first_month
        self.monthly_count_by_agent = counts
        self.linear_model_cache = {}

    def _month(self, running_month):
        return 1 + ((running_month+self.first_month-1) % 12)

    def _quarter(self, running_month):
        return math.ceil(self._month(running_month)/3)

    def _linear_trend(self, running_month, agent):
        """
        Calculate linear trend per supplier since beginning
        of data aquisition

        :param running_month:
         Month since dawn of forecasting time.
         :return
         Trendline since dawn of forecasting.
        """
        key = (running_month, agent)
        if key in self.linear_model_cache:
            lm = self.linear_model_cache[key]
        else:
            lm = LinearRegression()
            counts = self.monthly_count_by_agent[agent]
            if len(counts) > running_month:
                counts = counts[:running_month]
            months = list(range(0, len(counts)))
            lm.fit([[i] for i in months], [[j] for j in counts])
            self.linear_model_cache[key] = lm
        return lm

    def _forecast(self, running_month, agent):
        lm = self._linear_trend(running_month, agent)
        retval = lm.predict(running_month)[0]
        if len(retval) == 1:
            return retval[0]
        return retval

    def _orders(self, running_months, agent):
        count = self.monthly_count_by_agent[agent]
        if isinstance(running_months,int):
            return count[running_months]
        else:
            return [count[i] for i in running_months]

    def _orders_in_quarter(self, quarter, agent):
        ct = self.monthly_count_by_agent[agent]
        months = list(range(0,len(ct)))
        counts = [ct[i] for i in months if self._quarter(i) == quarter]
        return counts

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from DAForecast import DA

    orders = {"AA": [1, 4, 2], "BB": [9, 5, 1]}
    da = DA(10, orders)

    a_future = da._linear_trend(6, "AA")
    b_future = da._linear_trend(6, "BB")

    print(da._forecast(2,"AA") - da._orders(2,"AA"))
    print(da._forecast(2,"BB") - da._orders(2,"BB"))

    plt.plot(orders["AA"])
    plt.plot(orders["BB"])

    for q in [1,2,3,4]:
        print(da._orders_in_quarter(q,"AA"))


