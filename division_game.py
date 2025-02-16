import time
import random
import streamlit as st

import pandas as pd

def generate_numbers(maximum_divisor, maximum_quotient):
    """Generate a random dividend and divisor for integer division."""
    generated_divisor = random.randint(1, maximum_divisor)  # Avoid zero as divisor
    generated_dividend = generated_divisor * random.randint(1, maximum_quotient)  # Ensure exact division
    return generated_dividend, generated_divisor

st.title("Division Game")

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.correct_answers = 0
    st.session_state.start_time = None
    st.session_state.game_active = False
    st.session_state.user_answers = []
    st.session_state.timer_active = False

# Select the number of questions, max divisor, and max quotient
if not st.session_state.game_active:
    num_questions = st.slider("Choose the number of questions:", min_value=1, max_value=50, value=10)
    max_divisor = st.slider("Set the maximum divisor:", min_value=1, max_value=100, value=20)
    max_quotient = st.slider("Set the maximum quotient:", min_value=1, max_value=100, value=20)
    st.session_state.timer_active = st.checkbox("Activate timer")
    if st.button("Start Game"):
        st.session_state.questions = [generate_numbers(max_divisor, max_quotient) for _ in range(num_questions)]
        st.session_state.current_index = 0
        st.session_state.correct_answers = 0
        st.session_state.user_answers = []
        if st.session_state.timer_active:
            st.session_state.start_time = time.time()
        st.session_state.game_active = True
        st.rerun()

if st.session_state.game_active:
    if st.session_state.current_index < len(st.session_state.questions):
        dividend, divisor = st.session_state.questions[st.session_state.current_index]
        st.write(f"Question {st.session_state.current_index + 1}: {dividend} ÷ {divisor} = ?")

        user_input = st.number_input("Your answer:", min_value=0, step=1, format="%d",
                                     key=f"input_{st.session_state.current_index}")

        if st.button("Submit"):
            correct_result = dividend // divisor
            st.session_state.user_answers.append((dividend, divisor, user_input, correct_result))
            if user_input == correct_result:
                st.session_state.correct_answers += 1
                st.success("Correct answer!")
            else:
                st.error(f"Wrong answer! The correct answer was {correct_result}.")

            st.session_state.current_index += 1
            st.rerun()
    else:
        # End of the game
        total_time = time.time() - st.session_state.start_time if st.session_state.timer_active else None
        st.success(f"Game over! Score: {st.session_state.correct_answers}/{len(st.session_state.questions)}")
        if total_time:
            st.write(f"Total time: {total_time:.2f} seconds")

        # Display recap table
        recap_data = {
            "Dividend": [q[0] for q in st.session_state.user_answers],
            "Divisor": [q[1] for q in st.session_state.user_answers],
            "Your Answer": [q[2] for q in st.session_state.user_answers],
            "Correct Answer": [q[3] for q in st.session_state.user_answers]
        }
        recap_df = pd.DataFrame(recap_data)
        st.table(recap_df)

        if st.button("Play Again"):
            st.session_state.game_active = False
            st.session_state.questions = []
            st.rerun()
            