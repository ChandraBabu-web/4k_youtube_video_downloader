import streamlit as st
import random

# Define the board with snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Initialize session state
if "position" not in st.session_state:
    st.session_state.position = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🎲 Snake and Ladder Game 🐍🪜")

# Function to draw the grid
def draw_grid(current_position):
    # Create a 10x10 grid
    rows = 10
    cols = 10
    grid_numbers = [[None for _ in range(cols)] for _ in range(rows)]

    # Fill the grid with numbers from 1 to 100
    num = 100
    for i in range(rows):
        for j in range(cols):
            if i % 2 == 0:  # Left to right
                grid_numbers[rows - 1 - i][j] = num
            else:  # Right to left
                grid_numbers[rows - 1 - i][cols - 1 - j] = num
            num -= 1

    # Display the grid
    for row in grid_numbers:
        cols = st.columns(10)
        for idx, cell in enumerate(row):
            if cell == current_position:
                cols[idx].markdown(
                    f'<div style="background-color:#ADD8E6; border-radius:5px; padding:5px; text-align:center; font-weight:bold;">{cell}</div>',
                    unsafe_allow_html=True,
                )
            elif cell in snakes:
                cols[idx].markdown(f"**:red[{cell} 🐍]**")
            elif cell in ladders:
                cols[idx].markdown(f"**:green[{cell} 🪜]**")
            else:
                cols[idx].markdown(f"<div style='text-align:center;'>{cell}</div>", unsafe_allow_html=True)

# Display the grid
st.write("### 🕹️ Game Board")
draw_grid(st.session_state.position)

# Game controls
st.write(f"🎯 Your current position: **{st.session_state.position}**")

if not st.session_state.game_over:
    if st.button("🎲 Roll the Die"):
        roll = random.randint(1, 6)
        st.write(f"🎲 You rolled a **{roll}**!")

        # Update position
        new_position = st.session_state.position + roll
        if new_position > 100:
            st.write("🚫 Roll exceeds position 100. Stay at current position.")
        else:
            st.session_state.position = new_position
            st.write(f"🚶 You moved to position **{st.session_state.position}**")

            # Check for snakes or ladders
            if st.session_state.position in snakes:
                st.session_state.position = snakes[st.session_state.position]
                st.write(f"🐍 Oh no! A snake! You slid down to **{st.session_state.position}**")
            elif st.session_state.position in ladders:
                st.session_state.position = ladders[st.session_state.position]
                st.write(f"🪜 Yay! A ladder! You climbed up to **{st.session_state.position}**")

            # Check for win condition
            if st.session_state.position == 100:
                st.session_state.game_over = True
                st.balloons()
                st.write("🎉 **Congratulations! You won the game!** 🎉")

# Reset the game
if st.session_state.game_over or st.button("🔄 Restart Game"):
    st.session_state.position = 0
    st.session_state.game_over = False
    st.write("🔄 Game reset. Roll to start again!")
