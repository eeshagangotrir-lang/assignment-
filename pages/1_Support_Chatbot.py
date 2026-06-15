import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="MiniStore Support",
    page_icon="💬"
)

st.title("💬 MiniStore Customer Support")

# --------------------------------------------------
# OpenAI Client
# --------------------------------------------------
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# --------------------------------------------------
# Store Product Catalog
# --------------------------------------------------
PRODUCT_CATALOG = """
MiniStore Product Catalog

1. Wireless Headphones
   Price: $89.99
   Category: Electronics
   Description: Premium noise-cancelling wireless headphones with long battery life.

2. Smart Watch Pro
   Price: $149.99
   Category: Electronics
   Description: Smartwatch with fitness tracking and notifications.

3. Classic Backpack
   Price: $49.99
   Category: Fashion
   Description: Durable backpack suitable for daily use.

4. Running Shoes
   Price: $79.99
   Category: Fashion
   Description: Lightweight and comfortable running shoes.

5. Coffee Maker
   Price: $119.99
   Category: Home
   Description: Automatic coffee machine for home brewing.

6. Desk Lamp
   Price: $34.99
   Category: Home
   Description: LED desk lamp with adjustable brightness.
"""

# --------------------------------------------------
# System Prompt
# --------------------------------------------------
SYSTEM_PROMPT = f"""
You are MiniStore's professional customer support assistant.

Your responsibilities:
- Answer questions about MiniStore products.
- Answer questions about orders.
- Answer questions about shipping and delivery.
- Answer questions about refunds.
- Answer questions about returns.
- Answer questions about payment methods.
- Help customers understand product information.

Store Product Information:
{PRODUCT_CATALOG}

Important Rules:
1. Only answer MiniStore-related support questions.
2. Do not answer general knowledge questions.
3. Do not answer coding, math, politics, entertainment, or unrelated topics.
4. If a question is unrelated, politely respond:

"I'm here to assist with MiniStore products, orders,
delivery, returns, refunds, and payments. How may I
help you with your MiniStore experience today?"

5. Be concise, professional, and friendly.
6. Never invent products not listed in the catalog.
"""

# --------------------------------------------------
# Chat History
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
user_prompt = st.chat_input(
    "Ask a question about products, orders, refunds, delivery..."
)

if user_prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Build Message List
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)

    # Assistant Response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.3
            )

            assistant_reply = (
                response.choices[0]
                .message
                .content
            )

            response_placeholder.markdown(
                assistant_reply
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

        except Exception as e:

            error_message = f"Error: {str(e)}"

            response_placeholder.error(
                error_message
            )