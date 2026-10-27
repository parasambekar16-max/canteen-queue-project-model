# Canteen Queue Toolkit

## Setup in VS Code
1. Unzip, then File > Open Folder > `canteen_queue`.
2. Terminal > New Terminal, then:
   - `python -m venv venv`
   - Windows: `venv\Scripts\activate`   Mac/Linux: `source venv/bin/activate`
   - `pip install -r requirements.txt`
3. Run analysis: `python analyze.py` (creates tables/charts in `outputs/`)
4. Run web app: `streamlit run app.py`

## Use your own data
Replace `data/observed_arrivals.csv` (currently SAMPLE numbers) with your own
lunch-time observations, then re-run `analyze.py`.

## Deploy
Push this folder to GitHub, then share.streamlit.io > New app > pick `app.py`.
