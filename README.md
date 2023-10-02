# Vlog-Director

An automate vlog/video script generator empowered by Metaphor and OpenAI.

## Usage

Download the package

```bash
python3 app.py
```

## API - getMetaphorSearch

Will interpret user's natural language search to a metaphor query
and return blog content of recent (3 months) related to input tourism attractions

```python

    def getMetaphorSearch(self):
        USER_QUESTION = "What's the popular travelling blog only about Los Angeles?"
        SYSTEM_MESSAGE = "You are a helpful assistant that generates search queiries based on user questions. Only generate one search query."

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": USER_QUESTION},
            ],
        )

        date_90_days_ago = datetime.now() - timedelta(days=90)
        # Format the date as "YYYY-MM-DD"
        formatted_date = date_90_days_ago.strftime("%Y-%m-%d")

        query = completion.choices[0].message.content
        search_response = self.metaphor.search(
            query, use_autoprompt=True, start_published_date=formatted_date
        )

        return search_response.get_contents()
```

## API - vlogScriptGenerator

Will generate a vlog script based on the very first blog content(for demo purpose)
and return in a formatted string

```python
    def vlogScriptGenerator(self, search_result):
        # choose the very first result as demo
        first_content = search_result.contents[0]
        SYSTEM_MESSAGE = "You are a helpful assistant that generates vlog script with multiple scenes based on blog " \
                         "content."
        ASSISTANT_MESSAGE = "some context"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "name": "example_user", "content": "help me to generate a random script with some "
                                                                 "scenes"},
                {"role": "system", "name": "example_assistant",
                 "content": ASSISTANT_MESSAGE},
                {"role": "user", "content": first_content.extract},
            ],
        )

        result_script = completion.choices[0].message.content
        return "Vlog script for {0}: {1}".format(first_content.title, result_script)
```

## Reference

metaphor API: 

https://github.com/metaphorsystems/metaphor-python 

OpenAI API: 

https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models

# Future work
1. more arguments can be added to make this API more customized, so people can choose any locations they prefer
2. database can be added to store user preference history for future analysis, like who can be the potential content maker for video platform like Youtube