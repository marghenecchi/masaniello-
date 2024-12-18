def get_valid_input(prompt, valid_options=None, is_float=False, min_value=None, max_value=None):
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("\nInvalid input. Please try again.")
                continue
            if is_float:
                value = float(value)
                if (min_value is None or value >= min_value) and (max_value is None or value <= max_value):
                    return value
                else:
                    print("\nInvalid input. Please try again.")
            elif valid_options:
                if value in valid_options:
                    return value
                else:
                    print("\nInvalid input. Please try again.")
            else:
                value = int(value)
                if (min_value is None or value >= min_value) and (max_value is None or value <= max_value):
                    return value
                else:
                    print("\nInvalid input. Please try again.")
        except ValueError:
            print("\nInvalid input. Please try again.")

def masaniello():
    initial_capital = get_valid_input("\nInitial capital: ", is_float=True, min_value=0)
    n_events = get_valid_input("\nNumber of events: ", min_value=1)
    expected_wins = get_valid_input("\nExpected wins: ", min_value=1, max_value=n_events)
    odds_mean= get_valid_input("\nOdds mean: ", is_float=True, min_value=0)
    current_wins = 0
    current_event = 0
    odds_type = get_valid_input("\nDo all events have the same odds? (1/0): ", valid_options=['1', '0'])
    capital=initial_capital

    while current_event < n_events and current_wins < expected_wins:
        if expected_wins - current_wins == 0 or n_events - current_event < expected_wins - current_wins:
            break

        # If odds are different for this event, ask for the new odds and update the array
        if odds_type == '0':
            odds = get_valid_input(f"\nEnter the odds for event {current_event + 1}: ", is_float=True, min_value=0)
        
        # Calculate the mean odds using the entire array

        # Initialize the matrix for calculating bets
        matrix = [[0] * (expected_wins + 1) for _ in range(n_events)]
        for i in range(n_events - 1, -1, -1):
            for j in range(expected_wins, -1, -1):
                if j == expected_wins:
                    matrix[i][j] = 1.0
                elif i > n_events - expected_wins + j:
                    matrix[i][j] = 0.0
                elif i == n_events - expected_wins + j:
                    matrix[i][j] = odds_mean * (1 if i == n_events - 1 else matrix[i + 1][j + 1])
                else:
                    matrix[i][j] = (odds_mean * matrix[i + 1][j] * matrix[i + 1][j + 1] /
                                    (matrix[i + 1][j] + (odds_mean - 1.0) * matrix[i + 1][j + 1]))

        # Calculate the current bet based on the mean odds
        current_bet = capital * (1 - odds[current_event] * matrix[current_event + 1][current_wins + 1] /
            (matrix[current_event + 1][current_wins] +
             (odds[current_event] - 1.0) * matrix[current_event + 1][current_wins + 1]))
        print(odds_mean)
        print(matrix)
        print(f"\nBet {current_event + 1}: {current_bet:.2f}")
        result = get_valid_input("\nW-L (1/0): ", valid_options=['1', '0'])

        if result == '1':
            win = (odds_mean - 1) * current_bet
            capital += win
            current_wins += 1
            print(f"\nWin: {win:.2f}, Current capital: {capital:.2f}")
        else:
            capital -= current_bet
            print(f"\nCurrent capital: {capital:.2f}")

        current_event += 1

        resa_totale=initial_capital*matrix[0][0]
        print(f"\nResa totale: {resa_totale:.2f}")

    print(f"\nFinal capital: {capital:.2f}")
    print(f"\nFinal odds array: {odds_array}")
    print(f"\nFinal odds mean: {odds_mean:.2f}")
 

if __name__ == "__main__":
    masaniello()
