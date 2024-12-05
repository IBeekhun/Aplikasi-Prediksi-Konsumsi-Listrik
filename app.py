# Import pustaka yang diperlukan
import streamlit as st  # Framework untuk membangun aplikasi web interaktif
from streamlit_option_menu import option_menu  # Membuat sidebar navigasi dengan menu yang rapi
import pandas as pd  # Untuk manipulasi dan analisis data dalam format tabel
from sklearn.linear_model import LinearRegression  # Untuk membuat model regresi linier
from sklearn.model_selection import train_test_split  # Untuk membagi dataset menjadi data training dan testing
from sklearn.metrics import mean_squared_error, r2_score  # Metrik evaluasi untuk model regresi
import nbformat  # Untuk membaca file Jupyter Notebook (.ipynb)
from nbconvert import HTMLExporter  # Untuk mengonversi file Notebook menjadi HTML
import io  # Mengelola input/output, khususnya untuk menangkap output dari eksekusi kode
import contextlib  # Mengarahkan output ke buffer tertentu
import sys  # Akses ke parameter dan fungsi sistem

# Pengaturan halaman navigasi
st.set_page_config(page_title="Aplikasi Prediksi Konsumsi Listrik", layout="wide")
# Mengatur judul tab browser menjadi "Aplikasi Prediksi Konsumsi Listrik"
# Mengatur tata letak aplikasi menjadi "wide" agar elemen di layar lebih lebar.

# Menu navigasi
with st.sidebar:  # Membuat sidebar untuk navigasi aplikasi
    selected = option_menu(
        menu_title="Navigasi",  # Judul menu
        options=["Halaman Utama", "Analisis MLR", "Unggah Gambar", "Gambar Statis", "Notebook", "Editor Kode"],  # Pilihan menu
        icons=["house", "bar-chart-line", "file-image", "image", "file-earmark-code", "code"],  # Ikon untuk setiap menu
        default_index=0,  # Pilihan default yang akan ditampilkan pertama kali
    )

# Halaman Utama
if selected == "Halaman Utama":
    st.title("Selamat Datang di Aplikasi Prediksi Konsumsi Listrik")
    # Menampilkan judul utama halaman
    st.write("Diciptakan untuk Solusi Masa Depan yang Lebih Cerdas dan Efisien.")
    # Memberikan deskripsi singkat mengenai aplikasi
    st.image("16694.jpg")  # Menampilkan gambar dengan file name `16694.jpg`
    st.write(
        "Selamat datang di aplikasi prediksi konsumsi listrik yang dirancang khusus untuk membantu memahami dan memprediksi kebutuhan energi dengan akurat. "
        "Aplikasi ini menggabungkan teknologi Multiple Linear Regression (MLR) dengan data yang telah dikumpulkan untuk memberikan prediksi yang akurat dan bermanfaat. "
        "Dikembangkan oleh Rifai Machri (NPM: 121055520121124), aplikasi ini tidak hanya membantu dalam analisis konsumsi listrik tetapi juga menjadi alat edukatif bagi Anda yang ingin memahami pola dan efisiensi energi."
    )
    # Memberikan informasi detail tentang manfaat aplikasi ini.

# Halaman Analisis MLR
elif selected == "Analisis MLR":
    st.title("Analisis Multiple Linear Regression (MLR)")
    # Judul halaman untuk analisis MLR
    st.write(
        "Selamat datang di halaman Analisis Multiple Linear Regression (MLR), di mana data berbicara dan keputusan menjadi lebih cerdas! "
        "Pada halaman ini, Anda dapat memprediksi konsumsi listrik dengan model statistik yang didukung oleh variabel-variabel penting, seperti Area, Jumlah Penghuni, "
        "Jumlah Alat Listrik, dan Jam Penggunaan. Temukan pola, buat prediksi, dan jelajahi berbagai aspek konsumsi energi untuk wawasan yang lebih mendalam!"
    )
    # Deskripsi mengenai fungsi halaman ini

    # Mengunggah data
    uploaded_file = st.file_uploader(
        "Silahkan Unggah file CSV dengan kolom Area, Jumlah_Penghuni, Jumlah_Alat_Listrik, Jam_Penggunaan, dan Konsumsi_Listrik",
        type="csv",
    )
    # Komponen untuk mengunggah file CSV

    if uploaded_file is not None:
        # Jika ada file yang diunggah
        data = pd.read_csv(uploaded_file)  # Membaca data dari file CSV
        st.write("Data yang diunggah:")  # Menampilkan data yang diunggah
        st.dataframe(data.head())  # Menampilkan 5 baris pertama dari data

        if all(col in data.columns for col in ["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Konsumsi_Listrik"]):
            # Memastikan bahwa data memiliki kolom yang diperlukan
            X = data[["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan"]]
            # Variabel input (predictors)
            Y = data["Konsumsi_Listrik"]
            # Variabel target
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
            # Membagi data menjadi training dan testing

            model = LinearRegression()  # Membuat model Linear Regression
            model.fit(X_train, Y_train)  # Melatih model dengan data training
            Y_pred = model.predict(X_test)  # Melakukan prediksi dengan data testing

            st.write("Koefisien regresi:")
            coef_df = pd.DataFrame(model.coef_, X.columns, columns=["Koefisien"])
            st.write(coef_df)  # Menampilkan koefisien model
            st.write("Intercept:", model.intercept_)  # Menampilkan intercept
            st.write("Mean Squared Error (MSE):", mean_squared_error(Y_test, Y_pred))
            # Menampilkan nilai MSE
            st.write("R-squared:", r2_score(Y_test, Y_pred))
            # Menampilkan nilai R-squared

            intercept = model.intercept_  # Menyimpan nilai intercept
            b = model.coef_  # Menyimpan nilai koefisien

            st.subheader("Prediksi Konsumsi Listrik Berdasarkan Input Pengguna")
            # Form input untuk prediksi manual
            Area_input = st.number_input("Masukkan nilai Area (m²)", value=0.0)
            Jumlah_Penghuni_input = st.number_input("Masukkan Jumlah Penghuni", value=0)
            Jumlah_Alat_Listrik_input = st.number_input("Masukkan Jumlah Alat Listrik", value=0)
            Jam_Penggunaan_input = st.number_input("Masukkan Jam Penggunaan", value=0.0)

            if "prediction_table" not in st.session_state:
                # Inisialisasi tabel prediksi jika belum ada
                st.session_state["prediction_table"] = pd.DataFrame(
                    columns=["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Prediksi Konsumsi Listrik"]
                )

            if st.button("Prediksi"):
                # Jika tombol prediksi ditekan
                prediksi = intercept + b[0] * Area_input + b[1] * Jumlah_Penghuni_input + b[2] * Jumlah_Alat_Listrik_input + b[3] * Jam_Penggunaan_input
                # Menghitung prediksi berdasarkan model

                input_data = pd.DataFrame(
                    [[Area_input, Jumlah_Penghuni_input, Jumlah_Alat_Listrik_input, Jam_Penggunaan_input, prediksi]],
                    columns=["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Prediksi Konsumsi Listrik"],
                )
                st.session_state["prediction_table"] = pd.concat([st.session_state["prediction_table"], input_data], ignore_index=True)
                st.write("Hasil Prediksi:")
                st.dataframe(st.session_state["prediction_table"])
