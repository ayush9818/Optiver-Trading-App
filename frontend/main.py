import warnings

warnings.filterwarnings("ignore")

import requests
import os
from handlers.api_handler import APIHandler
from handlers.s3_handler import S3Handler
import streamlit as st
import plotly.express as px
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from utils import get_holidays, convert_to_meaningful_time, get_date_from_date_id
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Load environment variables from .env file
load_dotenv()


# Function to inject CSS
def inject_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Inject your custom CSS
inject_css("style.css")

# Your Streamlit app code
st.title("Stock Analysis Dashboard")


# Create three columns with different widths
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image("images/app_frontend.jpg", caption="Stock Analysis")

if __name__ == "__main__":
    # Create artifacts directory to keep model files
    artifact_dir = Path() / "artifacts"
    artifact_dir.mkdir(exist_ok=True)

    # Retrieve the base URL from environment variables
    BASE_GET_API = os.getenv("BASE_GET_API")
    BASE_POST_API = os.getenv("BASE_POST_API")

    # Initialize API handler in session state
    if "api_handler" not in st.session_state:
        st.session_state["api_get_handler"] = APIHandler(base_url=BASE_GET_API)
        st.session_state["api_post_handler"] = APIHandler(base_url=BASE_POST_API)

    if "all_models" not in st.session_state:
        st.session_state["all_models"] = None

    if "last_date_id" not in st.session_state:
        st.session_state["last_date_id"] = 0

    if "last_model_id" not in st.session_state:
        st.session_state["last_model_id"] = 0

    if "last_model_name" not in st.session_state:
        st.session_state["last_model_name"] = ""

    if "last_fetch_time" not in st.session_state:
        st.session_state["last_fetch_time"] = None

    if "holiday_dates_2023" not in st.session_state:
        st.session_state["holiday_dates_2023"] = get_holidays("US", 2023)

    if "inference_data" not in st.session_state:
        st.session_state["inference_data"] = None

    if "training_success" not in st.session_state:
        st.session_state["training_success"] = False

    def fetch_models():
        # Fetch all models from the API
        all_models = st.session_state["api_get_handler"].get("/models/", {})
        print(all_models)

        if all_models:
            last_model = sorted(all_models, key=lambda x: x["date_id"], reverse=True)[0]
            st.session_state["last_date_id"] = last_model["date_id"]
            st.session_state["last_model_id"] = last_model["model_id"]
            st.session_state["last_model_name"] = last_model["model_name"]
        st.session_state["all_models"] = all_models
        st.session_state["last_fetch_time"] = datetime.now()

        st.rerun()  # Ensure the page re-runs to update display

    # Automatically fetch models when the app loads
    if "all_models" not in st.session_state or st.session_state["all_models"] is None:
        fetch_models()

    # Display the result
    if st.session_state["all_models"] is not None:
        st.write(f"Last Date ID: {st.session_state['last_date_id']}")
        st.write(f"Last Model ID: {st.session_state['last_model_id']}")
        st.write(f"Last Model Name: {st.session_state['last_model_name']}")

        # TEST
        # st.write("All Models:", st.session_state['all_models'])
        # if st.session_state['last_fetch_time'] is not None:
        #     st.write(f"Last Fetch Time: {st.session_state['last_fetch_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.write("No models fetched yet. Click 'Fetch Last Model ID' to fetch models.")

    try:
        max_date_id = int(os.getenv("MAX_DATE_ID", 0))  # Default to 0 if not set
    except ValueError:
        max_date_id = 0  # Default to 0 if conversion fails

    model_training_tab, model_inferences_tab, show_data_tab = st.tabs(
        ["Model Training", "Model Inferences", "Show Data"]
    )
    with model_training_tab:
        # Calculate the training date ID
        train_date_id = min(st.session_state["last_date_id"] + 1, max_date_id)

        # Display the date ID input (disabled)
        # st.markdown(f"Date ID (range from 1-{max_date_id})")
        # train_date_id_input = st.text_input("", train_date_id, key="train_date_id", disabled=True, label_visibility="collapsed")

        st.markdown(f"Date")
        train_date_input = st.text_input(
            "",
            get_date_from_date_id(
                train_date_id, holidays=st.session_state["holiday_dates_2023"]
            ),
            key="train_date",
            disabled=True,
            label_visibility="collapsed",
        )

        # Display the base model name input (disabled)
        st.markdown("Base Model Name")
        base_model_name_input = st.text_input(
            "",
            f"optiver-{st.session_state['last_date_id']}",
            key="base_model_name",
            disabled=True,
            label_visibility="collapsed",
        )

        train_button_clicked = st.button("Train")
        if train_button_clicked:
            # Prepare data for the API request
            model_train_data = {
                "model_id": st.session_state[
                    "last_model_id"
                ],  # ID of the initial model to be fine-tuned
                "model_name": f"optiver-{train_date_id}",  # Name for the new model
                "date_id": train_date_id,  # Date ID for training data
            }

            # Send POST request to start the training process with error handling
            try:
                train_model_endpoint = "/train-model/"
                response = st.session_state["api_post_handler"].post(
                    train_model_endpoint, model_train_data
                )
                st.session_state["training_success"] = True
                fetch_models()
            except requests.exceptions.HTTPError as err:
                st.session_state["training_success"] = False
                if err.response.status_code == 500:
                    st.error(
                        "Error 500: Internal Server Error occurred while starting the training process."
                    )
                else:
                    st.error(f"An error occurred: {err}")

        # Display success message if training was successful
        if st.session_state["training_success"]:
            st.success(
                f"The newly trained model {st.session_state['last_model_name']} has been successfully uploaded to S3."
            )

    with model_inferences_tab:
        # Calculate the prediction date ID
        prediction_date_id = min(st.session_state["last_date_id"] + 1, max_date_id + 1)
        # Display the prediction date ID input (disabled)
        # st.markdown(f"Prediction Date ID (range from 1-{max_date_id})")
        # prediction_date_id_input = st.text_input(
        #     "",
        #     prediction_date_id,
        #     key="prediction_date_id",
        #     disabled=True,
        #     label_visibility="collapsed"
        # )

        st.markdown(f"Date")
        prediction_date_input = st.text_input(
            "",
            get_date_from_date_id(
                train_date_id, holidays=st.session_state["holiday_dates_2023"]
            ),
            key="prediction_date",
            disabled=True,
            label_visibility="collapsed",
        )

        # Display the last model name input (disabled)
        st.markdown("Last Model Name")
        last_model_name_input = st.text_input(
            "",
            st.session_state["last_model_name"],
            key="last_model_name_input",
            disabled=True,
            label_visibility="collapsed",
        )

        button_clicked = st.button("Inference")
        if button_clicked:
            # inference-model (POST, PORT 81) first then model-inference (GET, PORT 80)
            # Define the endpoint for inference model
            inference_model_endpoint = "/inference-model/"

            inference_model_data = {
                "model_id": st.session_state["last_model_id"],
                "pred_date_id": prediction_date_id,
            }
            # Model inference from the API with error handling
            try:
                model_data = st.session_state["api_post_handler"].post(
                    inference_model_endpoint, inference_model_data
                )
                st.info("Inference completed successfully!")
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 500:
                    st.error(
                        "Error 500: Internal Server Error occurred while performing inference."
                    )
                else:
                    st.error(f"An error occurred: {err}")

            model_inference_endpoint = "/model-inferences/"
            model_inference_data = {
                "model_id": st.session_state["last_model_id"],  # ID of the model
                "date_id": prediction_date_id,  # ID of the date.
            }

            # fetch the s3 path
            model_inferences_data = st.session_state["api_get_handler"].get(
                model_inference_endpoint, model_inference_data
            )
            s3_path = model_inferences_data[0]["predictions"]

            inference_data_local_path = S3Handler().download_file(
                s3_path, artifact_dir
            )  # f'inference_{request.model_id}_{request.pred_date_id}.csv'
            # inference_data_local_path = "artifacts/inference_24_405.csv"

            # Load inference data outside of the try block to catch file-specific errors separately
            try:
                st.session_state["inference_data"] = pd.read_csv(
                    inference_data_local_path
                )
            except Exception as e:
                st.error(f"Failed to load data: {e}")
                inference_data = None

        # Initialize or load existing session state variables
        if "stock_id_display" not in st.session_state:
            st.session_state["stock_id_display"] = ""

        # Create a fixed container at the top for inputs
        input_container = st.container()

        tab1, tab2 = st.tabs(["Show Inference Data", "Plot Prediction Data"])

        inference_data = st.session_state["inference_data"]
        if inference_data is not None and "stock_id" in inference_data.columns:
            # Place the input field in the fixed container
            with input_container:
                # Placeholders for text input within the container
                stock_id_display_input = st.text_input(
                    label="Enter a stock ID to display inference data 😎",
                    value=st.session_state["stock_id_display"],
                    key="show_inference_data_input",
                )
                # Update the session state based on the input
                st.session_state["stock_id_display"] = stock_id_display_input

            # Filter data by the entered stock ID, assuming it's valid and a part of the dataframe
            try:
                if st.session_state["stock_id_display"].strip():
                    stock_id_int = int(
                        st.session_state["stock_id_display"]
                    )  # Ensure the ID is integer
                    inference_data_filtered = inference_data[
                        inference_data["stock_id"] == stock_id_int
                    ]

                    if not inference_data_filtered.empty:
                        with tab1:
                            if not inference_data_filtered.empty:
                                st.dataframe(
                                    inference_data_filtered, use_container_width=True
                                )
                            else:
                                st.warning(
                                    "No available data for the entered stock ID."
                                )

                        with tab2:
                            if not inference_data_filtered.empty:
                                if (
                                    "prediction" in inference_data_filtered.columns
                                    and "target" in inference_data_filtered.columns
                                ):
                                    col1, col2, col3 = st.columns(
                                        [1, 2, 1]
                                    )  # Create columns to control layout
                                    with col1:  # Place chart in the middle column
                                        # Create a figure and axis with a specific size
                                        fig, ax = plt.subplots(figsize=(10, 6))

                                        # Plotting the predicted and actual prices
                                        ax.plot(
                                            inference_data_filtered[
                                                "seconds_in_bucket"
                                            ],
                                            inference_data_filtered["prediction"],
                                            label="Prediction",
                                            linestyle="-",
                                            color="royalblue",
                                        )
                                        ax.plot(
                                            inference_data_filtered[
                                                "seconds_in_bucket"
                                            ],
                                            inference_data_filtered["target"],
                                            label="Target",
                                            linestyle="--",
                                            color="darkorange",
                                        )

                                        # Setting labels, legend, and title
                                        ax.set_xlabel("Seconds in Bucket")
                                        ax.set_ylabel("Value")
                                        plt.title(
                                            f"Prediction vs. Target for Stock ID {st.session_state['stock_id_display']}"
                                        )
                                        ax.legend()

                                        # Enabling grid for better readability
                                        ax.grid(True)
                                        # Tight layout for neatness
                                        plt.tight_layout()
                                        # Display the plot in Streamlit or any other preferred frontend
                                        st.pyplot(fig)
                                else:
                                    st.warning(
                                        "'prediction' or 'target' columns are missing in the data."
                                    )
                    else:
                        st.warning("No available data for the entered stock ID.")
            except ValueError:
                st.error("Please enter a valid numeric stock ID.")

    with show_data_tab:
        # Input for stock_id with validation
        stock_id_input = st.text_input("Enter the stock ID for plotting", value="0")

        # Input for chart start date
        chart_date_id = st.text_input(
            f"Enter the date id for plotting (range from 1-480)", value="1"
        )

        st.markdown(f"Selected date for plotting")
        chart_date_input = st.text_input(
            "",
            get_date_from_date_id(
                int(chart_date_id), holidays=st.session_state["holiday_dates_2023"]
            ),
            key="chart_date",
            disabled=True,
            label_visibility="collapsed",
        )

        # Convert input values to integers and handle errors
        try:
            date_id = int(chart_date_id)
            stock_id = int(stock_id_input)
        except ValueError:
            st.error("Date ID and stock ID must be integers.")
            date_id = None
            stock_id = None

        # Validate that end date ID is greater than or equal to start date ID
        if date_id is not None:
            if date_id > 480:
                st.error("Date ID must be less than 480.")
            elif stock_id < 0 or stock_id > 199:
                st.error("Stock ID must be between 0 and 199.")
            else:
                # Proceed if validation passes
                show_data_button_clicked = st.button("Show Data")
                if show_data_button_clicked:
                    query_params = {"start_date_id": date_id, "end_date_id": date_id}
                    print(query_params)
                    stock_data_result = st.session_state["api_get_handler"].get(
                        api_url="/stock_data/", params=query_params
                    )

                    # Convert the list of dictionaries to a pandas DataFrame
                    df = pd.DataFrame(stock_data_result)
                    df_filtered = df[df["stock_id"] == stock_id]

                    st.info("Show Stock Data")
                    st.dataframe(df_filtered, use_container_width=True)

                    # Sort the filtered DataFrame by date_id
                    df_filtered = df_filtered.sort_values(by="time_id")

                    # Apply the get_date_from_date_id function to each row_id
                    meaningful_timestamps = (
                        df_filtered["row_id"]
                        .apply(
                            lambda x: convert_to_meaningful_time(
                                x, holidays=st.session_state["holiday_dates_2023"]
                            )
                        )
                        .tolist()
                    )

                    df_filtered["meaningful_timestamp"] = meaningful_timestamps

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )  # Create columns to control layout
                    with col1:  # Place plot in the middle column
                        # Plot the filtered data with returns
                        fig, ax = plt.subplots(figsize=(6, 3))

                        # Plotting the target values
                        ax.plot(
                            df_filtered["meaningful_timestamp"],
                            df_filtered["target"],
                            linestyle="-",
                            color="royalblue",
                            marker=None,
                        )

                        # Setting labels and title
                        ax.set_xlabel("Timestamp")
                        ax.set_ylabel("Target (Basis Points)")
                        date_str = (
                            df_filtered["meaningful_timestamp"]
                            .iloc[0]
                            .strftime("%Y-%m-%d")
                        )
                        ax.set_title(
                            f"Target vs. Timestamp for Stock ID {stock_id} on {date_str}"
                        )

                        # Formatting the x-axis to only show time in HH:MM:SS format
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
                        ax.xaxis.set_major_locator(
                            mdates.MinuteLocator(interval=1)
                        )  # Adjust depending on data density

                        # Adding grid, legend, and adjusting tick rotation for better readability
                        ax.grid(True)
                        ax.legend()
                        plt.xticks(rotation=45)

                        # Ensuring a tight layout so everything fits without clipping
                        plt.tight_layout()

                        # Displaying the plot in Streamlit
                        st.pyplot(fig)
