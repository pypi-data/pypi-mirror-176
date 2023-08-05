from .client import Client


class JobClient(Client):
    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)
        self._endpoint = f'{self._endpoint}/jobs'

    def query_job_status(self, job_id):
        assert job_id, 'Job ID is not provided!'
        r = self.get(timeout=self.TIMEOUT_IN_SEC, job_id=job_id)
        return r
