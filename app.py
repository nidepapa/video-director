import os
import openai
from metaphor_python import Metaphor
from datetime import datetime, timedelta
import sys

os.environ["OPENAI_API_KEY"] = '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'
os.environ["METAPHOR_API_KEY"] = '3ba9f09f-34e0-493e-a6e2-835304c79916'


class VideoDirector:
    def __init__(self):
        self.metaphor = Metaphor(os.getenv("METAPHOR_API_KEY"))
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def getMetaphorSearch(self, city):
        USER_QUESTION = "What's the popular travelling blog only about {}?".format(city)
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

    def vlogScriptGenerator(self, search_result):
        # choose the very first result as demo
        first_content = search_result.contents[0]
        SYSTEM_MESSAGE = "You are a helpful assistant that generates vlog script with multiple scenes based on blog " \
                         "content."
        ASSISTANT_MESSAGE = "[SCENE 1: Mount Rainier's Grandeur] Narrator (Voiceover): (Proudly) 'Ascending to 14," \
                            "410 feet above sea level, Mount Rainier stands as an icon in the Washington landscape.' " \
                            "[Visuals: Breathtaking aerial views of Mount Rainier] Narrator (Voiceover): 'An active " \
                            "volcano, Mount Rainier is the most glaciated peak in the contiguous U.S.A., " \
                            "spawning five major rivers.' [Visuals: Time-lapse shots of glaciers and rivers] Narrator " \
                            "(Voiceover): 'Subalpine wildflower meadows ring the icy volcano while ancient forest " \
                            "cloaks Mount Rainier’s lower slopes.' [Visuals: Vibrant wildflowers and lush forest] " \
                            "Narrator (Voiceover): 'Wildlife abounds in the park’s ecosystems. A lifetime of " \
                            "discovery awaits.' [Visuals: Wildlife, including deer, bears, and birds] [SCENE 2: " \
                            "Exploring the Park Narrator (Voiceover): 'Now, let's explore the opportunities that " \
                            "await you at Mount Rainier National Park. [Visual transition: A map of the park with " \
                            "various icons highlighting key locations] [SCENE 3: Road Status] Narrator (Voiceover): " \
                            "'First, let's check out the road status.' [Visuals: A map showing road conditions] " \
                            "Narrator (Voiceover): 'Find out current road conditions, including access to Paradise " \
                            "during the winter season.' [Visuals: Snowy roads nnnnnnn and tire chains]"

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


if __name__ == "__main__":
    director = VideoDirector()
    city = sys.argv[1]
    query_content = director.getMetaphorSearch(city)
    demo_script = director.vlogScriptGenerator(query_content)
    print(demo_script)
