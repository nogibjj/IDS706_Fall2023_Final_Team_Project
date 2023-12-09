from locust import HttpUser, task


class WebsiteUser(HttpUser):
    wait_time = lambda self: 0

    @task
    def task1(self):
        self.client.get("/")
