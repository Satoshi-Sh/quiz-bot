from quiz import get_quiz
import random
import os 
from mastodon import Mastodon
from dotenv import load_dotenv
import datetime
load_dotenv()

def main():
    category,level,question,answers,tags,correct = prepare_quiz()
    make_toot(category,level,question,answers,tags,correct)
    

def prepare_quiz():
    data = get_quiz()
    category = data['category'].replace('_',' ').title().replace(' And ',' and ')
    level = data['difficulty'].capitalize()
    question = data['question']['text']
    tags = data['tags']
    tags = [tag.replace("'",'') for tag in tags]
    tags = "#" + ' #'.join(data['tags'])
    correct = data['correctAnswer']
    answers = [correct]
    answers.extend(data['incorrectAnswers'])
    random.shuffle(answers)
    print(f'Category: {category}')
    print(f'Level: {level}')
    print(f'Question: {question}')

    index=1
    for answer in answers:
        print(f"{index} {answer}")
        index+=1;
    print(tags)
    return [category,level,question,answers,tags,correct]

def make_toot(category,level,question,answers,tags,correct):
    time=600
    mastodon = Mastodon(
        access_token=os.environ.get('ACCESS_TOKEN'),
        api_base_url = os.environ.get('URL'))
        
    poll = mastodon.make_poll(
        options= answers,
        expires_in=time,
    )
    mastodon.status_post(
        status=f"""Category:{category}\nLevel:{level}\nQuestion:{question}\n{tags}""",
        poll= poll
    )
    current_time_utc = datetime.datetime.utcnow()
    ten_minutes_later_utc = current_time_utc + datetime.timedelta(seconds=time)

    mastodon.status_post(
        status=f"Answer: {correct}",
        scheduled_at=ten_minutes_later_utc
    )

if __name__ == "__main__":
    main()








