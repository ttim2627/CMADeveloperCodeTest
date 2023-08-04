import requests
import datetime
import pymongo
import sys


# Since our point of entry to the API is the exhibtions, let's find the CMA's very first exhibiton
def getExhibitions():
    # To get a set of results containing the 1916 Inaugural, we could either use the opening_date parameter to filter
    # before 1917, or as I do here, search on titles containing the string 'inaugural'
    api_url_exhibitions = "https://openaccess-api.clevelandart.org/api/exhibitions/?title=inaugural"

    response = requests.get(api_url_exhibitions)

    # Make sure we connect properly
    if response.status_code != 200:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        return []

    exhibitions = response.json().get("data", [])
    print("\n")
    print(f"Found {len(exhibitions)} with 'Inaugural' in their title.")
    return exhibitions


# We get multiple results for inaugural - let's find the earliest opening_date to be sure we have the right one
def getCMAInaugural():
    earliest_date = None
    earliest_exhibition = None

    exhibitions = getExhibitions()
    # Loop through our subset of exhibitions comparing their opening_dates and setting the earliest to our return variable
    if len(exhibitions) > 1:
        for exhibition in exhibitions:
            opening_date = datetime.datetime.fromisoformat(exhibition["opening_date"])
            if earliest_date is None or opening_date < earliest_date:
                earliest_date = opening_date
                earliest_exhibition = exhibition
        print("\n")
        print(f"1916 Exhibition ID is: {earliest_exhibition['id']}.")
        return earliest_exhibition


# We have our exhibition (id: 317001), let's find the artwork which made a big hit and was featured in the most subsequent exhibitions
# First we'll grab all of the artwork Ids
def getArtworkIds():
    artworkIds = []

    inaugExhibition = getCMAInaugural()
    for artwork in inaugExhibition["artworks"]:
        artworkIds.append(artwork["id"])
    print("\n") 
    print(f"The 1916 Exhibition featured {len(artworkIds)} artworks.")
    return artworkIds


# We'll head back to Open Access, but this time let's look at the Artworks Endpoint
# Side note - it wasn't immediately obvious to me what the classification of current vs legacy exhibition was, so for these purposes I used 'current'
def mostExhibitedfromInaugural():
    api_url_artwork = "https://openaccess-api.clevelandart.org/api/artworks/"
    maxExhNumber = None
    mostExhibited = None

    #Loop through each artwork and select the one with the most exhibitions
    inaugArtworkIds = getArtworkIds()
    print("\n")
    print("Looping through all 286 artworks...")
    for id in inaugArtworkIds:
        response = requests.get(api_url_artwork + str(id))
        artworkInfo = response.json().get("data", [])
        if (
            maxExhNumber is None
            or len(artworkInfo["exhibitions"]["current"]) > maxExhNumber
        ):
            maxExhNumber = len(artworkInfo["exhibitions"]["current"])
            mostExhibited = artworkInfo["title"]
    print("\n")
    print(f"The portrait of {mostExhibited} was exhibited {maxExhNumber} times.")

    #Function Call placed here to maintain narrative chronology
    mongoRecords = list(map(prepForMongo, findRecentUpdates()))
    sendToMongo(mongoRecords)
    
    return mostExhibited, maxExhNumber


# That last query took a while, let's change gears. 
# That's funny - even though he was one of the original exhibition objects, this record was updated less than a month ago.
# Let's find some other things which have been updated just after him. We'll use the updated_since parameter to align with Mr. Hurd, and grab 5 objects.
def findRecentUpdates():
    api_url_recentlyUpdatedArtworks = "https://openaccess-api.clevelandart.org/api/artworks/?updated_since=2023-07-19&limit=6"

    recentlyUpdated = []

    response = requests.get(api_url_recentlyUpdatedArtworks)

    artworkInfo = response.json()
    recentlyUpdated = artworkInfo.get("data", [])
    print("\n")
    print(f"We have gathered {len(recentlyUpdated)} records to look at.")
    return recentlyUpdated


# Oh, there's a connection, it looks like someone (or a team) in the American Painting and Sculpture Department is hard at work.
# Let's put these 5 artworks into Mongo and leave them to their work
def prepForMongo(artworks):
    return {
        "athena id": artworks["athena_id"],
        "accession number": artworks["accession_number"],
        "tombstone": artworks["tombstone"],
        "image": artworks["images"]["web"]["url"],
        "department": artworks["department"],
        "PyExId": "recentlyUpdated_" + (str(artworks["title"]).replace(" ", "")),
    }


# Connect to Atlas - I have included my password in the Client because this account was created just for this exercise so there is no sensitive data.
def sendToMongo(mongoRecords):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://timtrombley2115:CMAC0deT3st@cluster4cma.yvr5bwe.mongodb.net/?retryWrites=true&w=majority"
        )
    except pymongo.errors.ConfigurationError:
        print("Connection Error")
        sys.exit(1)

    db = client.CMACodeTest
    my_collection = db["artworks"]

    # Empty the collection before inserting new
    try:
        my_collection.drop()

    except pymongo.errors.OperationFailure:
        print("Authentication Error")
        sys.exit(1)

    # Insert our prepared Records
    try:
        result = my_collection.insert_many(mongoRecords)

    except pymongo.errors.OperationFailure:
        print("Permissions Error")
        sys.exit(1)
    else:
        # Confirm our success
        print("\n")
        print(f"We have inserted {len(result.inserted_ids)} documents:")
        print("\n")
        print(result.inserted_ids)


if __name__ == "__main__":
    CMACodeTest = mostExhibitedfromInaugural()
