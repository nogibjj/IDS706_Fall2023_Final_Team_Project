from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    # wait_time = between(1, 2)
    wait_time = lambda self: 0

    @task
    def task1(self):
        self.client.get("/")