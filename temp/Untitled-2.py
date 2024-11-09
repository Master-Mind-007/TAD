def rps(p1, p2):
    if p1 == p2:
        return "Draw!"
    
    winning_plays = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }

    # Check if p1 wins
    if winning_plays[p1] == p2:
        return "Player 1 won!"
    # Check if p2 wins
    elif winning_plays[p2] == p1:
        return "Player 2 won!"
    
print(rps("rock", "paper"))