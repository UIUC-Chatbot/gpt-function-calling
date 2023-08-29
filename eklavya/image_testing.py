from function_calling_sloan import *
import requests


# Function to query galaxies within 1 arcminute of a given point
def query_galaxies(ra, dec):
  # Base URL for the SDSS API's SkyServer SQL Search service
  base_url = "http://skyserver.sdss.org/dr16/SkyServerWS/SearchTools/SqlSearch"

  # SQL query to retrieve galaxies within 1 arcminute of the specified point
  query = f"""
        SELECT TOP 100
            p.objid, p.ra, p.dec
        FROM PhotoObjAll p
        WHERE
            p.ra BETWEEN {ra - 1/60.0} AND {ra + 1/60.0}
            AND p.dec BETWEEN {dec - 1/60.0} AND {dec + 1/60.0}
            AND p.type = 3  -- Select only galaxies (type=3)
    """

  # Construct the API request URL
  url = f"{base_url}?cmd={query}"

  # Make the HTTP GET request to the SDSS API
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Parse the response JSON to obtain the galaxy coordinates
    data = response.json()
    galaxies = [(i + 1, float(entry['ra']), float(entry['dec'])) for i, entry in enumerate(data)]
    return galaxies
  else:
    print(f"Error: Unable to fetch galaxy data. Status code: {response.status_code}")
    return []


# Given point (RA, Dec) in degrees
ra_point = 184.9511
dec_point = -0.8754

# Query galaxies within 1 arcminute of the given point
galaxies_within_1arcmin = query_galaxies(ra_point, dec_point)


# Function to get the image cutouts for the galaxies
def get_galaxy_images(galaxies, image_size=256):
  # Base URL for the SDSS API's Image Cutout service
  base_url = "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg"

  for i, (ra, dec) in enumerate(galaxies):
    # Construct the API request URL for each galaxy
    url = f"{base_url}?ra={ra}&dec={dec}&scale=0.2&width={image_size}&height={image_size}"

    # Make the HTTP GET request to the SDSS API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
      # Save the image as a file
      with open(f"galaxy_{i+1}.jpg", "wb") as f:
        f.write(response.content)
      print(f"Image for galaxy {i+1} saved as galaxy_{i+1}.jpg")
    else:
      print(f"Error: Unable to fetch the image for galaxy {i+1}. Status code: {response.status_code}")


# Get images for the galaxies within 1 arcminute
get_galaxy_images(galaxies_within_1arcmin)
