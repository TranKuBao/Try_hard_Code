import base64
import urllib.parse

# Open a text file for writing the encoded values
with open('encoded_values.txt', 'w') as file:
    # Loop through the range of users from 1 to 300
    for user_number in range(1001, 1501):
        # Create the user string (e.g., user1, user2, ..., user300)
        user_string = f"user{user_number}"

        # Encode the user string using base64
        encoded_user = base64.b64encode(user_string.encode('utf-8')).decode('utf-8')

        # URL encode the base64-encoded user string
        url_encoded_user = urllib.parse.quote(encoded_user)

        # Write the URL-encoded user string to the file
        file.write(url_encoded_user + '\n')

print("Encoding completed. Check 'encoded_values.txt' for the results.")
