import streamlit as st
import random
import time

# Define the board with snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Initialize session state
if "position" not in st.session_state:
    st.session_state.position = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("Snake and Ladder Game 🎲🐍🪜")

# Display the board
st.write("Snakes: ", snakes)
st.write("Ladders: ", ladders)
st.write(f"Your current position: {st.session_state.position}")

# Roll the die
if not st.session_state.game_over:
    if st.button("Roll the Die"):
        roll = random.randint(1, 6)
        st.write(f"You rolled a {roll}!")

        # Update position
        new_position = st.session_state.position + roll
        if new_position > 100:
            st.write("Roll exceeds position 100. Stay at current position.")
        else:
            st.session_state.position = new_position
            st.write(f"You moved to position {st.session_state.position}")

            # Check for snakes or ladders
            if st.session_state.position in snakes:
                st.session_state.position = snakes[st.session_state.position]
                st.write(f"Oh no! A snake! You slid down to {st.session_state.position}")
            elif st.session_state.position in ladders:
                st.session_state.position = ladders[st.session_state.position]
                st.write(f"Yay! A ladder! You climbed up to {st.session_state.position}")

            # Check for win condition
            if st.session_state.position == 100:
                st.session_state.game_over = True
                st.write("🎉 Congratulations! You won the game! 🎉")

# Reset the game
if st.session_state.game_over or st.button("Restart Game"):
    st.session_state.position = 0
    st.session_state.game_over = False
    st.write("Game reset. Roll to start again!")
