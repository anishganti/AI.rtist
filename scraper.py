import requests
from annotation import annotate_image


def scrape_data(search_term):
    # print(search_term)

    image_results = search_images(search_term)

    process_images(image_results, search_term)


def search_images(search_term):
    # code mostly pulled from Bing documentation

    # create and initialize the application
    subscription_key = '72c3cc8969dc4e6f9a1a6bbd4ed4b044'
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"

    # add your subscription key to the Ocp-Apim-Subscription-Key header
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # create and send a search request
    params = {"q": search_term, "license": "public", "imageType": "photo"}

    # send search query to Bing Image Search API
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    img_urls = [img["contentUrl"] for img in search_results["value"]]

    return img_urls


def process_images(img_urls, search_term):
    counter = 1

    # view results of search request and annotate
    for img_url in img_urls:
        if img_url is not None:
            img_data = requests.get(img_url)
            success = annotate_image(img_data, search_term + str(counter))

            # if user has pressed 'esc' key while annotating image, they quit the program
            if success is False:
                break

            counter += 1
