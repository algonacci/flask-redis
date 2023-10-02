from flask import Flask, jsonify
import redis
from flask_redis import FlaskRedis
import time

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"
redis_store = FlaskRedis(app)

# Dummy data
data = {i: f"item_{i}" for i in range(1000)}


@app.route('/')
def index():
    redis_store.set('key', 'value')
    return redis_store.get('key')


@app.route('/no-cache', methods=['GET'])
def no_cache():
    start_time = time.time()

    # Simulate a slight delay like in a real DB operation
    time.sleep(0.1)

    elapsed_time = time.time() - start_time
    return jsonify({"data": data, "time_taken": elapsed_time})


@app.route('/with-cache', methods=['GET'])
def with_cache():
    start_time = time.time()

    # Try to get data from cache
    cached_data = redis_store.get("cached_data")

    if cached_data:
        elapsed_time = time.time() - start_time
        return jsonify({"data": eval(cached_data.decode()), "time_taken": elapsed_time})

    # If not in cache, fetch data (simulate delay) and set in cache
    time.sleep(0.1)

    redis_store.set("cached_data", str(data))

    elapsed_time = time.time() - start_time
    return jsonify({"data": data, "time_taken": elapsed_time})


if __name__ == '__main__':
    app.run(debug=True)
