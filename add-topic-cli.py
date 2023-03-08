# This is to show you that you can write programmes to send HTTP requests
# It doesn't have to be written in Python—you can send requests from, for
# example, a Java programme to your Flask app written in Python, isn't 
# that cool?

# Note that this only works with the version of topiclist without 
# authentication. 

import argparse, requests

def post_topic(topic):
    try:
        response = requests.post(
            url="http://127.0.0.1:15113/add",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            },
            data={
                "topic": f"{topic}",
            },
        )
        print(
            "Response HTTP Status Code: {status_code}".format(
                status_code=response.status_code
            )
        )
    except requests.exceptions.RequestException:
        print("HTTP Request failed")

if __name__ == "__main__":
    # set variables
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required = True)
    args = parser.parse_args()
    
    post_topic(args.topic)