import os
import urllib.request

# Create folder for images
os.makedirs("images", exist_ok=True)

# List of all pieces
pieces = ["wp", "bp", "wn", "bn", "wb", "bb", "wr", "br", "wq", "bq", "wk", "bk"]

# Working CDN source (PNG images)
base_url = "https://images.chesscomfiles.com/chess-themes/pieces/neo/150"

# Download each image
for piece in pieces:
    url = f"{base_url}/{piece}.png"
    file_path = f"images/{piece}.png"
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"✅ Downloaded: {piece}")
    except Exception as e:
        print(f"❌ Failed to download {piece}: {e}")

print("\n🎉 All chess piece images are ready in the 'images' folder!")
