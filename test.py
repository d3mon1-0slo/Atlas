import geocoder

# 'me' uses your current IP address to find location
g = geocoder.ip('me')

if g.latlng:
    lat, lon = g.latlng
    print(f"Latitude: {lat}, Longitude: {lon}")
else:
    print("Location not found.")
