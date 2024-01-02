import wikipedia


def get_random_article():
    while True:
        # Get a random article title
        article_title = wikipedia.random()

        # Get the summary of the article
        try:
            article_summary = wikipedia.summary(article_title)
            return article_title, article_summary
        except wikipedia.exceptions.DisambiguationError:
            continue


def main():
    while True:
        # Get a random article
        article_title, article_summary = get_random_article()

        print("Random Article:")
        print("Title:", article_title)
        print("Summary:", article_summary)

        # Ask the user if they want to read the article
        answer = input("Do you want to read this article? (yes/no): ").lower()

        if answer == "yes":
            # Open the full Wikipedia page in a browser
            wikipedia_url = wikipedia.page(article_title).url
            print("Opening the Wikipedia page in your browser...")
            print("URL:", wikipedia_url)
            another = input('Would you like another article? yes or no ')
            if another == 'yes':
                pass
            else:
                break


if __name__ == "__main__":
    main()
