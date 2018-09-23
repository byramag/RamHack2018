from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

rule = gen_rule_payload("beyonce", results_per_call=100) # testing with a sandbox account

#enterprise_search_args = load_credentials("~/.twitter_keys.yaml", yaml_key="search_tweets_enterprise", env_overwrite=False)

tweets = collect_results(rule, max_results=100)#,result_stream_args=enterprise_search_args) # change this if you need to

[print(tweet.all_text, end='\n\n') for tweet in tweets[0:10]]