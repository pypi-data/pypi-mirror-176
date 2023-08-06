import pandas as pd
from ValiotWorker.Logging import LogLevel

from factoryos_lib.base.outputs import UpdateDatumOutput
from factoryos_lib.filters import MovingAverage


class ExponentialMovingAverage(MovingAverage):

    def apply_filter(self):
        values = pd.Series(data=self.X)
        self.Y = values.ewm(com=0.4).mean().to_numpy()
        print(self.Y)

    def post_data(self):
        vo = UpdateDatumOutput()
        self.log_callback(LogLevel.DEBUG, "Updating {0} and {1} datums for filter".format(len(self.Y), len(self.Y_id)))
        vo.save_output(self.Y_name, self.Y, self.Y_id, self)
        self.log_callback(LogLevel.DEBUG, f"Completed the update of  {len(self.Y)} datums for filter {self.Y_name}")
