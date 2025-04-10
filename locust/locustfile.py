from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_data(self):
        self.client.get("/api/v1/airquality")
