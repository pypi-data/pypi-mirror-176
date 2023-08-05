# requires pip install 'requests' and 'bs4'
import requests
from bs4 import BeautifulSoup


def validate_url(subject):
    """
    Compose url and make sure a status code of 200 is returned.
    """
    url = 'https://www.vox.com/' + subject
    response = requests.get(url)
    return response


def get_list(webpage):
    """
    Returns a list of headlines.
    """
    soup = BeautifulSoup(webpage.text, 'html.parser')
    headlines = soup.find('body').find_all(
        'h2', {"class": "c-entry-box--compact__title"})
    today = []
    for x in list(dict.fromkeys(headlines)):
        # exclude single words and questions
        if len(x.text.split()) > 1 and x.text[-1] != '?':
            today.append(x.text)
    return today


def get_headlines(subject, titular):
    """
    Returns a list of headlines from the BBC News website.
    """
    content = validate_url(subject)

    if content.status_code == 200:
        hd = get_list(content)
        print("\nTODAY'S HEADLINES FROM VOX NEWS ON " + titular + ":\n")
        for (i, x) in enumerate(hd):
            print(f"{i+1}. {x}")

        print("\nRead more at: " + content.url + "\n")
        return hd

    else:
        print("Sorry, we had some trouble retrieving the headlines from Vox. Please try again later.")
        return False


if __name__ == "__main__":

    choose = True

    while choose:
        print("Choose from the following subjects... ")
        print("1. Culture")
        print("2. Politics")
        print("3. Science")
        print("4. World")
        print("5. Technology")
        print("6. Environment")
        print("7. Business")
        print("8. <Return to main menu>")

        selection = input(
            "Enter the number of the subject you want to explore: ")
        if selection not in ['1', '2', '3', '4', '5', '6', '7', '8']:
            print("Invalid selection. Please try again.")
            continue
        else:
            selection = int(selection)
            choose = False

    if selection != 8:
        if selection == 1:
            subject = "culture"
            titular = "CULTURE"
        elif selection == 2:
            subject = "policy-and-politics"
            titular = "POLITICS AND POLICY"
        elif selection == 3:
            subject = "science-and-health"
            titular = "SCIENCE AND HEALTH"
        elif selection == 4:
            subject = "world"
            titular = "WORLD"
        elif selection == 5:
            subject = "technology"
            titular = "TECHNOLOGY"
        elif selection == 6:
            subject = "energy-and-environment"
            titular = "ENERGY AND ENVIRONMENT"
        elif selection == 7:
            subject = "business-and-finance"
            titular = "BUSINESS AND FINANCE"

        get_headlines(subject, titular)

    else:
        print("Returning to main menu...")
