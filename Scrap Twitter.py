from apify_client import ApifyClient
import json

client = ApifyClient("APIKEY")

run_input = {
    "searchQueries": ["drark web"],
    "tweetsDesired": 20,
    "includeUserInfo": True,
    "minReplies": 0,
    "minRetweets": 0,
    "minLikes": 0,
    "fromTheseAccounts": [],
    "toTheseAccounts": [],
    "mentioningTheseAccounts": [],
    "nativeRetweets": False,
    "media": False,
    "images": False,
    "videos": False,
    "news": False,
    "verified": False,
    "nativeVideo": False,
    "replies": False,
    "links": False,
    "safe": False,
    "quote": False,
    "proVideo": False,
    "excludeNativeRetweets": False,
    "excludeMedia": False,
    "excludeImages": False,
    "excludeVideos": False,
    "excludeNews": False,
    "excludeVerified": False,
    "excludeNativeVideo": False,
    "excludeReplies": False,
    "excludeLinks": False,
    "excludeSafe": False,
    "excludeQuote": False,
    "excludeProVideo": False,
    "language": "any",
    "proxyConfig": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
    },
}

# Run the Actor and wait for it to finish
run = client.actor("2s3kSMq7tpuC3bI6M").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
    with open ("data.json", "w") as f:
        json.dump(item, f)
