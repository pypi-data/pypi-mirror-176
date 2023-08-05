import httpx
import pandas
import io

from aw_client.data_master.base import DataMasterApi


class DataMasterV0(DataMasterApi):
    """ """

    def load_model(self, model_id: int, **options) -> pandas.DataFrame:
        """ """
        with self.get_http_client() as client:
            url = f"data-master/v0/model/data?model_id={model_id}&format=csv"
            r = client.get(url, timeout=None)
            if not r.is_success:
                raise Exception(f"Ошибка загрузки данных модели: {r.text}")

        return pandas.read_csv(io.StringIO(r.content.decode("utf-8")))
