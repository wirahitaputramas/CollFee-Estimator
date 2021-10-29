import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_CategoryID = data["le_CategoryID"]
le_bucketovd = data["le_bucketovd"]
le_typeRepoFee = data["le_typeRepoFee"]
le_Kasus = data["le_Kasus"]
le_kondisiAset = data["le_kondisiAset"]
le_kondisi = data["le_kondisi"]

def show_predict_page():
    st.title("MTF Collection Fee Estimator")

    st.write("""### We need some information to estimate the Collection Fee""")

    CategoryID = (
        "PASSENGER",
        "PICK UP   ",
        "TRUCK     ",
        "BULDOZER  ",
        "MOTOR",
        "Excavator ",
        "Truck-HE  ",
        "GENERATOR ",
        "TRACTORS  ",
        "MOTORGRAD ",
        "PUMP      ",
        "LANDFILL  ",
    )

    bucketovd = (
        "1. 0-30",
        "Writeoff",
        "2. 31-60",
        "3. 61-90d",
        "4. 91-120",
        "5. 121-150",
        "6. 151-180",
        "7. >180",
    )

    typeRepoFee = (
        "fee_standar",
        "fee_standar_plus_expense",
    )

    Kasus = (
        "unknown",
        "Kasus",
        "Kasus Berat",
        "Administratif",
    )

    kondisiAset = (
        "Asset Atas Nama",
        "Asset ada di luar kota",
        "Asset ada di dalam kota",
        "Biaya sayembara",
    )

    kondisi = (
        "Customer ada, unit tidak ada",
        "Customer ada, unit ada",
        "Customer tidak ada, unit ada",
        "Customer tidak ada, unit tidak ada",
    )

    selCategoryID = st.selectbox("CategoryID", CategoryID)
    selbucketovd = st.selectbox("bucketovd", bucketovd)
    seltypeRepoFee = st.selectbox("typeRepoFee", typeRepoFee)
    selKasus = st.selectbox("Kasus", Kasus)
    selkondisiAset = st.selectbox("kondisiAset", kondisiAset)
    selkondisi = st.selectbox("kondisi", kondisi)

    ok = st.button("Estimate Collection Fee")
    if ok:
        X = np.array([[selCategoryID, selbucketovd, seltypeRepoFee, selKasus, selkondisiAset, selkondisi]])
        X[:, 0] = le_CategoryID.transform(X[:,0])
        X[:, 1] = le_bucketovd.transform(X[:,1])
        X[:, 2] = le_typeRepoFee.transform(X[:,2])
        X[:, 3] = le_Kasus.transform(X[:,3])
        X[:, 4] = le_kondisiAset.transform(X[:,4])
        X[:, 5] = le_kondisi.transform(X[:,5])
        X = X.astype(float)

        collFee = regressor.predict(X)
        collFee = int(collFee)

        collFeeIntLower = collFee - 2500000
        collFeeIntUpper = collFee + 2500000

        if (collFee <= 2500000) and (collFee >= 1000000):
            collFeeIntLower = 500000

        if (collFee < 1000000):
            collFeeIntLower = 50000
            collFeeIntUpper = 1000000
        
        st.subheader(f"The estimated range of collection fee is IDR {collFeeIntLower} - IDR {collFeeIntUpper}")
