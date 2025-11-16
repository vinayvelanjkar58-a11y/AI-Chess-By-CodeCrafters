from stockfish import Stockfish

# -------------------------------------------------------------
# Connect to Stockfish Engine (Use your real Stockfish EXE path)
# -------------------------------------------------------------
stockfish = Stockfish(
    path=r"C:\stockfish\stockfish-windows-x86-64-avx2.exe",
    depth=15,
    parameters={"Threads": 2, "Minimum Thinking Time": 30}
)

print("\n♟️ Welcome to AI Chess with Move Hints!")
print("You are playing as WHITE. Enter moves like: e2e4, g1f3")

while True:
    print("\nCurrent Board:")
    print(stockfish.get_board_visual())

    # ---------------------------------------------------------
    # Show Top 3 Moves Suggested by AI
    # ---------------------------------------------------------
    print("\n🤖 AI Move Suggestions:")
    top_moves = stockfish.get_top_moves(3)

    for i, move in enumerate(top_moves, start=1):
        print(f"{i}. Move: {move['Move']}, Eval: {move['Centipawn']}")

    # ---------------------------------------------------------
    # Get Player Move
    # ---------------------------------------------------------
    player_move = input("\nYour Move (or 'exit'): ")

    if player_move.lower() == "exit":
        print("Game ended.")
        break

    # ---------------------------------------------------------
    # Validate Move
    # ---------------------------------------------------------
    if not stockfish.is_move_correct(player_move):
        print("❌ Invalid move! Try again.")
        continue

    # ---------------------------------------------------------
    # Apply Player Move
    # ---------------------------------------------------------
    stockfish.make_moves_from_current_position([player_move])

    # ---------------------------------------------------------
    # AI Moves Back
    # ---------------------------------------------------------
    ai_move = stockfish.get_best_move()
    print(f"🤖 AI plays: {ai_move}")
    stockfish.make_moves_from_current_position([ai_move])
