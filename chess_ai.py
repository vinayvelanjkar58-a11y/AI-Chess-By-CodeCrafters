from stockfish import Stockfish

# Connect to Stockfish engine
stockfish = Stockfish(path=r"C:\Users\Asus\OneDrive\Attachments\stockfish-windows-x86-64-avx2.exe")

print("♟️ Welcome to AI Chess with Move Hints!")
print("You are playing as White. Enter moves in standard chess format (example: e2e4)\n")

while True:
    print("\nCurrent Board:")
    print(stockfish.get_board_visual())

    # Show top 3 move suggestions
    print("\n💡 AI Move Suggestions:")
    top_moves = stockfish.get_top_moves(3)
    for i, move in enumerate(top_moves, start=1):
        print(f"{i}. Move: {move['Move']}, Eval: {move['Centipawn']}")

    # Player move
    user_move = input("\nYour move (e.g., e2e4 or type 'quit' to exit): ").strip()
    if user_move.lower() == "quit":
        print("Thanks for playing!")
        break

    legal_moves = stockfish.get_legal_moves()
    if user_move not in legal_moves:
        print("❌ Invalid move! Try again.")
        continue

    stockfish.make_moves_from_current_position([user_move])

    # AI move
    ai_move = stockfish.get_best_move()
    print(f"\n🤖 AI plays: {ai_move}")
    stockfish.make_moves_from_current_position([ai_move])
