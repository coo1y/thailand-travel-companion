import utils
import streamlit as st

selected_sentiment = None
press_submit = False

st.set_page_config(
    page_title="Thailand Trip Companion",
    page_icon="🌴",
    layout="centered"
)

st.title("💬 Feedback")
st.write("Your rating:")
sentiment_mapping = ["1", "2", "3", "4", "5"]
selected_sentiment = st.feedback("stars")

opinion = st.text_area(
    "Your honest opinion about our system:",
    value=None,
    key="feedback",
)

uploaded_files = st.file_uploader(
    "Attach files/images (Optional)", accept_multiple_files=True
)

press_submit = st.button("Submit")

if selected_sentiment and opinion and press_submit:
    st.success('Thank you for your feedback.', icon="😊")

    with st.spinner("Uploading your feedback...", show_time=True):
        ## Upload all feedback files
        # write feedback files
        with open("result/feedback/feedback.txt", "w") as tf:
            tf.write(f"Star: {selected_sentiment}\n\n")
            tf.write(f"Opinion: {opinion}")

        utils.upload_feedback_files_to_blob()
        utils.upload_streamlit_multi_files_to_blob(uploaded_files=uploaded_files)

elif press_submit:
    st.error('Please fill all before submitting.', icon="⚠️")
