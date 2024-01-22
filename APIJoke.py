# Joke API Hacks-Avanthika

class FlaskAPI:
    def __init__(self, name):
        self.name = name

    def tell_joke(self):
        return f"Why did the {self.name} developer go on stage at the comedy club?\nBecause they wanted to deliver the most 'punny' JSON responses, and their sense of humor was as impeccable as their code! 😂🐍"

def main():
    flask_api = FlaskAPI("Flask API")
    joke = flask_api.tell_joke()
    print(joke)

if __name__ == "__main__":
    main()  