elif selected == "Unggah Gambar":
    st.title("Unggah dan Tampilkan Gambar")
    # Judul halaman untuk mengunggah dan menampilkan gambar

    uploaded_image = st.file_uploader("Unggah gambar dalam format JPG atau PNG", type=["jpg", "png"])
    # Komponen untuk mengunggah file gambar dengan format yang didukung

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Gambar yang diunggah", use_column_width=True)
        # Menampilkan gambar yang diunggah beserta keterangan (caption)
elif selected == "Gambar Statis":
    st.title("Gambar Statis")
    # Judul halaman untuk menampilkan gambar statis

    st.image("16510.jpg", caption="Gambar Statis", use_column_width=True)
    # Menampilkan gambar statis dari file bernama `16510.jpg` beserta keterangan
elif selected == "Notebook":
    st.title("Tampilkan File Notebook Jupyter")
    # Judul halaman untuk menampilkan file Jupyter Notebook (.ipynb)

    uploaded_notebook = st.file_uploader("Unggah file Jupyter Notebook (.ipynb)", type="ipynb")
    # Komponen untuk mengunggah file dengan format .ipynb

    if uploaded_notebook is not None:
        notebook_content = nbformat.read(uploaded_notebook, as_version=4)
        # Membaca konten file notebook dengan format nbformat

        html_exporter = HTMLExporter()
        # Membuat objek HTMLExporter untuk mengonversi notebook ke HTML
        html_exporter.exclude_input = True
        # Menghilangkan bagian input kode pada tampilan HTML
        body, _ = html_exporter.from_notebook_node(notebook_content)
        # Menghasilkan HTML dari file notebook

        st.components.v1.html(body, height=800, scrolling=True)
        # Menampilkan HTML hasil konversi pada aplikasi
elif selected == "Editor Kode":
    st.title("Editor Kode Interaktif")
    # Judul halaman untuk editor kode interaktif

    code_input = st.text_area("Masukkan kode Python di bawah ini dan klik Jalankan:", height=300)
    # Komponen text area untuk menulis kode Python yang akan dijalankan

    if st.button("Jalankan"):
        # Jika tombol 'Jalankan' ditekan
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                exec(code_input, {})  # Menjalankan kode Python yang dimasukkan pengguna
                result = buf.getvalue()  # Menyimpan hasil eksekusi kode
            except Exception as e:
                result = str(e)  # Menyimpan pesan kesalahan jika terjadi error
        st.text_area("Hasil Output:", result, height=300)
        # Menampilkan hasil eksekusi kode pada area teks
if st.button("Jalankan Kode"):
    # Jika tombol "Jalankan Kode" ditekan

    # Membuat buffer untuk menangkap output eksekusi
    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec_globals = {}
            # Menjalankan kode Python dari input pengguna
            exec(code_input, exec_globals)

        # Menampilkan hasil eksekusi jika ada
        output = output_buffer.getvalue()
        if output:
            st.subheader("Hasil Eksekusi Kode:")
            st.code(output)
        else:
            st.write("Kode berhasil dijalankan tanpa output.")
    except Exception as e:
        # Menangkap dan menampilkan error jika terjadi
        st.error(f"Terjadi kesalahan saat menjalankan kode: {e}")
    finally:
        # Membersihkan buffer output
        output_buffer.close()
